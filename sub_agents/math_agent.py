"""Math Agent - Specialized agent for mathematical operations."""
import requests
import json
import statistics
from typing import Any, Dict, List

class MathAgent:
    """Math Agent - Handles numerical computations."""
    
    def __init__(self, mcp_url: str = "http://localhost:8000"):
        self.mcp_url = mcp_url
        self.name = "Math Agent"
        self.capabilities = ["add", "subtract", "multiply", "divide", "average", "median", "max", "min", "power", "sqrt"]
    
    def call_mcp(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Call MCP Math Server."""
        try:
            # Some operations expect a list, others expect individual parameters
            if operation in ['add', 'multiply', 'average', 'median', 'max_value', 'min_value', 'sum_numbers']:
                # Convert all args to a single list
                if len(args) == 1 and isinstance(args[0], list):
                    payload_args = args
                else:
                    payload_args = [list(args)]
            else:
                # Operations like subtract, divide, power, sqrt use individual args
                payload_args = list(args)
            
            payload = {
                'operation': operation,
                'args': payload_args,
                'kwargs': kwargs
            }
            
            response = requests.post(f"{self.mcp_url}/operate", json=payload, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"MCP Error: {response.status_code}"}
        
        except Exception as e:
            return {'error': str(e)}
    
    def process(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Process math operation."""
        print(f"\n[MATH AGENT] 🧮 TOOL CALL: {operation}")
        print(f"[MATH AGENT]    Parameters: {args if args else kwargs}")
        result = self.call_mcp(operation, *args, **kwargs)
        
        if 'result' in result:
            print(f"[MATH AGENT] ✅ RESULT: {result['result']}")
            
            # Show step-by-step if available
            if 'steps' in result:
                print(f"\n[MATH AGENT] 📋 STEP-BY-STEP BREAKDOWN:")
                for step in result['steps']:
                    if step.strip():  # Only print non-empty steps
                        print(f"             {step}")
            
            # Show breakdown if available
            if 'breakdown' in result:
                print(f"\n[MATH AGENT] 📊 FINAL RESULT: {result['breakdown']}")
        else:
            # If MCP failed, try local computation as fallback
            local_result = self._compute_local(operation, *args, **kwargs)
            if local_result:
                print(f"[MATH AGENT] ✅ RESULT: {local_result.get('result')}")
                if 'steps' in local_result:
                    print(f"\n[MATH AGENT] 📋 STEP-BY-STEP BREAKDOWN:")
                    for step in local_result['steps']:
                        if step.strip():
                            print(f"             {step}")
                if 'breakdown' in local_result:
                    print(f"\n[MATH AGENT] 📊 FINAL RESULT: {local_result['breakdown']}")
                return local_result
            
        return result
    
    def _compute_local(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Compute operation locally without MCP server."""
        try:
            if operation == 'add' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                return {'operation': operation, 'result': sum(numbers)}
            
            elif operation == 'median' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                return {'operation': operation, 'result': statistics.median(numbers)}
            
            elif operation == 'average' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                return {'operation': operation, 'result': statistics.mean(numbers)}
            
            elif operation == 'multiply' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                result = 1
                for n in numbers:
                    result *= n
                return {'operation': operation, 'result': result}
            
            elif operation == 'max_value' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                return {'operation': operation, 'result': max(numbers)}
            
            elif operation == 'min_value' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                return {'operation': operation, 'result': min(numbers)}
            
            elif operation == 'sum_numbers' and args:
                numbers = args[0] if isinstance(args[0], list) else list(args)
                return {'operation': operation, 'result': sum(numbers)}
            
            elif operation == 'subtract' and len(args) >= 2:
                return {'operation': operation, 'result': args[0] - args[1]}
            
            elif operation == 'divide' and len(args) >= 2:
                if args[1] == 0:
                    raise ValueError("Division by zero")
                return {'operation': operation, 'result': args[0] / args[1]}
            
            elif operation == 'power' and len(args) >= 2:
                return {'operation': operation, 'result': args[0] ** args[1]}
            
            elif operation == 'square_root' and args:
                num = args[0]
                if num < 0:
                    raise ValueError("Cannot take square root of negative number")
                return {'operation': operation, 'result': num ** 0.5}
            
            elif operation == 'convert_seconds' and args:
                total_seconds = int(args[0])
                total_minutes = total_seconds // 60
                remaining_seconds = total_seconds % 60
                hours = total_minutes // 60
                remaining_minutes = total_minutes % 60
                
                return {
                    'operation': operation,
                    'result': f"{hours}h {remaining_minutes}m {remaining_seconds}s",
                    'steps': [
                        'Step 1: Divide total seconds by 60',
                        f'{total_seconds} / 60 = {total_minutes} minutes with remainder {remaining_seconds} seconds',
                        'Step 2: Divide total minutes by 60 to get hours',
                        f'{total_minutes} / 60 = {hours} hours with remainder {remaining_minutes} minutes',
                        'Step 3: Final remaining values',
                        f'Hours: {hours}',
                        f'Minutes: {remaining_minutes}',
                        f'Seconds: {remaining_seconds}'
                    ],
                    'breakdown': {
                        'hours': hours,
                        'minutes': remaining_minutes,
                        'seconds': remaining_seconds
                    }
                }
            
            return None
        except Exception as e:
            print(f"[MATH AGENT] ⚠️ Local computation failed: {e}")
            return None
    
    def is_healthy(self) -> bool:
        """Check if MCP server is healthy."""
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

if __name__ == '__main__':
    agent = MathAgent()
    
    if agent.is_healthy():
        print(f"✓ {agent.name} is healthy")
        # result = agent.process("average", [10, 20, 30, 40, 50])
        # print(f"Average of [10,20,30,40,50]: {result['result']}")
    else:
        print(f"✗ {agent.name} is not healthy - MCP server not running on {agent.mcp_url}")
