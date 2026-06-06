"""
Data processing utilities for CSV, JSON, and Excel files
Requires: pandas, openpyxl (for Excel support)
"""

import os
import json
import csv
from typing import List, Dict, Any, Optional
import pandas as pd
from logger import get_logger

logger = get_logger('data_processor')

class DataProcessor:
    """
    Unified data processing class for handling CSV, JSON, and Excel files
    
    Usage:
        processor = DataProcessor()
        
        # Read data
        data = processor.read_csv('data.csv')
        data = processor.read_json('data.json')
        data = processor.read_excel('data.xlsx')
        
        # Process data
        filtered = processor.filter_by_column(data, 'age', lambda x: x > 25)
        sorted_data = processor.sort_by_column(data, 'name')
        
        # Write data
        processor.write_csv('output.csv', data)
        processor.write_json('output.json', data)
        processor.write_excel('output.xlsx', data)
    """
    
    def __init__(self):
        """Initialize DataProcessor"""
        logger.info('DataProcessor initialized')
    
    def read_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Read CSV file
        
        Args:
            filepath: Path to CSV file
        
        Returns:
            List of dictionaries
        """
        try:
            df = pd.read_csv(filepath)
            logger.info(f'Read CSV: {filepath} ({len(df)} rows)')
            return df.to_dict('records')
        except Exception as e:
            logger.error(f'Error reading CSV {filepath}: {e}')
            return []
    
    def read_json(self, filepath: str) -> Any:
        """
        Read JSON file
        
        Args:
            filepath: Path to JSON file
        
        Returns:
            Parsed JSON data
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f'Read JSON: {filepath}')
            return data
        except Exception as e:
            logger.error(f'Error reading JSON {filepath}: {e}')
            return []
    
    def read_excel(self, filepath: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """
        Read Excel file
        
        Args:
            filepath: Path to Excel file
            sheet_name: Sheet name (optional)
        
        Returns:
            List of dictionaries
        """
        try:
            if sheet_name:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
            else:
                df = pd.read_excel(filepath)
            logger.info(f'Read Excel: {filepath} ({len(df)} rows)')
            return df.to_dict('records')
        except Exception as e:
            logger.error(f'Error reading Excel {filepath}: {e}')
            return []
    
    def write_csv(self, filepath: str, data: List[Dict[str, Any]]) -> bool:
        """
        Write data to CSV file
        
        Args:
            filepath: Path to output CSV file
            data: List of dictionaries
        
        Returns:
            True if successful
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f'Wrote CSV: {filepath} ({len(data)} rows)')
            return True
        except Exception as e:
            logger.error(f'Error writing CSV {filepath}: {e}')
            return False
    
    def write_json(self, filepath: str, data: Any, indent: int = 2) -> bool:
        """
        Write data to JSON file
        
        Args:
            filepath: Path to output JSON file
            data: Data to write
            indent: JSON indentation
        
        Returns:
            True if successful
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            logger.info(f'Wrote JSON: {filepath}')
            return True
        except Exception as e:
            logger.error(f'Error writing JSON {filepath}: {e}')
            return False
    
    def write_excel(self, filepath: str, data: List[Dict[str, Any]], sheet_name: str = 'Sheet1') -> bool:
        """
        Write data to Excel file
        
        Args:
            filepath: Path to output Excel file
            data: List of dictionaries
            sheet_name: Sheet name
        
        Returns:
            True if successful
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            df = pd.DataFrame(data)
            df.to_excel(filepath, sheet_name=sheet_name, index=False)
            logger.info(f'Wrote Excel: {filepath} ({len(data)} rows)')
            return True
        except Exception as e:
            logger.error(f'Error writing Excel {filepath}: {e}')
            return False
    
    def filter_by_column(self, data: List[Dict[str, Any]], column: str, condition) -> List[Dict[str, Any]]:
        """
        Filter data by column condition
        
        Args:
            data: List of dictionaries
            column: Column name
            condition: Lambda function or condition
        
        Returns:
            Filtered data
        """
        try:
            df = pd.DataFrame(data)
            filtered_df = df[df[column].apply(condition)]
            result = filtered_df.to_dict('records')
            logger.info(f'Filtered {column}: {len(data)} -> {len(result)} rows')
            return result
        except Exception as e:
            logger.error(f'Error filtering by {column}: {e}')
            return data
    
    def sort_by_column(self, data: List[Dict[str, Any]], column: str, ascending: bool = True) -> List[Dict[str, Any]]:
        """
        Sort data by column
        
        Args:
            data: List of dictionaries
            column: Column name
            ascending: Sort order
        
        Returns:
            Sorted data
        """
        try:
            df = pd.DataFrame(data)
            sorted_df = df.sort_values(by=column, ascending=ascending)
            result = sorted_df.to_dict('records')
            logger.info(f'Sorted by {column} ({'asc' if ascending else 'desc'})')
            return result
        except Exception as e:
            logger.error(f'Error sorting by {column}: {e}')
            return data
    
    def group_by_column(self, data: List[Dict[str, Any]], column: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group data by column
        
        Args:
            data: List of dictionaries
            column: Column name
        
        Returns:
            Dictionary with grouped data
        """
        try:
            df = pd.DataFrame(data)
            grouped = {}
            for name, group in df.groupby(column):
                grouped[str(name)] = group.to_dict('records')
            logger.info(f'Grouped by {column}: {len(grouped)} groups')
            return grouped
        except Exception as e:
            logger.error(f'Error grouping by {column}: {e}')
            return {}
    
    def get_statistics(self, data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
        """
        Get statistics for numeric column
        
        Args:
            data: List of dictionaries
            column: Column name
        
        Returns:
            Dictionary with statistics
        """
        try:
            df = pd.DataFrame(data)
            if column in df.columns:
                stats = df[column].describe().to_dict()
                logger.info(f'Statistics for {column}: {stats}')
                return stats
            return {}
        except Exception as e:
            logger.error(f'Error getting statistics for {column}: {e}')
            return {}


# Example usage
if __name__ == '__main__':
    print('=== DataProcessor Example ===\n')
    
    # Create sample data
    sample_data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York', 'salary': 70000},
        {'name': 'Bob', 'age': 25, 'city': 'London', 'salary': 60000},
        {'name': 'Charlie', 'age': 35, 'city': 'Tokyo', 'salary': 80000},
        {'name': 'Diana', 'age': 28, 'city': 'New York', 'salary': 75000},
    ]
    
    # Create processor
    processor = DataProcessor()
    
    # Write sample data
    print('1. Writing sample data...')
    processor.write_json('output/sample_data.json', sample_data)
    processor.write_csv('output/sample_data.csv', sample_data)
    
    # Read data
    print('\n2. Reading data...')
    data = processor.read_json('output/sample_data.json')
    print(f'   Loaded {len(data)} records')
    
    # Filter data
    print('\n3. Filtering (age > 25)...')
    filtered = processor.filter_by_column(data, 'age', lambda x: x > 25)
    for person in filtered:
        print(f'   {person["name"]} ({person["age"]})')
    
    # Sort data
    print('\n4. Sorting by salary (desc)...')
    sorted_data = processor.sort_by_column(data, 'salary', ascending=False)
    for person in sorted_data:
        print(f'   {person["name"]}: ${person["salary"]}')
    
    # Group by city
    print('\n5. Grouping by city...')
    grouped = processor.group_by_column(data, 'city')
    for city, people in grouped.items():
        print(f'   {city}: {len(people)} people')
    
    # Get statistics
    print('\n6. Salary statistics...')
    stats = processor.get_statistics(data, 'salary')
    for key, value in stats.items():
        print(f'   {key}: {value}')
    
    print('\n[OK] Data processing completed successfully!')
