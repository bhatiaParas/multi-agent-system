"""Entry point to run the supervisor agent."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Check if GROQ_API_KEY is set
if not os.environ.get('GROQ_API_KEY'):
    print("❌ Error: GROQ_API_KEY environment variable not set!")
    print("   Set it in .env file or run: $env:GROQ_API_KEY='your-key'")
    sys.exit(1)

from supervisor.supervisor_agent import SupervisorAgent

def main():
    """Start the supervisor agent."""
    try:
        supervisor = SupervisorAgent()
        
        print("\n" + "="*70)
        print("🤖 MULTI-AGENT SUPERVISOR STARTED")
        print("="*70)
        
        # Health check
        status = supervisor.health_check()
        
        if not all([status['math_agent'], status['data_agent'], status['text_agent']]):
            print("\n❌ ERROR: Some MCP servers are not running!")
            print("\n   SOLUTION:")
            print("   1. Open a NEW terminal window")
            print("   2. Run: python run_mcp_servers.py")
            print("   3. Wait for 'ALL MCP SERVERS RUNNING' message")
            print("   4. Come back to this terminal and try again")
            sys.exit(1)
        
        print("\n✅ All systems operational!\n")
        print("="*70)
        print("📝 USAGE:")
        print("  - Type your query and press Enter")
        print("  - Type 'exit' to quit")
        print("="*70 + "\n")
        
        # Interactive loop
        supervisor.verbose = True
        while True:
            try:
                query = input("Query> ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['exit', 'quit', 'q', 'bye']:
                    print("\n👋 Goodbye!\n")
                    break
                
                supervisor.process_query(query)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
    
    except Exception as e:
        print(f"\n❌ Failed to start supervisor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
