"""
Configuration manager with JSON/YAML support
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """
    Singleton configuration manager
    
    Usage:
        config = ConfigManager()
        config.load('config.json')
        db_host = config.get('database.host', 'localhost')
        config.set('database.port', 5432)
        config.save()
    """
    
    _instance = None
    _config = {}
    _filepath = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def load(self, filepath: str) -> bool:
        """
        Load configuration from file
        
        Args:
            filepath: Path to config file (JSON)
        
        Returns:
            True if successful
        """
        try:
            if not os.path.exists(filepath):
                print(f'Config file not found: {filepath}')
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
                self._filepath = filepath
                print(f'Config loaded from {filepath}')
                return True
        except Exception as e:
            print(f'Error loading config: {e}')
            return False
    
    def save(self, filepath: Optional[str] = None) -> bool:
        """
        Save configuration to file
        
        Args:
            filepath: Path to save (uses original path if not specified)
        
        Returns:
            True if successful
        """
        try:
            path = filepath or self._filepath
            if not path:
                print('No filepath specified')
                return False
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            print(f'Config saved to {path}')
            return True
        except Exception as e:
            print(f'Error saving config: {e}')
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value by dot-notation key
        
        Args:
            key: Dot-notation key (e.g., 'database.host')
            default: Default value if key not found
        
        Returns:
            Value or default
        
        Example:
            config.get('database.port', 5432)
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value by dot-notation key
        
        Args:
            key: Dot-notation key (e.g., 'database.host')
            value: Value to set
        
        Example:
            config.set('database.port', 5432)
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def delete(self, key: str) -> bool:
        """
        Delete key from config
        
        Args:
            key: Dot-notation key
        
        Returns:
            True if deleted, False if not found
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if isinstance(config, dict) and k in config:
                config = config[k]
            else:
                return False
        
        # Delete the key
        if isinstance(config, dict) and keys[-1] in config:
            del config[keys[-1]]
            return True
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Return entire config as dictionary
        
        Returns:
            Configuration dictionary
        """
        return self._config.copy()
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load config from dictionary
        
        Args:
            data: Configuration dictionary
        """
        self._config = data.copy()
    
    def clear(self) -> None:
        """Clear all configuration"""
        self._config = {}
    
    def print_config(self) -> None:
        """Pretty print current configuration"""
        print(json.dumps(self._config, indent=2, ensure_ascii=False))


# Example usage
if __name__ == '__main__':
    # Create a config manager (singleton)
    config = ConfigManager()
    
    # Load existing config or create new one
    if not config.load('config.json'):
        print('Creating new config...')
        config.from_dict({
            'app_name': 'My App',
            'version': '1.0.0',
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'myapp_db'
            },
            'debug': True
        })
        config.save('config.json')
    
    # Get values
    print('App Name:', config.get('app_name'))
    print('Database Host:', config.get('database.host'))
    print('Database Port:', config.get('database.port'))
    
    # Update values
    config.set('database.port', 5433)
    config.set('new_seting', 'value')
    
    # Print config
    print('\nCurrent Config:')
    config.print_config()
    
    # Save changes
    config.save()
