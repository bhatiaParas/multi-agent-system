"""Entry point to run all MCP servers."""
import sys
import time
from mcp_servers.math_server import MathMCPServer
from mcp_servers.data_server import DataMCPServer
from mcp_servers.text_server import TextMCPServer

def main():
    """Start all MCP servers."""
    print("\n" + "="*70)
    print("🚀 STARTING MCP SERVERS")
    print("="*70 + "\n")
    
    # Create servers
    math_server = MathMCPServer(port=8000)
    data_server = DataMCPServer(port=8001)
    text_server = TextMCPServer(port=8002)
    
    # Start servers
    try:
        math_server.start()
        time.sleep(0.5)
        
        data_server.start()
        time.sleep(0.5)
        
        text_server.start()
        time.sleep(0.5)
        
        print("\n" + "="*70)
        print("✅ ALL MCP SERVERS RUNNING")
        print("="*70)
        print("  Math Server:  http://localhost:8000")
        print("  Data Server:  http://localhost:8001")
        print("  Text Server:  http://localhost:8002")
        print("\n⏳ Keep this terminal open and run supervisor in another terminal:")
        print("   python run_supervisor.py")
        print("\n  Press Ctrl+C to stop all servers")
        print("="*70 + "\n")
        
        # Keep servers running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 SHUTTING DOWN MCP SERVERS")
        print("="*70)
        math_server.stop()
        data_server.stop()
        text_server.stop()
        print("✅ All servers stopped\n")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
