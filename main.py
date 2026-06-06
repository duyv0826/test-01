"""
Main application entry point with practical examples
"""

import os
import sys
from datetime import datetime

# Import our utility modules
from utils import (
    read_file, write_file, read_json, write_json,
    read_csv, write_csv, calculate_md5, calculate_sha256,
    get_timestamp, list_files, ensure_dir, flatten_dict, chunk_list
)
from config_manager import ConfigManager
from logger import Logger, get_logger

def example_file_operations():
    """Example: File operations"""
    print('\n=== File Operations ===')
    
    # Write a file
    write_file('output/hello.txt', 'Hello, World!\nThis is a test file.')
    
    # Read the file
    content = read_file('output/hello.txt')
    print(f'File content: {content}')
    
    # Get file MD5
    md5_hash = calculate_md5(content)
    print(f'MD5: {md5_hash}')

def example_json_operations():
    """Example: JSON operations"""
    print('\n=== JSON Operations ===')
    
    # Create sample data
    data = {
        'app_name': 'Test App',
        'version': '1.0.0',
        'users': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ],
        'settings': {
            'debug': True,
            'max_connections': 100
        }
    }
    
    # Write JSON
    write_json('output/data.json', data)
    
    # Read JSON
    loaded_data = read_json('output/data.json')
    print(f'Loaded JSON: {loaded_data}')
    
    # Flatten nested dict
    flat = flatten_dict(loaded_data)
    print(f'\nFlattened dict:')
    for key, value in flat.items():
        print(f'  {key}: {value}')

def example_csv_operations():
    """Example: CSV operations"""
    print('\n=== CSV Operations ===')
    
    # Create sample data
    data = [
        {'id': '1', 'name': 'Alice', 'age': '30', 'city': 'New York'},
        {'id': '2', 'name': 'Bob', 'age': '25', 'city': 'London'},
        {'id': '3', 'name': 'Charlie', 'age': '35', 'city': 'Tokyo'}
    ]
    
    # Write CSV
    write_csv('output/data.csv', data)
    
    # Read CSV
    loaded_data = read_csv('output/data.csv')
    print(f'Loaded CSV rows: {len(loaded_data)}')
    for row in loaded_data:
        print(f'  {row["name"]} ({row["age"]}) - {row["city"]}')

def example_config_management():
    """Example: Configuration management"""
    print('\n=== Config Management ===')
    
    # Create config manager (singleton)
    config = ConfigManager()
    
    # Load or create config
    if not config.load('output/config.json'):
        print('Creating new config...')
        config.from_dict({
            'app': {
                'name': 'My App',
                'version': '1.0.0'
            },
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'myapp_db'
            },
            'features': {
                'enable_cache': True,
                'max_users': 1000
            }
        })
        config.save('output/config.json')
    
    # Get values
    print(f'App Name: {config.get("app.name")}')
    print(f'Database Host: {config.get("database.host")}')
    print(f'Database Port: {config.get("database.port")}')
    
    # Update config
    config.set('database.port', 5433)
    config.set('features', True)
    config.save()
    print('\nConfig updated and saved.')

def example_logging():
    """Example: Logging"""
    print('\n=== Logging ===')
    
    # Create logger
    log = get_logger('my_app')
    
    # Log messages
    log.info('Application started')
    log.debug('Debug information')
    log.warning('This is a warning')
    
    # Log with exception
    try:
        result = 10 / 0
    except Exception as e:
        log.error(f'Exception occurred: {e}', exc_info=True)
    
    print('\nCheck logs/ directory for log files.')

def example_utilities():
    """Example: Other utilities"""
    print('\n=== Other Utilities ===')
    
    # Get timestamp
    print(f'Current timestamp: {get_timestamp()}')
    
    # List files
    files = list_files('.', '*.py')
    print(f'\nPython files in current directory: {len(files)}')
    for f in files[:5]:  # Show first 5
        print(f'  {f}')
    
    # Chunk list
    numbers = list(range(1, 11))
    chunks = chunk_list(numbers, 3)
    print(f'\nChunked list: {chunks}')
    
    # Calculate hashes
    text = 'Hello, World!'
    print(f'\nMD5 of "{text}": {calculate_md5(text)}')
    print(f'SHA256 of "{text}": {calculate_sha256(text)[:16]}...')

def main():
    """Main function"""
    # Initialize logger
    log = get_logger('main')
    log.info('=' * 50)
    log.info('Practical Python Examples Started')
    log.info('=' * 50)
    
    # Ensure output directory exists
    ensure_dir('output')
    ensure_dir('logs')
    
    # Run examples
    try:
        example_file_operations()
        example_json_operations()
        example_csv_operations()
        example_config_management()
        example_logging()
        example_utilities()
        
        log.info('\n' + '=' * 50)
        log.info('All examples completed successfully!')
        log.info('=' * 50)
        
    except Exception as e:
        log.error(f'Error occurred: {e}', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
