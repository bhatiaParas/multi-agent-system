"""Math MCP Server - Provides mathematical operations (Port 8000)."""
import json
import statistics
from typing import List, Union, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class MathOperations:
    """Math operation handlers."""
    
    @staticmethod
    def add(numbers: List[Union[int, float]]) -> float:
        return sum(numbers)
    
    @staticmethod
    def subtract(a: Union[int, float], b: Union[int, float]) -> float:
        return a - b
    
    @staticmethod
    def multiply(numbers: List[Union[int, float]]) -> float:
        result = 1
        for n in numbers:
            result *= n
        return result
    
    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    @staticmethod
    def average(numbers: List[Union[int, float]]) -> float:
        if not numbers:
            raise ValueError("Cannot average empty list")
        return statistics.mean(numbers)
    
    @staticmethod
    def median(numbers: List[Union[int, float]]) -> float:
        if not numbers:
            raise ValueError("Cannot find median of empty list")
        return statistics.median(numbers)
    
    @staticmethod
    def sum_numbers(numbers: List[Union[int, float]]) -> float:
        return sum(numbers)
    
    @staticmethod
    def max_value(numbers: List[Union[int, float]]) -> Union[int, float]:
        if not numbers:
            raise ValueError("Cannot find max of empty list")
        return max(numbers)
    
    @staticmethod
    def min_value(numbers: List[Union[int, float]]) -> Union[int, float]:
        if not numbers:
            raise ValueError("Cannot find min of empty list")
        return min(numbers)
    
    @staticmethod
    def power(base: Union[int, float], exponent: Union[int, float]) -> float:
        return base ** exponent
    
    @staticmethod
    def square_root(number: Union[int, float]) -> float:
        if number < 0:
            raise ValueError("Cannot take square root of negative number")
        return number ** 0.5
    
    @staticmethod
    def convert_seconds(total_seconds: int) -> Dict[str, Any]:
        """Convert seconds to hours, minutes, seconds (step-by-step)."""
        
        # Step 1: Divide by 60 to get minutes
        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60
        
        # Step 2: Divide minutes by 60 to get hours
        hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        
        # Step 3: Final remaining seconds
        
        return {
            'total_seconds': total_seconds,
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
            'result': f'{hours}h {remaining_minutes}m {remaining_seconds}s',
            'breakdown': {
                'hours': hours,
                'minutes': remaining_minutes,
                'seconds': remaining_seconds
            }
        }

class MathHandler(BaseHTTPRequestHandler):
    """HTTP handler for math operations."""
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            if self.path != '/operate':
                self.send_error(404)
                return
            
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            request = json.loads(body.decode('utf-8'))
            
            operation = request.get('operation')
            args = request.get('args', [])
            kwargs = request.get('kwargs', {})
            
            # Log tool call
            print(f"  [⚙️ MATH TOOL] {operation}({args}, {kwargs})")
            
            math_ops = MathOperations()
            if not hasattr(math_ops, operation):
                raise ValueError(f"Unknown operation: {operation}")
            
            func = getattr(math_ops, operation)
            result = func(*args, **kwargs)
            print(f"  [✅ RESULT] {operation} = {result}")
            
            response = {
                'operation': operation,
                'result': result,
                'status': 'success'
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        except Exception as e:
            import traceback
            print(f"  [❌ ERROR] {str(e)}")
            print(f"  [TRACEBACK] {traceback.format_exc()}")
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'math'}).encode('utf-8'))
        
        elif self.path == '/tools':
            tools = {
                'tools': [
                    {'name': 'add', 'description': 'Add numbers'},
                    {'name': 'subtract', 'description': 'Subtract'},
                    {'name': 'multiply', 'description': 'Multiply numbers'},
                    {'name': 'divide', 'description': 'Divide'},
                    {'name': 'average', 'description': 'Calculate average'},
                    {'name': 'median', 'description': 'Calculate median'},
                    {'name': 'max_value', 'description': 'Find maximum'},
                    {'name': 'min_value', 'description': 'Find minimum'},
                    {'name': 'power', 'description': 'Power operation'},
                    {'name': 'square_root', 'description': 'Square root'},
                    {'name': 'convert_seconds', 'description': 'Convert seconds to hours, minutes, seconds'},
                ]
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tools).encode('utf-8'))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

class MathMCPServer:
    """Math MCP Server."""
    
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the server."""
        self.server = HTTPServer((self.host, self.port), MathHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[MATH MCP] Started on http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            print("[MATH MCP] Stopped")

if __name__ == '__main__':
    server = MathMCPServer()
    server.start()
    print("Math MCP Server running. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()
