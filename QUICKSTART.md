# ⚡ Quick Start Guide

Get the Multi-Agent System running in **10 minutes**.

---

## 📋 Prerequisites

- Windows 10/11 with PowerShell
- Python 3.8+ (recommended: 3.12)
- Free Groq API key (5 minutes to get)
- Internet connection

---

## 🚀 Installation (5 minutes)

### Step 1: Get Groq API Key (2 min)

1. Go to https://console.groq.com
2. Click "Sign up" (or "Sign in" if already registered)
3. Complete sign-up process (free)
4. Click "API Keys" in left sidebar
5. Click "Create API Key"
6. Copy the key (format: `gsk_...`)
7. **Save it somewhere safe** - You'll need it next

### Step 2: Setup Project (3 min)

```powershell
# 1. Navigate to project folder
cd C:\your\path\to\multi-agent-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\Activate.ps1

# If permission error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed PyYAML, groq, requests, python-dotenv
```

### Step 3: Configure API Key (1 min)

```powershell
# 1. Copy env template
Copy-Item .env.example .env

# 2. Open .env in your editor
notepad .env

# 3. Find this line:
# GROQ_API_KEY=your-groq-api-key-here

# 4. Replace with your API key from Step 1:
GROQ_API_KEY=gsk_your_actual_key_here

# 5. Save file (Ctrl+S, then close)
```

Your `.env` should look like:
```
GROQ_API_KEY=gsk_abcdef123456789...
SUPERVISOR_MODEL=llama-3.1-8b-instant
VERBOSE=true
```

---

## ▶️ Running the System (2 min)

### Terminal 1: Start MCP Servers

```powershell
# Make sure you're in the project folder and venv is activated
# (You should see (venv) at the start of your path)

python run_mcp_servers.py
```

**Wait for this message:**
```
✅ ALL MCP SERVERS RUNNING
  Math Server:  http://localhost:8000
  Data Server:  http://localhost:8001
  Text Server:  http://localhost:8002

⏳ Keep this terminal open and run supervisor in another terminal:
   python run_supervisor.py
```

**✓ Keep this terminal open!**

### Terminal 2: Start Supervisor Agent

Open a **NEW** PowerShell window (don't close Terminal 1!)

```powershell
# Navigate to project
cd C:\your\path\to\multi-agent-system

# Activate virtual environment again
venv\Scripts\Activate.ps1

# Start supervisor
python run_supervisor.py
```

**Wait for this message:**
```
✅ All systems operational!

Query>
```

**✓ You're ready to query!**

---

## 💬 Try Your First Query (1 min)

In Terminal 2 where you see `Query>`, type:

```
Query> What is the average of 10, 20, 30, 40, 50?
```

Press Enter.

**You should see:**
```
======================================================================
📝 USER QUERY: What is the average of 10, 20, 30, 40, 50?
======================================================================

[🧠 LLM ANALYSIS] Analyzing query: What is the average of 10, 20, 30, 40, 50?
[📊 QUERY INTENT] Agents needed: ['math']
[🔧 INVOKING MATH AGENT]
[MATH AGENT] Processing: average
[MATH AGENT] Result: {'operation': 'average', 'result': 30.0, 'status': 'success'}
[✨ RESPONSE GENERATION] Generating final answer

======================================================================
✅ FINAL ANSWER:
The average of these numbers is 30.0.
======================================================================
```

🎉 **Success!** Your multi-agent system is working!

---

## 🧪 Try More Queries

### Math Queries
```
Query> Calculate 5 plus 15
Query> What's the maximum of 100, 50, 75?
Query> Square root of 144
```

### Data Queries
```
Query> Count all employees
Query> Filter data
Query> Show unique departments
```

### Text Queries
```
Query> Count words in this sentence
Query> What is the sentiment of this text?
Query> Summarize the data
```

### Complex Queries
```
Query> Analyze all data and provide summary
Query> What are the top performing employees?
Query> Calculate statistics and summarize
```

---

## 🛑 Stopping the System

When you're done:

### Terminal 2 (Supervisor)
```powershell
exit
# Or press Ctrl+C
```

### Terminal 1 (MCP Servers)
```powershell
# Press Ctrl+C
# Should see: "All servers stopped"
```

Both terminals should close gracefully.

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Terminal 1 shows "✅ ALL MCP SERVERS RUNNING"
- [ ] Terminal 2 shows "✅ All systems operational!"
- [ ] First query returns an answer
- [ ] All three agents show as healthy

---

## 🔧 Troubleshooting Quick Fixes

### "GROQ_API_KEY not set!"
```powershell
# Make sure .env file has your API key
notepad .env

# Check GROQ_API_KEY=gsk_... is set correctly
# Then restart supervisor
```

### "Connection refused"
```powershell
# Make sure MCP servers are running in Terminal 1
# Look for: ✅ ALL MCP SERVERS RUNNING
# If not, Terminal 1 needs to be started first
```

### "Port already in use"
```powershell
# Kill existing Python processes
taskkill /F /IM python.exe

# Restart both terminals
```

### "ModuleNotFoundError"
```powershell
# Make sure venv is activated
venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Agents showing "Unavailable"
```powershell
# Make sure MCP servers running in Terminal 1
# Restart Terminal 2 (supervisor)
```

**For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

---

## 📚 What's Next?

Now that it's working:

1. **Read the docs** - [START_HERE.md](START_HERE.md) for detailed guide
2. **Understand architecture** - [ARCHITECTURE.md](ARCHITECTURE.md) explains how it works
3. **Learn the APIs** - [API_REFERENCE.md](API_REFERENCE.md) for all operations
4. **Add custom agents** - Create your own specialized workers
5. **Deploy** - Run in production environment

---

## 🎯 Common Next Steps

### "I want to understand the system better"
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

### "I want to use the APIs directly"
→ See [API_REFERENCE.md](API_REFERENCE.md)

### "I want to create custom agents"
→ Review [ARCHITECTURE.md](ARCHITECTURE.md) - Extension Points

### "Something's not working"
→ Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### "I want detailed setup instructions"
→ Read [START_HERE.md](START_HERE.md)

---

## 🚀 You're All Set!

Your multi-agent system is ready to:
- ✅ Analyze queries with AI
- ✅ Route to specialized agents
- ✅ Perform mathematical operations
- ✅ Analyze data
- ✅ Process text
- ✅ Generate intelligent responses

**Happy querying!** 🎉

---

## 📞 Need Help?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Enable verbose logging: `VERBOSE=true` in .env
3. Test servers individually: `curl http://localhost:8000/health`
4. Review code comments for detailed explanations
5. Check [API_REFERENCE.md](API_REFERENCE.md) for operation details

---

**Questions? See [INDEX.md](INDEX.md) for full documentation roadmap.**
