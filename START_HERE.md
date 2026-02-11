# 🤖 Multi-Agent System - START HERE

Welcome to the **Multi-Agent AI System**! This is a production-ready supervisor + sub-agents architecture built with Python, Groq LLM, and HTTP-based MCP servers.

## ⚡ Quick Start (5 minutes)

### 1. **Setup**
```powershell
# Clone/extract the project and navigate to it
cd C:\your\path\to\multi-agent-system

# Install dependencies using uv
uv sync
```

### 2. **Configure API Key**
```powershell
# Copy .env.example to .env
Copy-Item .env.example .env

# Edit .env with your Groq API key
# (Get free key from https://console.groq.com)
```

### 3. **Terminal 1: Start MCP Servers**
```powershell
uv run python run_mcp_servers.py
```
You should see:
```
✅ ALL MCP SERVERS RUNNING
  Math Server:  http://localhost:8000
  Data Server:  http://localhost:8001
  Text Server:  http://localhost:8002
```
**Keep this terminal open!**

### 4. **Terminal 2: Start Supervisor Agent**
```powershell
uv run python run_supervisor.py
```
You should see:
```
✅ All systems operational!

Query>
```

### 5. **Query the System**
```
Query> What is the average of 10, 20, 30, 40, 50?
```

The supervisor will:
1. Analyze your query with Groq LLM
2. Route to appropriate agent(s) (Math/Data/Text)
3. Call the corresponding MCP server
4. Generate a final intelligent answer

Press `Ctrl+C` to exit.

---

## 🏗️ Architecture Overview

```
User Query
    ↓
[Supervisor Agent] (Main Coordinator)
    ↓
├─→ [LLM Analysis] (Groq) - Determine which agents needed
├─→ [Agent Router] - Route to appropriate sub-agents
├─→ Route to agents in parallel:
│   ├─→ [Math Agent] ──→ [Math MCP Server:8000]
│   ├─→ [Data Agent] ──→ [Data MCP Server:8001]
│   └─→ [Text Agent] ──→ [Text MCP Server:8002]
├─→ [Result Aggregation] - Combine agent results
└─→ [LLM Response Generation] - Create final answer
    ↓
Final Intelligent Answer to User
```

---

## 📦 System Components

### MCP Servers (Independent HTTP Services)

| Server | Port | Purpose | Operations |
|--------|------|---------|-----------|
| **Math** | 8000 | Mathematical operations | add, subtract, multiply, divide, average, median, max, min, power, sqrt |
| **Data** | 8001 | Data analysis | filter, group, sort, aggregate, count, unique_values |
| **Text** | 8002 | Text processing | summarize, extract, classify, word_count, format, split, join |

Each server:
- Runs independently on localhost
- Exposes HTTP API (`/health`, `/tools`, `/operate`)
- Accepts JSON operations
- Returns structured results

### Sub-Agents (Worker Agents)

| Agent | MCP Server | Role |
|-------|-----------|------|
| **Math Agent** | port 8000 | Calls math operations |
| **Data Agent** | port 8001 | Calls data operations |
| **Text Agent** | port 8002 | Calls text operations |

Each sub-agent:
- Communicates with one MCP server via HTTP
- Receives instructions from Supervisor
- Performs focused operations
- Returns results to Supervisor

### Supervisor Agent (Main Orchestrator)

- **Role**: Main coordinator and decision-maker
- **Responsibilities**:
  - Analyze user queries with Groq LLM
  - Route queries to appropriate sub-agents
  - Coordinate agent execution (sequential or parallel)
  - Aggregate results from multiple agents
  - Generate final intelligent response with LLM
- **Features**:
  - Keyword-based + LLM-based intelligent routing
  - Health checking for all agents
  - Comprehensive logging
  - Error handling and fallbacks

---

## 🚀 Running the System

### Terminal 1: MCP Servers
```powershell
uv run python run_mcp_servers.py
```
- Starts 3 servers in background threads
- Keeps listening for requests
- Runs indefinitely until Ctrl+C

### Terminal 2: Supervisor Agent
```powershell
uv run python run_supervisor.py
```
- Performs health check on all agents
- Enters interactive query loop
- Accepts user input
- Coordinates multi-agent responses

### Test Queries

Try these queries to test different agent capabilities:

#### **Math Agent Queries** (Port 8000)
```
Query> What is the average of 10, 20, 30, 40, 50?
Query> Calculate 15 plus 25 minus 10
Query> What is the square root of 144?
Query> Find the maximum value among 5, 15, 3, 42, 8
Query> What is 12 multiplied by 8?
Query> Calculate the median of these numbers: 2, 7, 1, 9, 5
Query> What is 100 divided by 4?
Query> Calculate 2 to the power of 8
```

#### **Data Agent Queries** (Port 8001)
```
Query> Show me data grouped by department
Query> Filter the dataset where department is Engineering
Query> Count how many unique departments are in the data
Query> Sort the data by salary
Query> Give me aggregate statistics on the dataset
Query> How many records are in the dataset?
```

#### **Text Agent Queries** (Port 8002)
```
Query> Summarize this text: The quick brown fox jumps over the lazy dog
Query> How many words are in this sentence: "The multi-agent system is working perfectly"?
Query> Extract key information from this text: John Smith works at Acme Corp in the Engineering department
Query> Classify this text by sentiment: This system is amazing and very intuitive!
Query> Split this text into words: "Hello world from the multi-agent system"
Query> Format this text: hello world from AI
```

#### **Complex Multi-Agent Queries** (Uses multiple agents together)
```
Query> Calculate the average salary and group employees by department
Query> Summarize the dataset and calculate the average of all numeric values
Query> How many employees in the data and what's their average salary?
Query> Analyze the data and provide word count analysis
Query> Find the maximum and minimum salaries in the dataset
```

#### **Mixed/Open-ended Queries**
```
Query> What can you tell me about the data?
Query> Perform some analysis on the available dataset
Query> Show me what operations are available
Query> What's the total of 50 and 75? Then summarize the word "engineer"
Query> Give me insights from the data and calculate some statistics
```

---

## 📁 Directory Structure

```
multi-agent-system/
├── mcp_servers/           # HTTP-based MCP servers
│   ├── math_server.py     # Math operations server
│   ├── data_server.py     # Data analysis server
│   └── text_server.py     # Text processing server
├── sub_agents/            # Specialized worker agents
│   ├── math_agent.py      # Math agent (uses math MCP)
│   ├── data_agent.py      # Data agent (uses data MCP)
│   └── text_agent.py      # Text agent (uses text MCP)
├── supervisor/            # Main orchestrator
│   └── supervisor_agent.py # Supervisor implementation
├── config/                # Configuration files
│   ├── supervisor_config.yaml # Agent registry & routing
│   └── data.yaml          # Sample dataset
├── src/                   # Shared utilities
│   └── config.py          # Config loader
├── run_mcp_servers.py     # Entry point: Start all MCP servers
├── run_supervisor.py      # Entry point: Start supervisor
├── pyproject.toml         # Python project configuration (uv)
├── uv.lock                # Locked dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

---

## 🔧 Configuration

### supervisor_config.yaml

```yaml
supervisor:
  model: llama-3.1-8b-instant  # LLM model
  temperature: 0.7             # Response creativity
  timeout: 30                  # Request timeout

agents:
  math_agent:
    name: Math Agent
    port: 8000
    url: http://localhost:8000
    description: Mathematical operations
    keywords: [average, calculate, math, number]
  
  data_agent:
    name: Data Agent
    port: 8001
    url: http://localhost:8001
    description: Data analysis
    keywords: [filter, data, group, count]
  
  text_agent:
    name: Text Agent
    port: 8002
    url: http://localhost:8002
    description: Text processing
    keywords: [summarize, text, word, split]
```

### .env

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
SUPERVISOR_MODEL=llama-3.1-8b-instant
VERBOSE=true
```

---

## 🧪 Testing Individual Components

### Test Math Server
```powershell
uv run python mcp_servers/math_server.py

# In another terminal:
uv run python sub_agents/math_agent.py
```

### Test Data Server
```powershell
uv run python mcp_servers/data_server.py

# In another terminal:
uv run python sub_agents/data_agent.py
```

### Test Text Server
```powershell
uv run python mcp_servers/text_server.py

# In another terminal:
uv run python sub_agents/text_agent.py
```

### Test Supervisor
```powershell
uv run python run_supervisor.py
```

---

## 📊 Flow Example

```
User: "What is the average of 10, 20, 30?"

1. [Supervisor] Receives query
2. [LLM] Analyzes: "This is a math question, needs Math Agent"
3. [Routing] Routes to Math Agent
4. [Math Agent] Calls Math MCP Server: average([10, 20, 30])
5. [Math Server] Calculates: average = 20
6. [Result] Returns: {"operation": "average", "result": 20}
7. [LLM] Generates response: "The average of 10, 20, and 30 is 20."
8. [User] Receives final answer
```

---

## 🛠️ Advanced Usage

### Parallel Agent Execution

For queries needing multiple agents, the supervisor can:
- Execute agents in parallel (Fast)
- Execute sequentially (Ordered)
- Create dependency chains

### Custom Agents

To add a new agent:
1. Create MCP server in `mcp_servers/`
2. Create sub-agent wrapper in `sub_agents/`
3. Add to `supervisor_config.yaml`
4. Supervisor automatically routes to it

### Custom Operations

To add operations to MCP servers:
1. Add method to Operations class in server file
2. Method automatically exposed via HTTP API
3. No changes needed to agents or supervisor

---

## 📝 Logging

All components include detailed logging:
- **[🧠 LLM ANALYSIS]** - Query analysis
- **[📊 QUERY INTENT]** - Routing decisions
- **[🔧 INVOKING]** - Agent invocations
- **[✅ RESULT]** - Operation results
- **[✨ RESPONSE]** - Final answer generation

Enable/disable via `VERBOSE=true` in `.env`

---

## 🔍 Troubleshooting

### Problem: "Connection refused" for MCP Server

**Solution:**
```powershell
# Terminal 1
python run_mcp_servers.py

# Wait for "ALL MCP SERVERS RUNNING" message before running Terminal 2
```

### Problem: "GROQ_API_KEY not set"

**Solution:**
```powershell
# Edit .env file with your API key
# Get free key from https://console.groq.com

# Then set it:
$env:GROQ_API_KEY = "your-key-here"
python run_supervisor.py
```

### Problem: Agents showing "Unavailable"

**Solution:**
```powershell
# Make sure MCP servers are running in Terminal 1
# Check that servers are on correct ports (8000, 8001, 8002)
# Restart all servers
```

### Problem: LLM not responding

**Solution:**
- Check internet connection
- Verify GROQ_API_KEY is valid
- Check Groq service status (https://console.groq.com)

---

## 🎯 Next Steps

1. ✅ Run the system successfully
2. ✅ Test with sample queries
3. ✅ Understand the architecture
4. 🔜 Customize agents and operations
5. 🔜 Add new MCP servers
6. 🔜 Deploy to production

---

## 📚 Documentation Files

- **START_HERE.md** (this file) - Quick start guide
- **ARCHITECTURE.md** - Detailed system design
- **API_REFERENCE.md** - MCP server APIs
- **AGENT_GUIDE.md** - Creating custom agents
- **TROUBLESHOOTING.md** - Common issues and solutions

---

## 💡 Key Concepts

### MCP (Model Context Protocol)
- HTTP-based protocol for agent-server communication
- Simple request-response pattern
- Language and framework agnostic

### Supervisor Pattern
- Main agent coordinates sub-agents
- Makes routing decisions
- Aggregates results
- Generates final response

### HTTP-Based Architecture
- Independent, loosely-coupled components
- Easy to scale and deploy
- Simple debugging and monitoring

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## ❓ Support

For issues or questions:
1. Check TROUBLESHOOTING.md
2. Verify all terminals are running
3. Check logs for error messages
4. Review configuration files

---

**Ready to get started? Follow the Quick Start section above!** 🚀
