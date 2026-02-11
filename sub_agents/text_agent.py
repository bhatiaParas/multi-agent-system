"""Text Agent - Specialized agent for text processing operations."""
import requests
import json
from typing import Any, Dict, List

class TextAgent:
    """Text Agent - Handles text processing and analysis."""
    
    def __init__(self, mcp_url: str = "http://localhost:8002"):
        self.mcp_url = mcp_url
        self.name = "Text Agent"
        self.capabilities = ["count_words", "summarize_text", "extract_keywords", "classify_text"]
    
    def call_mcp(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Call MCP Text Server."""
        try:
            payload = {
                'operation': operation,
                'args': list(args),
                'kwargs': kwargs
            }
            
            response = requests.post(f"{self.mcp_url}/operate", json=payload, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"MCP Error: {response.status_code}"}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _compute_local(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Compute text operation locally."""
        try:
            text = args[0] if args else ""
            
            if operation == 'count_words':
                words = text.split()
                word_count = len(words)
                return {'operation': operation, 'result': word_count}
            
            elif operation == 'summarize_text':
                # Simple summary: first 50% of text
                sentences = text.split('.')
                summary_sentences = sentences[:max(1, len(sentences)//2)]
                summary = '.'.join(summary_sentences).strip()
                return {'operation': operation, 'result': summary}
            
            elif operation == 'extract_keywords':
                # Simple keyword extraction: words > 5 chars
                words = text.split()
                keywords = [w for w in words if len(w) > 5]
                return {'operation': operation, 'result': keywords}
            
            elif operation == 'classify_text':
                # Simple classification based on length
                if len(text) < 50:
                    category = "short"
                elif len(text) < 200:
                    category = "medium"
                else:
                    category = "long"
                return {'operation': operation, 'result': category}
            
            return None
        except Exception as e:
            return None
    
    def process(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Process text operation."""
        print(f"\n[TEXT AGENT] 📝 TOOL CALL: {operation}")
        if args:
            print(f"[TEXT AGENT]    Input: {str(args[0])[:50]}{'...' if len(str(args[0])) > 50 else ''}")
        if kwargs:
            print(f"[TEXT AGENT]    Options: {kwargs}")
        
        # Try local computation first
        local_result = self._compute_local(operation, *args, **kwargs)
        if local_result and 'result' in local_result:
            result = local_result
        else:
            # Fallback to MCP
            result = self.call_mcp(operation, *args, **kwargs)
        
        if 'result' in result:
            print(f"[TEXT AGENT] ✅ RESULT: {result['result']}")
        return result
    
    def is_healthy(self) -> bool:
        """Check if Text Agent is healthy."""
        return True  # Text Agent always healthy (has local fallback)

if __name__ == '__main__':
    agent = TextAgent()
    
    if agent.is_healthy():
        print(f"✓ {agent.name} is healthy")
        result = agent.process("count_words", "Hello world this is amazing")
        print(f"Word count result: {result['result']}")
    else:
        print(f"✗ {agent.name} is not healthy - MCP server not running on {agent.mcp_url}")
