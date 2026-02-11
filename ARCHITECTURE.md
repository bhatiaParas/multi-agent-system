# 🏗️ Multi-Agent System Architecture

## System Overview

The Multi-Agent System implements a **Supervisor + Sub-Agents** pattern with HTTP-based MCP (Model Context Protocol) servers.

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                                                                   │
│                   Interactive Query Terminal                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SUPERVISOR AGENT                              │
│                                                                   │
│  1. Analyze query with Groq LLM                                  │
│  2. Determine required agents (Math/Data/Text)                   │
│  3. Route to specialized sub-agents                              │
│  4. Aggregate results from multiple agents                       │
│  5. Generate final response with LLM                             │
└─┬──────────────────────┬──────────────────────┬─────────────────┘
  │                      │                      │
  ▼                      ▼                      ▼
┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  MATH AGENT     │ │  DATA AGENT     │ │  TEXT AGENT      │
│                 │ │                 │ │                  │
│ • Arithmetic    │ │ • Filtering     │ │ • Summarization  │
│ • Statistics    │ │ • Grouping      │ │ • Classification │
│ • Calculations  │ │ • Aggregation   │ │ • Word count     │
└────────┬────────┘ └────────┬────────┘ └─────────┬────────┘
         │                   │                    │
         ▼                   ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                    MCP SERVERS (HTTP)                             │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │ Math Server :8000│  │ Data Server :8001│  │Text Server:8002│ │
│  │                  │  │                  │  │                │ │
│  │ • GET /health    │  │ • GET /health    │  │• GET /health   │ │
│  │ • GET /tools     │  │ • GET /tools     │  │• GET /tools    │ │
│  │ • POST /operate  │  │ • POST /operate  │  │• POST /operate │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
│                                                                   │
│  Each server:                                                     │
│  • Independent HTTP service                                      │
│  • JSON request-response protocol                                │
│  • Stateless operations                                          │
│  • Easy to scale and deploy                                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Supervisor Agent (`supervisor/supervisor_agent.py`)

**Primary Responsibilities:**
- Query analysis using Groq LLM
- Agent routing decisions
- Result aggregation
- Final response generation

**Key Methods:**
```python
process_query(query)        # Main entry point
_analyze_query(query)       # LLM analysis for agent selection
_generate_response(...)     # LLM response synthesis
health_check()              # Agent health verification
```

**Flow:**
```
receive_query()
    ↓
analyze_with_LLM()
    ↓
determine_agents()
    ↓
invoke_agents_in_parallel()
    or_invoke_sequentially()
    ↓
aggregate_results()
    ↓
generate_response_with_LLM()
    ↓
return_final_answer()
```

### 2. MCP Servers

#### Math Server (Port 8000)
```python
Operations:
  • add(numbers: List[float])
  • subtract(a: float, b: float)
  • multiply(numbers: List[float])
  • divide(a: float, b: float)
  • average(numbers: List[float])
  • median(numbers: List[float])
  • max_value(numbers: List[float])
  • min_value(numbers: List[float])
  • power(base: float, exponent: float)
  • square_root(number: float)

HTTP API:
  POST /operate
    {
      "operation": "average",
      "args": [[10, 20, 30, 40, 50]],
      "kwargs": {}
    }
  
  Response:
    {
      "operation": "average",
      "result": 30.0,
      "status": "success"
    }
```

#### Data Server (Port 8001)
```python
Operations:
  • filter_records(records, field, operator, value)
  • group_by(records, field)
  • sort_records(records, field, descending)
  • aggregate(records, field, operation)
  • select_fields(records, fields)
  • count_records(records)
  • unique_values(records, field)

HTTP API:
  POST /operate
    {
      "operation": "filter_records",
      "args": [records, "department", "==", "Engineering"],
      "kwargs": {}
    }
  
  Response:
    {
      "operation": "filter_records",
      "result": [{...}, {...}],
      "status": "success"
    }
```

#### Text Server (Port 8002)
```python
Operations:
  • summarize(text, max_length)
  • extract_entities(text, entity_type)
  • classify(text)
  • word_count(text)
  • format_text(text, format_type)
  • split_text(text, delimiter)
  • join_text(texts, delimiter)
  • remove_duplicates(texts)

HTTP API:
  POST /operate
    {
      "operation": "word_count",
      "args": ["Hello world this is a test"],
      "kwargs": {}
    }
  
  Response:
    {
      "operation": "word_count",
      "result": {
        "word_count": 6,
        "character_count": 36,
        "unique_words": 6,
        "average_word_length": 5.2
      },
      "status": "success"
    }
```

### 3. Sub-Agents

#### Common Pattern
```python
class SomeAgent:
    def __init__(self, mcp_url="http://localhost:PORT"):
        self.mcp_url = mcp_url
        self.name = "Agent Name"
        self.capabilities = ["op1", "op2", ...]
    
    def call_mcp(self, operation, *args, **kwargs):
        # HTTP POST to /operate endpoint
        # Returns JSON response
    
    def process(self, operation, *args, **kwargs):
        # Wrapper with logging
        # Calls call_mcp()
    
    def is_healthy(self):
        # GET /health check
```

---

## Data Flow Detailed

### Step 1: Query Reception
```
User Input: "What is the average of 10, 20, 30?"
         ↓
Supervisor receives query
```

### Step 2: LLM Query Analysis
```
Supervisor sends to Groq LLM:
"Analyze: What is the average of 10, 20, 30?"

Prompt includes:
  • Query text
  • Agent options (math, data, text, multiple)
  • Format instructions

LLM Response:
{
  "agent": "math",
  "reason": "Arithmetic operation on numbers"
}
```

### Step 3: Agent Routing
```
Supervisor determines:
  agents_needed = ["math"]

Routes query to:
  → MathAgent (not DataAgent, not TextAgent)
```

### Step 4: Agent Execution
```
MathAgent.process("average", [10, 20, 30])
         ↓
MathAgent.call_mcp("average", [10, 20, 30])
         ↓
HTTP POST to http://localhost:8000/operate
{
  "operation": "average",
  "args": [[10, 20, 30]],
  "kwargs": {}
}
         ↓
Math Server processes:
  sum([10, 20, 30]) / 3 = 20.0
         ↓
Returns JSON:
{
  "operation": "average",
  "result": 20.0,
  "status": "success"
}
```

### Step 5: Result Aggregation
```
Supervisor collects:
{
  "math": {
    "operation": "average",
    "result": 20.0,
    "status": "success"
  }
}
```

### Step 6: Response Generation
```
Supervisor sends to Groq LLM:
  Query: "What is the average of 10, 20, 30?"
  Agent Results: {math result = 20.0}
  Instruction: "Generate a clear answer"

LLM Response:
"The average of 10, 20, and 30 is 20.0"
```

### Step 7: Response Delivery
```
Final Answer returned to User:
"The average of 10, 20, and 30 is 20.0"
```

---

## Multi-Agent Query Flow

### Query: "Find engineering employees and count them"

```
Step 1: Query Analysis
  LLM determines: agents_needed = ["data"]
  (Not multiple agents needed in this case)

Step 2: Routing
  → DataAgent

Step 3: Execution
  DataAgent.process("filter_records", 
    records, "department", "==", "Engineering")
  
  HTTP POST to localhost:8001/operate

Step 4: Result
  {
    "count": 3,
    "records": [
      {"name": "Alice", "department": "Engineering"},
      {"name": "Carol", "department": "Engineering"},
      {"name": "David", "department": "Engineering"}
    ]
  }

Step 5: Response
  "There are 3 employees in the Engineering department."
```

---

## Configuration Flow

```
.env (Environment Variables)
  ↓
GROQ_API_KEY, SUPERVISOR_MODEL
  ↓
supervisor_config.yaml
  ↓
Agent Registry:
  • math_agent (port 8000, keywords)
  • data_agent (port 8001, keywords)
  • text_agent (port 8002, keywords)
  ↓
Supervisor loads config
  ↓
Routes based on keywords + LLM analysis
```

---

## Error Handling

### Agent Unavailability
```
supervisor.health_check()
  ↓
If agent not responding:
  ↓
Log warning
Return error in agent_results
  ↓
LLM generates response acknowledging limitation
  ↓
User sees: "Math Agent is currently unavailable"
```

### MCP Server Error
```
Agent calls MCP server
  ↓
Server returns 400 Bad Request
  ↓
Agent catches exception
  ↓
Returns: {"error": "error message"}
  ↓
Supervisor logs error
  ↓
LLM generates response with error context
```

### LLM Failure
```
Groq API timeout/error
  ↓
Fallback analysis
  ↓
Route to all agents or default agent
  ↓
Aggregate results
  ↓
Return results without LLM formatting
```

---

## Scalability Considerations

### Adding New MCP Server
1. Create server file in `mcp_servers/`
2. Implement Operations class
3. Create HTTP handler
4. Choose unique port
5. Update supervisor config

### Adding New Sub-Agent
1. Create agent file in `sub_agents/`
2. Implement agent class
3. Point to MCP server
4. Register in supervisor config

### Parallel Execution
- Supervisor can invoke multiple agents simultaneously
- Uses Python `threading` or `asyncio`
- Aggregates results when all complete

### Load Balancing
- Multiple instances of same MCP server
- Supervisor routes to different ports
- Implement basic round-robin

---

## Security Considerations

### API Key Protection
- Store in `.env` file (not in git)
- Load via environment variables
- Never log API keys

### Input Validation
- MCP servers validate operation names
- JSON validation for payloads
- Type checking for arguments

### Network Security
- HTTP servers on localhost only by default
- Can be restricted to specific IPs
- Consider HTTPS for remote deployment

---

## Performance Characteristics

| Component | Latency | Throughput | Notes |
|-----------|---------|-----------|-------|
| LLM Query | 200-500ms | 1 query/sec | Groq API |
| Math Op | <10ms | 1000+ ops/sec | Local HTTP |
| Data Op | 10-50ms | 100+ ops/sec | Depends on dataset |
| Text Op | 20-100ms | 100+ ops/sec | Depends on text |
| Supervisor | 500-1000ms | 1 query/sec | Total end-to-end |

---

## Extension Points

### Custom Agents
```python
class CustomAgent:
    def __init__(self, mcp_url):
        # Initialize
    
    def call_mcp(self, operation, *args, **kwargs):
        # HTTP communication
    
    def process(self, operation, *args, **kwargs):
        # Business logic
```

### Custom MCP Operations
```python
class Operations:
    @staticmethod
    def custom_operation(arg1, arg2, ...):
        # Implementation
        return result
```

### Custom Routing Logic
```python
def _analyze_query(self, query):
    # Custom analysis instead of LLM
    # Return agent list based on rules
```

---

## Monitoring and Debugging

### Logging Levels
- INFO: Normal operations
- DEBUG: Detailed agent operations
- WARNING: Recoverable issues
- ERROR: System failures

### Health Check
```bash
curl http://localhost:8000/health   # Math
curl http://localhost:8001/health   # Data
curl http://localhost:8002/health   # Text
```

### Tools Discovery
```bash
curl http://localhost:8000/tools    # Available operations
```

---

**This architecture provides flexibility, scalability, and clear separation of concerns!**
