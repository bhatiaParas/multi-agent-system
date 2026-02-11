# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

## 1. MCP Servers Not Starting

### Problem: "Address already in use" error

```
OSError: [Errno 10048] Only one usage of each socket address (protocol/IP/port) 
          is normally permitted
```

**Cause:** Port is already in use by another process

**Solution:**
```powershell
# Find process using the port
netstat -ano | findstr :8000    # For Math Server

# Kill the process
taskkill /PID <PID> /F

# Or use different ports by editing server startup code
```

---

### Problem: "Permission denied" error

```
PermissionError: [Errno 13] Permission denied
```

**Cause:** Running on restricted port or insufficient permissions

**Solution:**
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as Administrator"

# Try again
python run_mcp_servers.py
```

---

### Problem: Servers start but don't respond

**Cause:** Network configuration, firewall, or localhost resolution

**Solution:**
```powershell
# Test connectivity
curl http://localhost:8000/health

# If fails, try alternate localhost
curl http://127.0.0.1:8000/health

# Check firewall
# Windows Firewall → Allow Python through

# Try binding to all interfaces (edit server code)
# self.host = '0.0.0.0'  # Instead of 'localhost'
```

---

## 2. Supervisor Agent Issues

### Problem: "Connection refused" when starting supervisor

```
ConnectionRefusedError: [Errno 10061] No connection could be made 
                       because the target machine actively refused it
```

**Cause:** MCP servers are not running

**Solution:**
```powershell
# Terminal 1: Start MCP servers FIRST
python run_mcp_servers.py

# Wait for message:
# ✅ ALL MCP SERVERS RUNNING

# Terminal 2: THEN start supervisor
python run_supervisor.py
```

**Important:** Always start MCP servers first in a separate terminal!

---

### Problem: "GROQ_API_KEY not set"

```
Error: GROQ_API_KEY environment variable not set!
```

**Cause:** API key not configured

**Solution:**
```powershell
# Method 1: Using .env file (Recommended)
Copy-Item .env.example .env
# Edit .env and add your API key
$env:GROQ_API_KEY = 'gsk_...'
python run_supervisor.py

# Method 2: Direct environment variable
$env:GROQ_API_KEY = 'your-groq-api-key-here'
python run_supervisor.py

# Method 3: Get API key
# 1. Go to https://console.groq.com
# 2. Sign up (free)
# 3. Create API key
# 4. Copy and paste above
```

---

### Problem: "Some MCP servers are not running"

```
❌ ERROR: Some MCP servers are not running!
  Math Agent: Unavailable
  Data Agent: Unavailable
  Text Agent: Unavailable
```

**Solution:**
```powershell
# Check MCP servers terminal
# Look for message: ✅ ALL MCP SERVERS RUNNING

# If not present, in MCP terminal:
python run_mcp_servers.py

# If already running but shows unavailable:
# 1. Check ports are correct (8000, 8001, 8002)
# 2. Test manually:
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health

# If curl fails, restart servers:
# 1. Kill existing processes
taskkill /PID <PID> /F
# 2. Restart from beginning
```

---

## 3. Query Processing Issues

### Problem: "Timeout waiting for agent response"

```
Timeout: Request timed out after 5 seconds
```

**Cause:** Agent is unresponsive, network issue, or heavy computation

**Solution:**
```powershell
# 1. Check if servers are responding
curl http://localhost:8000/health

# 2. If not responding, restart servers
# 3. Try simpler query
Query> add 1 and 2

# 4. Check system resources
# Task Manager → Performance
# If CPU/Memory high, close other apps

# 5. Increase timeout (edit agent files)
# requests.post(..., timeout=10)  # was 5
```

---

### Problem: LLM returns errors

```
BadRequestError: Error code: 429 - {"error":{"message":"Rate limited"}}
```

**Cause:** Too many requests to Groq API, quota exceeded

**Solution:**
```powershell
# 1. Wait a few minutes (rate limit resets)
# 2. Check Groq status: https://console.groq.com
# 3. Check your API key is valid
# 4. Verify account hasn't hit limits
# 5. Try simpler queries first
```

---

### Problem: "Model not found or access denied"

```
Error: llama-3.1-70b-versatile has been decommissioned
```

**Cause:** Model is no longer available on Groq

**Solution:**
```powershell
# 1. Update supervisor_config.yaml
# Change: model: llama-3.1-8b-instant
# Or try: model: mixtral-8x7b-32768

# 2. Available models (as of last update):
# - llama-3.1-8b-instant (Recommended)
# - mixtral-8x7b-32768
# - Check https://console.groq.com for latest

# 3. Update config
vim config/supervisor_config.yaml
# supervisor:
#   model: llama-3.1-8b-instant
```

---

### Problem: Queries hang indefinitely

**Cause:** Deadlock, infinite loop, or server crash

**Solution:**
```powershell
# 1. Press Ctrl+C to stop
# 2. Check logs for errors
# 3. Restart supervisor
python run_supervisor.py

# 4. If specific query hangs:
# Try simpler query first
# Check server is responding
curl http://localhost:8000/health

# 5. Increase verbosity
# Edit supervisor_agent.py: self.verbose = True
# Restart to see detailed logs
```

---

## 4. Data and Configuration Issues

### Problem: "FileNotFoundError: Config file not found"

```
FileNotFoundError: [Errno 2] No such file or directory: 'config/supervisor_config.yaml'
```

**Cause:** Configuration file is missing or in wrong directory

**Solution:**
```powershell
# 1. Check file exists
dir config/

# 2. Verify you're in right directory
pwd  # Should show multi-agent-system folder

# 3. If file missing, it was created earlier
# Try running from project root:
cd C:\path\to\multi-agent-system
python run_supervisor.py

# 4. If still missing, check project structure:
# multi-agent-system/
# ├── config/
# │   ├── supervisor_config.yaml
# │   └── data.yaml
# ├── run_supervisor.py
# └── ...
```

---

### Problem: "TypeError: list indices must be integers"

```
TypeError: list indices must be integers or slices, not str
```

**Cause:** Wrong argument format for MCP operation

**Solution:**
```powershell
# 1. Check API_REFERENCE.md for correct format
# 2. Ensure args are in correct order
# 3. Example - WRONG:
#   operation: "filter_records"
#   args: ["department", "==", "Engineering"]  # WRONG - missing records!
# 
# 3. Example - CORRECT:
#   operation: "filter_records"
#   args: [records, "department", "==", "Engineering"]  # records FIRST

# 4. If querying directly via API:
curl -X POST http://localhost:8001/operate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "filter_records",
    "args": [RECORDS_HERE, "department", "==", "Engineering"],
    "kwargs": {}
  }'
```

---

### Problem: Empty or unexpected results

**Cause:** Query not specific enough, agent selection wrong, empty dataset

**Solution:**
```powershell
# 1. Try more specific query
# WRONG: "show data"
# RIGHT: "filter Engineering employees"

# 2. Check if data exists
# Edit config/data.yaml to verify sample data

# 3. Test agent directly
python sub_agents/math_agent.py
python sub_agents/data_agent.py
python sub_agents/text_agent.py

# 4. If agent test fails, check MCP server is running
python run_mcp_servers.py

# 5. Use verbose mode for detailed logging
# Edit run_supervisor.py: supervisor.verbose = True
```

---

## 5. Python and Environment Issues

### Problem: "ModuleNotFoundError: No module named 'yaml'"

```
ModuleNotFoundError: No module named 'yaml'
```

**Cause:** PyYAML package not installed

**Solution:**
```powershell
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Or install manually
pip install PyYAML groq requests python-dotenv

# 3. Verify installation
python -c "import yaml; print(yaml.__version__)"

# 4. If using virtual environment, ensure it's activated
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Problem: "Python version mismatch"

```
Error: requires Python 3.8+
```

**Cause:** Python version too old

**Solution:**
```powershell
# 1. Check Python version
python --version

# 2. If too old, install Python 3.12+
# Download from https://www.python.org/downloads/

# 3. Or use scoop/winget
winget install Python.Python.3.12

# 4. Verify installation
python --version  # Should show 3.12.x or higher
```

---

### Problem: "Permission denied" when running Python

```
PermissionError: [Errno 13] Permission denied
```

**Cause:** File permissions, antivirus blocking, or script execution policy

**Solution:**
```powershell
# 1. Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Run PowerShell as Administrator
# Right-click PowerShell → Run as Administrator

# 3. Check antivirus isn't blocking Python
# Temporarily disable antivirus or whitelist Python

# 4. Check file permissions
icacls "C:\path\to\file.py" /grant Users:F
```

---

## 6. Network and Connectivity Issues

### Problem: "Connection timeout" on slow network

```
ConnectionTimeout: Timeout waiting for connection
```

**Cause:** Network latency, slow connection

**Solution:**
```powershell
# 1. Check internet connection
ping google.com

# 2. Increase timeout values (edit agent files)
# requests.post(..., timeout=10)  # was 5

# 3. Try accessing server directly
curl http://localhost:8000/health

# 4. If localhost slow, change to 127.0.0.1
# Edit agent URLs: http://127.0.0.1:8000
```

---

### Problem: Firewall blocking connections

```
No connection could be made
```

**Cause:** Windows Firewall blocking localhost connections

**Solution:**
```powershell
# 1. Open Windows Defender Firewall
# Settings → Privacy & Security → Firewall

# 2. Allow Python through firewall
# Click "Allow an app through firewall"
# Find Python.exe → Allow

# 3. Or temporarily disable (not recommended for security)
# Settings → Privacy & Security → Firewall → Turn off
```

---

## 7. Performance Issues

### Problem: Slow response times

**Cause:** Network latency, LLM processing, agent load

**Solution:**
```powershell
# 1. Check system resources
tasklist /v | findstr python

# 2. Monitor during operation
# Task Manager → Performance tab

# 3. Simplify queries to diagnose
# Complex query: "Analyze all data and summarize"
# Simple query: "average 10 20 30"

# 4. Check Groq API status
# https://console.groq.com

# 5. Reduce model complexity (if acceptable)
# Change to faster model (if available)
```

---

### Problem: High memory usage

**Cause:** Large datasets, memory leak, too many processes

**Solution:**
```powershell
# 1. Check memory usage
Get-Process python | Select-Object Name, WorkingSet

# 2. Limit agent connections
# Edit supervisor to run agents sequentially (not parallel)

# 3. Reduce data size in config/data.yaml

# 4. Restart all servers
# Kill all Python processes
taskkill /F /IM python.exe

# 5. Restart cleanly
python run_mcp_servers.py
python run_supervisor.py
```

---

## 8. Debugging Techniques

### Enable Verbose Logging
```powershell
# Edit supervisor/supervisor_agent.py
# Change: self.verbose = False
# To: self.verbose = True

# Restart supervisor
python run_supervisor.py
```

### Test Individual Components
```powershell
# Test Math Server
python mcp_servers/math_server.py

# In another terminal:
curl http://localhost:8000/health

# Test Math Agent
python sub_agents/math_agent.py

# Test Supervisor
python run_supervisor.py
```

### Check Configuration
```powershell
# View loaded config
python -c "from src.config import Config; c = Config(); import json; print(json.dumps(c.supervisor_config, indent=2))"
```

### Monitor Network Requests
```powershell
# Install netstat watcher (optional)
# Or use built-in logging:
netstat -ano | findstr LISTENING  # See open ports

# Check specific port
netstat -ano | findstr :8000
netstat -ano | findstr :8001
netstat -ano | findstr :8002
```

---

## 9. Getting Help

### Information to gather:
1. **Error message** (full text)
2. **Terminal output** (last 20 lines)
3. **Configuration** (supervisor_config.yaml)
4. **System info** (Python version, OS)
5. **Steps to reproduce**

### Resources:
- **START_HERE.md** - Quick start guide
- **ARCHITECTURE.md** - System design
- **API_REFERENCE.md** - API documentation
- **Groq Console** - https://console.groq.com
- **GitHub Issues** - Project repository

---

## 10. Quick Checklist

Before asking for help, verify:

- [ ] MCP servers running in separate terminal
- [ ] All servers show ✅ healthy status
- [ ] GROQ_API_KEY set in .env
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Running from project root directory
- [ ] Python 3.8+ installed
- [ ] No firewall blocking localhost
- [ ] No other process using ports 8000-8002
- [ ] Tried restarting all components
- [ ] Checked error messages carefully

---

## Summary Table

| Issue | Quick Fix |
|-------|-----------|
| Port in use | `taskkill /F /IM python.exe` |
| No API key | Set `GROQ_API_KEY` in .env |
| Connection refused | Start MCP servers first |
| Server unavailable | `curl http://localhost:8000/health` |
| Timeout | Increase timeout values |
| Missing module | `pip install -r requirements.txt` |
| Slow response | Check internet, check Groq status |
| Data empty | Check config/data.yaml |
| Model error | Update to current model in config |
| Hangs | Press Ctrl+C, restart |

---

**Still stuck? Enable verbose logging and send error output for investigation.**
