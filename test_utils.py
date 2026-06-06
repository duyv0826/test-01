"""
Unit tests for utils.py
Run: pytest test_utils.py -v
"""

import pytest
import os
import json
import tempfile
from utils import (
    read_file, write_file, read_json, write_json,
    read_csv, write_csv, calculate_md5, calculate_sha256,
    get_timestamp, list_files, ensure_dir, flatten_dict, chunk_list
)


class TestFileOperations:
    """Test file operations"""
    
    def setup_method(self):
        """Setup for each test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.txt')
    
    def teardown_method(self):
        """Cleanup after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)
    
    def test_write_and_read_file(self):
        """Test write_file and read_file"""
        # Write file
        content = 'Hello, World!\nThis is a test.'
        result = write_file(self.test_file, content)
        assert result == True
        assert os.path.exists(self.test_file)
        
        # Read file
        read_content = read_file(self.test_file)
        assert read_content == content
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        result = read_file('nonexistent.txt')
        assert result == ''
    
    def test_read_file_with_encoding(self):
        """Test reading file with different encoding"""
        content = 'Hello, 世界!'
        write_file(self.test_file, content, encoding='utf-8')
        
        read_content = read_file(self.test_file, encoding='utf-8')
        assert read_content == content



class TestJSONOperations:
    """Test JSON operations"""
    
    def setup_method(self):
        """Setup for each test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.json')
    
    def test_write_and_read_json(self):
        """Test write_json and read_json"""
        data = {
            'name': 'Test',
            'value': 123,
            'nested': {'key': 'value'}
        }
        
        # Write JSON
        result = write_json(self.test_file, data)
        assert result == True
        assert os.path.exists(self.test_file)
        
        # Read JSON
        read_data = read_json(self.test_file)
        assert read_data == data
    
    def test_read_invalid_json(self):
        """Test reading invalid JSON file"""
        # Write invalid JSON
        with open(self.test_file, 'w') as f:
            f.write('invalid json')
        
        result = read_json(self.test_file)
        assert result == {}



class TestHashFunctions:
    """Test hash functions"""
    
    def test_calculate_md5(self):
        """Test MD5 calculation"""
        result = calculate_md5('hello')
        assert result == '5d41402abc4b2a76b9719d911017c592'
    
    def test_calculate_sha256(self):
        """Test SHA256 calculation"""
        result = calculate_sha256('hello')
        assert result == '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    
    def test_hash_empty_string(self):
        """Test hashing empty string"""
        md5_result = calculate_md5('')
        sha_result = calculate_sha256('')
        assert len(md5_result) == 32
        assert len(sha_result) == 64



class TestTimestamp:
    """Test timestamp function"""
    
    def test_get_timestamp(self):
        """Test timestamp generation"""
        result = get_timestamp()
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_get_timestamp_custom_format(self):
        """Test timestamp with custom format"""
        result = get_timestamp('%Y-%m-%d')
        assert isinstance(result, str)
        # Should match YYYY-MM-DD format
        import re
        assert re.match(r'\d{4}-\d{2}-\d{2}', result)



class TestDictOperations:
    """Test dictionary operations"""
    
    def test_flatten_dict(self):
        """Test dictionary flattening"""
        nested = {
            'a': 1,
            'b': {'c': 2, 'd': 3},
            'e': {'f': {'g': 4}}
        }
        
        flat = flatten_dict(nested)
        expected = {
            'a': 1,
            'b.c': 2,
            'b.d': 3,
            'e.f.g': 4
        }
        
        assert flat == expected
    
    def test_flatten_empty_dict(self):
        """Test flattening empty dictionary"""
        result = flatten_dict({})
        assert result == {}


class TestListOperations:
    """Test list operations"""
    
    def test_chunk_list(self):
        """Test list chunking"""
        lst = [1, 2, 3, 4, 5, 6, 7]
        
        # Chunk into 3
        result = chunk_list(lst, 3)
        expected = [[1, 2, 3], [4, 5, 6], [7]]
        assert result == expected
    
    def test_chunk_list_even(self):
        """Test chunking with even division"""
        lst = [1, 2, 3, 4]
        result = chunk_list(lst, 2)
        expected = [[1, 2], [3, 4]]
        assert result == expected
    
    def test_chunk_list_larger_than_size(self):
        """Test chunking when chunk size > list size"""
        lst = [1, 2]
        result = chunk_list(lst, 5)
        expected = [[1, 2]]
        assert result == expected



class TestDirectoryOperations:
    """Test directory operations"""
    
    def test_ensure_dir(self):
        """Test directory creation"""
        test_dir = tempfile.mkdtemp()
        new_dir = os.path.join(test_dir, 'subdir', 'nested')
        
        result = ensure_dir(new_dir)
        assert result == True
        assert os.path.exists(new_dir)
    
    def test_list_files(self):
        """Test file listing"""
        test_dir = tempfile.mkdtemp()
        
        # Create test files
        for i in range(3):
            with open(os.path.join(test_dir, f'test{i}.txt'), 'w') as f:
                f.write(f'File {i}')
        
        # List files
        files = list_files(test_dir, '*.txt')
        assert len(files) == 3



class TestCSVOperations:
    """Test CSV operations"""
    
    def setup_method(self):
        """Setup for each test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.csv')
    
    def test_write_and_read_csv(self):
        """Test write_csv and read_csv"""
        data = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'}
        ]
        
        # Write CSV
        result = write_csv(self.test_file, data)
        assert result == True
        assert os.path.exists(self.test_file)
        
        # Read CSV
        read_data = read_csv(self.test_file)
        assert len(read_data) == 2
        assert read_data[0]['name'] == 'Alice'
        assert read_data[1]['age'] == '25'



# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
