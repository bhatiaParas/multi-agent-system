"""Text MCP Server - Provides text processing operations (Port 8002)."""
import json
from typing import List, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class TextOperations:
    """Text operation handlers."""
    
    @staticmethod
    def summarize(text: str, max_length: int = 100) -> str:
        """Summarize text."""
        words = text.split()
        if len(words) <= max_length:
            return text
        
        summary = ' '.join(words[:max_length])
        if len(text) > len(summary):
            summary += "..."
        return summary
    
    @staticmethod
    def extract_entities(text: str, entity_type: str) -> List[str]:
        """Extract entities from text."""
        entities = []
        
        if entity_type == "numbers":
            import re
            entities = re.findall(r'\d+', text)
        elif entity_type == "words":
            entities = text.split()
        elif entity_type == "uppercase":
            entities = [word for word in text.split() if word.isupper()]
        
        return entities
    
    @staticmethod
    def classify(text: str) -> Dict[str, Any]:
        """Classify text."""
        words = text.lower().split()
        
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
        negative_words = ['bad', 'poor', 'terrible', 'awful', 'horrible']
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        
        if pos_count > neg_count:
            sentiment = "positive"
        elif neg_count > pos_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            'sentiment': sentiment,
            'confidence': max(pos_count, neg_count) / (pos_count + neg_count + 1),
            'positive_words': pos_count,
            'negative_words': neg_count
        }
    
    @staticmethod
    def word_count(text: str) -> Dict[str, Any]:
        """Count words and characters."""
        words = text.split()
        return {
            'word_count': len(words),
            'character_count': len(text),
            'unique_words': len(set(w.lower() for w in words)),
            'average_word_length': len(text) / len(words) if words else 0
        }
    
    @staticmethod
    def format_text(text: str, format_type: str) -> str:
        """Format text."""
        if format_type == "uppercase":
            return text.upper()
        elif format_type == "lowercase":
            return text.lower()
        elif format_type == "title":
            return text.title()
        elif format_type == "capitalize":
            return text.capitalize()
        
        return text
    
    @staticmethod
    def split_text(text: str, delimiter: str = " ") -> List[str]:
        """Split text."""
        return text.split(delimiter)
    
    @staticmethod
    def join_text(texts: List[str], delimiter: str = " ") -> str:
        """Join texts."""
        return delimiter.join(texts)
    
    @staticmethod
    def remove_duplicates(texts: List[str]) -> List[str]:
        """Remove duplicate strings."""
        return list(dict.fromkeys(texts))

class TextHandler(BaseHTTPRequestHandler):
    """HTTP handler for text operations."""
    
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
            print(f"  [⚙️ TEXT TOOL] {operation}({args}, {kwargs})")
            
            text_ops = TextOperations()
            if not hasattr(text_ops, operation):
                raise ValueError(f"Unknown operation: {operation}")
            
            func = getattr(text_ops, operation)
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
            self.wfile.write(json.dumps({'status': 'healthy', 'service': 'text'}).encode('utf-8'))
        
        elif self.path == '/tools':
            tools = {
                'tools': [
                    {'name': 'summarize', 'description': 'Summarize text'},
                    {'name': 'extract_entities', 'description': 'Extract entities'},
                    {'name': 'classify', 'description': 'Classify text sentiment'},
                    {'name': 'word_count', 'description': 'Count words'},
                    {'name': 'format_text', 'description': 'Format text'},
                    {'name': 'split_text', 'description': 'Split text'},
                    {'name': 'join_text', 'description': 'Join text'},
                    {'name': 'remove_duplicates', 'description': 'Remove duplicates'},
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

class TextMCPServer:
    """Text MCP Server."""
    
    def __init__(self, host: str = 'localhost', port: int = 8002):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the server."""
        self.server = HTTPServer((self.host, self.port), TextHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[TEXT MCP] Started on http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            print("[TEXT MCP] Stopped")

if __name__ == '__main__':
    server = TextMCPServer()
    server.start()
    print("Text MCP Server running. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()
