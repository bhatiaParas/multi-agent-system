"""Data MCP Server - Provides data analysis operations (Port 8001)."""
import json
from typing import List, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class DataOperations:
    """Data operation handlers."""
    
    @staticmethod
    def filter_records(records: List[Dict], field: str, operator: str, value: Any) -> List[Dict]:
        """Filter records based on condition."""
        result = []
        for record in records:
            if field not in record:
                continue
            
            record_value = record[field]
            
            if operator == "==":
                if record_value == value:
                    result.append(record)
            elif operator == ">":
                if record_value > value:
                    result.append(record)
            elif operator == "<":
                if record_value < value:
                    result.append(record)
            elif operator == ">=":
                if record_value >= value:
                    result.append(record)
            elif operator == "<=":
                if record_value <= value:
                    result.append(record)
            elif operator == "in":
                if record_value in value:
                    result.append(record)
        
        return result
    
    @staticmethod
    def group_by(records: List[Dict], field: str) -> Dict[str, List[Dict]]:
        """Group records by field."""
        groups = {}
        for record in records:
            if field in record:
                key = str(record[field])
                if key not in groups:
                    groups[key] = []
                groups[key].append(record)
        return groups
    
    @staticmethod
    def sort_records(records: List[Dict], field: str, descending: bool = False) -> List[Dict]:
        """Sort records by field."""
        return sorted(records, key=lambda x: x.get(field, 0), reverse=descending)
    
    @staticmethod
    def aggregate(records: List[Dict], field: str, operation: str) -> Any:
        """Aggregate field values."""
        values = [r.get(field, 0) for r in records if field in r]
        
        if not values:
            return None
        
        if operation == "sum":
            return sum(values)
        elif operation == "count":
            return len(values)
        elif operation == "average":
            return sum(values) / len(values)
        elif operation == "max":
            return max(values)
        elif operation == "min":
            return min(values)
        
        return None
    
    @staticmethod
    def select_fields(records: List[Dict], fields: List[str]) -> List[Dict]:
        """Select specific fields from records."""
        result = []
        for record in records:
            selected = {f: record.get(f) for f in fields if f in record}
            result.append(selected)
        return result
    
    @staticmethod
    def count_records(records: List[Dict]) -> int:
        """Count records."""
        return len(records)
    
    @staticmethod
    def unique_values(records: List[Dict], field: str) -> List[Any]:
        """Get unique values for a field."""
        values = set()
        for record in records:
            if field in record:
                values.add(str(record[field]))
        return sorted(list(values))

class DataHandler(BaseHTTPRequestHandler):
    """HTTP handler for data operations."""
    
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
            print(f"  [⚙️ DATA TOOL] {operation}({args}, {kwargs})")
            
            data_ops = DataOperations()
            if not hasattr(data_ops, operation):
                raise ValueError(f"Unknown operation: {operation}")
            
            func = getattr(data_ops, operation)
            result = func(*args, **kwargs)
            print(f"  [✅ RESULT] {operation} executed")
            
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
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'data'}).encode('utf-8'))
        
        elif self.path == '/tools':
            tools = {
                'tools': [
                    {'name': 'filter_records', 'description': 'Filter records'},
                    {'name': 'group_by', 'description': 'Group records'},
                    {'name': 'sort_records', 'description': 'Sort records'},
                    {'name': 'aggregate', 'description': 'Aggregate data'},
                    {'name': 'select_fields', 'description': 'Select fields'},
                    {'name': 'count_records', 'description': 'Count records'},
                    {'name': 'unique_values', 'description': 'Get unique values'},
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

class DataMCPServer:
    """Data MCP Server."""
    
    def __init__(self, host: str = 'localhost', port: int = 8001):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the server."""
        self.server = HTTPServer((self.host, self.port), DataHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[DATA MCP] Started on http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            print("[DATA MCP] Stopped")

if __name__ == '__main__':
    server = DataMCPServer()
    server.start()
    print("Data MCP Server running. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()
