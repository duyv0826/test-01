"""
Utility functions for common tasks
"""

import os
import json
import csv
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

def read_file(filepath: str, encoding: str = 'utf-8') -> str:
    """
    Read file content with error handling
    
    Args:
        filepath: Path to the file
        encoding: File encoding (default: utf-8)
    
    Returns:
        File content as string
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        print(f'Error reading file {filepath}: {e}')
        return ''

def write_file(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    Write content to file with error handling
    
    Args:
        filepath: Path to the file
        content: Content to write
        encoding: File encoding (default: utf-8)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f'Error writing file {filepath}: {e}')
        return False

def read_json(filepath: str) -> Dict[str, Any]:
    """
    Read JSON file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Dictionary with JSON content
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'Error reading JSON {filepath}: {e}')
        return {}

def write_json(filepath: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """
    Write data to JSON file
    
    Args:
        filepath: Path to JSON file
        data: Data to write
        indent: JSON indentation
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        print(f'Error writing JSON {filepath}: {e}')
        return False

def read_csv(filepath: str) -> List[Dict[str, str]]:
    """
    Read CSV file and return as list of dictionaries
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        List of dictionaries (each row is a dict)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f'Error reading CSV {filepath}: {e}')
        return []

def write_csv(filepath: str, data: List[Dict[str, str]], fieldnames: List[str] = None) -> bool:
    """
    Write data to CSV file
    
    Args:
        filepath: Path to CSV file
        data: List of dictionaries
        fieldnames: List of field names (optional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not fieldnames and data:
            fieldnames = list(data[0].keys())
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f'Error writing CSV {filepath}: {e}')
        return False

def calculate_md5(text: str) -> str:
    """
    Calculate MD5 hash of a string
    
    Args:
        text: Input string
    
    Returns:
        MD5 hash as hex string
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def calculate_sha256(text: str) -> str:
    """
    Calculate SHA256 hash of a string
    
    Args:
        text: Input string
    
    Returns:
        SHA256 hash as hex string
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def get_timestamp(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Get current timestamp as formatted string
    
    Args:
        format_str: Datetime format string
    
    Returns:
        Formatted timestamp
    """
    return datetime.datetime.now().strftime(format_str)

def list_files(directory: str, pattern: str = '*') -> List[str]:
    """
    List all files in directory matching pattern
    
    Args:
        directory: Directory path
        pattern: Glob pattern (e.g., '*.py')
    
    Returns:
        List of file paths
    """
    try:
        path = Path(directory)
        return [str(f) for f in path.glob(pattern) if f.is_file()]
    except Exception as e:
        print(f'Error listing files in {directory}: {e}')
        return []

def ensure_dir(directory: str) -> bool:
    """
    Ensure directory exists, create if not
    
    Args:
        directory: Directory path
    
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f'Error creating directory {directory}: {e}')
        return False

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key (used in recursion)
        sep: Separator between keys
    
    Returns:
        Flattened dictionary
    
    Example:
        {'a': {'b': 1, 'c': 2}} -> {'a.b': 1, 'a.c': 2}
    """
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    
    Example:
        chunk_list([1,2,3,4,5], 2) -> [[1,2], [3,4], [5]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

# Example usage
if __name__ == '__main__':
    # Test the functions
    print('Timestamp:', get_timestamp())
    print('MD5 of hello:', calculate_md5('hello'))
    print('SHA256 of hello:', calculate_sha256('hello'))
    
    # Test file operations
    test_data = {'name': 'test', 'value': 123}
    if write_json('test_output.json', test_data):
        print('JSON written successfully')
        read_data = read_json('test_output.json')
        print('JSON read back:', read_data)
