"""Data Agent - Specialized agent for data analysis operations."""
import requests
import json
import os
from typing import Any, Dict, List

class DataAgent:
    """Data Agent - Handles data analysis and filtering."""
    
    def __init__(self, mcp_url: str = "http://localhost:8001"):
        self.mcp_url = mcp_url
        self.name = "Data Agent"
        self.capabilities = ["count_records", "filter_records", "group_records", "sort_records", "aggregate_records"]
        self.dataset = self._load_dataset()
    
    def _load_dataset(self) -> Dict[str, Any]:
        """Load sample dataset from file."""
        dataset_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_dataset.json')
        try:
            if os.path.exists(dataset_path):
                with open(dataset_path, 'r') as f:
                    return json.load(f)
            else:
                return {'records': [], 'metadata': {'total_records': 0}}
        except Exception as e:
            print(f"[DATA AGENT] ⚠️ Could not load dataset: {e}")
            return {'records': [], 'metadata': {'total_records': 0}}
    
    def call_mcp(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Call MCP Data Server."""
        try:
            payload = {
                'operation': operation,
                'args': list(args),
                'kwargs': kwargs
            }
            
            response = requests.post(f"{self.mcp_url}/operate", json=payload, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"MCP Error: {response.status_code}"}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _compute_local(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Compute data operation locally using dataset."""
        try:
            records = self.dataset.get('records', [])
            
            if operation == 'count_records':
                return {'operation': operation, 'result': len(records)}
            
            elif operation == 'filter_records':
                # Filter records by a field matching a value
                # Usage: filter_records(field='department', value='Engineering')
                field = kwargs.get('field') or (args[0] if len(args) > 0 else None)
                value = kwargs.get('value') or (args[1] if len(args) > 1 else None)
                if field and value:
                    filtered = [r for r in records if r.get(field) == value]
                    return {'operation': operation, 'result': filtered}
                return {'operation': operation, 'result': []}
            
            elif operation == 'group_records':
                # Group records by a field
                field = kwargs.get('field') or (args[0] if len(args) > 0 else None)
                if field:
                    grouped = {}
                    for record in records:
                        key = record.get(field, 'Unknown')
                        if key not in grouped:
                            grouped[key] = []
                        grouped[key].append(record)
                    return {'operation': operation, 'result': grouped}
                return {'operation': operation, 'result': {}}
            
            elif operation == 'sort_records':
                # Sort records by a field
                field = kwargs.get('field') or (args[0] if len(args) > 0 else None)
                order = kwargs.get('order', 'asc')
                if field:
                    sorted_records = sorted(records, key=lambda x: x.get(field, ''), reverse=(order.lower() == 'desc'))
                    return {'operation': operation, 'result': sorted_records}
                return {'operation': operation, 'result': records}
            
            elif operation == 'aggregate_records':
                # Aggregate (count, sum, avg) on a field
                agg_type = kwargs.get('type', 'count')  # count, sum, avg
                agg_field = kwargs.get('field')
                if agg_type == 'count':
                    return {'operation': operation, 'result': len(records)}
                elif agg_field and agg_type in ['sum', 'avg']:
                    values = [r.get(agg_field, 0) for r in records if isinstance(r.get(agg_field), (int, float))]
                    if agg_type == 'sum':
                        return {'operation': operation, 'result': sum(values)}
                    else:  # avg
                        return {'operation': operation, 'result': sum(values) / len(values) if values else 0}
            
            return None
        except Exception as e:
            print(f"[DATA AGENT] ⚠️ Local computation failed: {e}")
            return None
    
    def process(self, operation: str, *args, **kwargs) -> Dict[str, Any]:
        """Process data operation."""
        print(f"\n[DATA AGENT] 📊 TOOL CALL: {operation}")
        if kwargs:
            print(f"[DATA AGENT]    Options: {kwargs}")
        
        # Try local computation first
        local_result = self._compute_local(operation, *args, **kwargs)
        if local_result and 'result' in local_result:
            result = local_result
        else:
            # Fallback to MCP
            result = self.call_mcp(operation, *args, **kwargs)
        
        if 'result' in result:
            print(f"[DATA AGENT] ✅ RESULT: Operation succeeded")
            if isinstance(result['result'], (list, dict)):
                if isinstance(result['result'], list):
                    print(f"[DATA AGENT]    Records: {len(result['result'])} items returned")
                elif isinstance(result['result'], dict):
                    print(f"[DATA AGENT]    Items: {len(result['result'])} groups/items")
                else:
                    print(f"[DATA AGENT]    Value: {result['result']}")
            else:
                print(f"[DATA AGENT]    Result: {result['result']}")
        return result
    
    def is_healthy(self) -> bool:
        """Check if Data Agent is healthy (checks if dataset is loaded)."""
        return len(self.dataset.get('records', [])) > 0

if __name__ == '__main__':
    agent = DataAgent()
    
    if agent.is_healthy():
        print(f"✓ {agent.name} is healthy with {len(agent.dataset['records'])} records")
        
        # Test count_records
        result = agent.process("count_records")
        print(f"Total records: {result.get('result')}")
        
        # Test filter_records
        result = agent.process("filter_records", field='department', value='Engineering')
        print(f"Engineering dept records: {len(result.get('result', []))}")
    else:
        print(f"✗ {agent.name} is not healthy - No dataset loaded")

