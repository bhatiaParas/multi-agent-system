"""Configuration loader for multi-agent system."""
import os
import yaml
from typing import Dict, Any

class Config:
    """Load and manage configuration from YAML files."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.supervisor_config = self._load_yaml("supervisor_config.yaml")
        self.data_config = self._load_yaml("data.yaml")
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML file with environment variable substitution."""
        filepath = os.path.join(self.config_dir, filename)
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                
                # Replace environment variables
                for key, value in os.environ.items():
                    content = content.replace(f"${{{key}}}", value)
                    content = content.replace(f"${key}", value)
                
                return yaml.safe_load(content) or {}
        
        except FileNotFoundError:
            print(f"Warning: Config file not found: {filepath}")
            return {}
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get config value by dot-notation path."""
        keys = path.split('.')
        value = self.supervisor_config or {}
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        
        return value if value is not None else default

if __name__ == '__main__':
    config = Config()
    print("Supervisor Config:", config.supervisor_config)
    print("Data Config:", config.data_config)
