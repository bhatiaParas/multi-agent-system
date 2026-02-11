"""Supervisor Agent - Orchestrates all sub-agents and coordinates responses."""
import os
import yaml
import json
from typing import Any, Dict, List, Tuple
from groq import Groq
from sub_agents.math_agent import MathAgent
from sub_agents.data_agent import DataAgent
from sub_agents.text_agent import TextAgent

class SupervisorAgent:
    """Supervisor Agent - Main orchestrator for multi-agent system."""
    
    def __init__(self, config_path: str = "config/supervisor_config.yaml"):
        self.config = self._load_config(config_path)
        self.groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        
        # Initialize sub-agents
        self.math_agent = MathAgent()
        self.data_agent = DataAgent()
        self.text_agent = TextAgent()
        
        self.name = "Supervisor Agent"
        self.verbose = self.config.get('logging', {}).get('verbose', True)
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"Warning: Config file not found at {config_path}")
            return {}
    
    def _log(self, message: str, level: str = "INFO"):
        """Log message."""
        if self.verbose or level != "DEBUG":
            prefix = f"[{level}]" if level != "INFO" else ""
            print(f"{prefix} {message}")
    
    def _extract_operation(self, query: str) -> Dict[str, Any]:
        """Extract operation and parameters from query."""
        self._log(f"[🔍 EXTRACTING OPERATION] From: {query}")
        
        extraction_prompt = f"""You are an expert at understanding data queries. Extract the OPERATION, AGENT TYPE, and NUMERIC PARAMETERS.

User Query: {query}

STEP 1: Identify the intent:
- Is this about COUNTING records, filtering, grouping, sorting, or aggregating DATA?
- Is this about MATH operations (add, divide, convert time)?
- Is this about TEXT operations (counting words, summarizing)?

STEP 2: Choose the correct OPERATION:

DATA OPERATIONS:
- count_records: How many records, total count, number of items
- filter_records: Filter, select, find specific records
- group_records: Group by, categorize
- sort_records: Sort, order
- aggregate_records: Sum, average, stats on data fields

MATH OPERATIONS:
- add, subtract, multiply, divide, power, square_root, convert_seconds, average, median, max_value, min_value, sum_numbers

TEXT OPERATIONS:
- count_words, summarize_text, extract_keywords, classify_text

STEP 3: Respond ONLY with valid JSON (no extra text):
{{
  "operation": "single_operation_name",
  "parameters": [numbers_only, not_text],
  "agent": "math_or_data_or_text",
  "description": "brief explanation"
}}

Examples:
- "How many records?" → {{"operation": "count_records", "parameters": [], "agent": "data"}}
- "Add 50 and 75" → {{"operation": "add", "parameters": [50, 75], "agent": "math"}}
- "Convert 3600 seconds" → {{"operation": "convert_seconds", "parameters": [3600], "agent": "math"}}
- "Count words in this text" → {{"operation": "count_words", "parameters": [], "agent": "text"}}"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.config.get('supervisor', {}).get('model', 'llama-3.1-8b-instant'),
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            response_text = response.choices[0].message.content.strip()
            extraction = json.loads(response_text)
            
            self._log(f"[✅ EXTRACTED] Operation: {extraction.get('operation')} | Agent: {extraction.get('agent')}")
            return extraction
        
        except Exception as e:
            self._log(f"Extraction failed: {e}", "ERROR")
            return {'operation': 'unknown', 'parameters': [], 'agent': 'math', 'description': str(e)}
    
    def _analyze_query(self, query: str) -> Tuple[str, List[str]]:
        """Use LLM to analyze query and determine required agents."""
        self._log(f"[🧠 LLM ANALYSIS] Analyzing query: {query}")
        
        analysis_prompt = f"""Analyze this query and determine which agents (math, data, text) are needed.
        
Query: {query}

Respond with JSON:
{{"agent": "math|data|text|multiple", "reason": "brief explanation"}}

Only respond with valid JSON, nothing else."""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.config.get('supervisor', {}).get('model', 'llama-3.1-8b-instant'),
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            response_text = response.choices[0].message.content.strip()
            analysis = json.loads(response_text)
            agent_type = analysis.get('agent', 'multiple')
            
            # Map agent types to list
            if agent_type == 'math':
                agents_needed = ['math']
            elif agent_type == 'data':
                agents_needed = ['data']
            elif agent_type == 'text':
                agents_needed = ['text']
            else:
                agents_needed = ['math']
            
            self._log(f"[📊 QUERY INTENT] Agent needed: {agents_needed[0]}")
            return query, agents_needed
        
        except Exception as e:
            self._log(f"LLM analysis failed: {e}", "ERROR")
            return query, ['math']
    
    def _generate_response(self, query: str, agent_results: Dict[str, Any], operation: str = "") -> str:
        """Use LLM to generate final response based on agent results."""
        self._log("[✨ RESPONSE GENERATION] Generating final answer")
        
        results_summary = json.dumps(agent_results, indent=2)
        
        # For step-by-step operations, request detailed breakdown
        if operation in ['convert_seconds', 'power', 'divide']:
            response_prompt = f"""Based on the query and agent results, provide a STEP-BY-STEP answer.

Query: {query}
Operation: {operation}

Agent Results:
{results_summary}

IMPORTANT: Show EACH STEP clearly with calculations and results. Do not skip any steps.
Format each step on a new line with clear explanations."""
        else:
            response_prompt = f"""Based on the query and agent results, provide a clear answer.

Query: {query}

Agent Results:
{results_summary}

Provide a concise answer that directly answers the query."""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.config.get('supervisor', {}).get('model', 'llama-3.1-8b-instant'),
                messages=[{"role": "user", "content": response_prompt}],
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            self._log(f"Response generation failed: {e}", "ERROR")
            return f"Unable to generate response: {e}"
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process user query through multi-agent system."""
        print("\n" + "="*70)
        print(f"📝 USER QUERY: {query}")
        print("="*70)
        
        analyzed_query, agents_needed = self._analyze_query(query)
        
        # Extract the actual operation and parameters from the query
        extraction = self._extract_operation(query)
        operation = extraction.get('operation', 'unknown')
        parameters = extraction.get('parameters', [])
        agent_needed = extraction.get('agent', 'math')
        
        print(f"\n[🎯 OPERATION] Tool: {operation}")
        print(f"[🎯 PARAMETERS] Values: {parameters}")
        
        agent_results = {}
        
        # Use extracted agent as primary source
        primary_agent = agent_needed  # From extraction
        
        # Call the appropriate agent with extracted operation
        if primary_agent == 'math':
            self._log(f"[🔧 INVOKING MATH AGENT with operation: {operation}]", "DEBUG")
            if self.math_agent.is_healthy():
                # Call with actual extracted parameters
                if isinstance(parameters, list) and len(parameters) > 0:
                    result = self.math_agent.process(operation, *parameters)
                else:
                    result = self.math_agent.process(operation, query)
                agent_results['math'] = result
            else:
                self._log("Math Agent not healthy", "WARNING")
                agent_results['math'] = {'error': 'Math Agent unavailable'}
        
        elif primary_agent == 'data':
            self._log(f"[🔧 INVOKING DATA AGENT with operation: {operation}]", "DEBUG")
            if self.data_agent.is_healthy():
                # Data operations typically don't need parameters for count_records
                result = self.data_agent.process(operation)
                agent_results['data'] = result
            else:
                self._log("Data Agent not healthy", "WARNING")
                agent_results['data'] = {'error': 'Data Agent unavailable'}
        
        elif primary_agent == 'text':
            self._log(f"[🔧 INVOKING TEXT AGENT with operation: {operation}]", "DEBUG")
            if self.text_agent.is_healthy():
                # Text operations need the query content
                result = self.text_agent.process(operation, query, *parameters if isinstance(parameters, list) else [])
                agent_results['text'] = result
            else:
                self._log("Text Agent not healthy", "WARNING")
                agent_results['text'] = {'error': 'Text Agent unavailable'}
        
        # Generate final response
        final_answer = self._generate_response(query, agent_results, operation)
        
        print("\n" + "="*70)
        print(f"✅ FINAL ANSWER:\n{final_answer}")
        print("="*70 + "\n")
        
        return {
            'query': query,
            'agents_used': agents_needed,
            'agent_results': agent_results,
            'final_answer': final_answer
        }
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all agents."""
        self._log("[🏥 HEALTH CHECK]")
        
        status = {
            'supervisor': True,
            'math_agent': self.math_agent.is_healthy(),
            'data_agent': self.data_agent.is_healthy(),
            'text_agent': self.text_agent.is_healthy(),
        }
        
        for agent, healthy in status.items():
            indicator = "✓" if healthy else "✗"
            print(f"  {indicator} {agent}: {'Healthy' if healthy else 'Unavailable'}")
        
        return status

if __name__ == '__main__':
    import sys
    
    supervisor = SupervisorAgent()
    
    print("\n" + "="*70)
    print("🤖 MULTI-AGENT SUPERVISOR SYSTEM")
    print("="*70)
    
    # Health check
    status = supervisor.health_check()
    
    if not all([status['math_agent'], status['data_agent'], status['text_agent']]):
        print("\n⚠️  WARNING: Some MCP servers are not running!")
        print("   Make sure to run: python run_mcp_servers.py")
        print("   in a separate terminal first!\n")
        sys.exit(1)
    
    print("\n✅ All systems operational! Starting supervisor...\n")
    
    # Interactive loop
    while True:
        try:
            query = input("Query> ").strip()
            if not query:
                continue
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
            
            supervisor.process_query(query)
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
