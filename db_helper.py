"""
Simple database helper with SQLite support (no external dependencies)
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional, Tuple
from logger import get_logger

class DBHelper:
    """
    Simple SQLite database helper
    
    Usage:
        db = DBHelper('app.db')
        db.create_table('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')
        
        # Insert
        db.insert('users', {'name': 'Alice', 'email': 'alice@example.com'})
        
        # Query
        users = db.query('SELECT * FROM users')
        
        # Update
        db.update('users', {'name': 'Bob'}, 'WHERE id = ?', (1,))
        
        # Delete
        db.delete('users', 'WHERE id = ?', (1,))
        
        db.close()
    """
    
    def __init__(self, db_path: str = 'app.db'):
        """
        Initialize database helper
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = get_logger('db_helper')
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Connect to database
        
        Returns:
            True if successful
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            self.cursor = self.connection.cursor()
            self.logger.info(f'Connected to database: {self.db_path}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to connect to database: {e}')
            return False
    
    def create_table(self, create_sql: str) -> bool:
        """
        Create table
        
        Args:
            create_sql: CREATE TABLE SQL statement
        
        Returns:
            True if successful
        """
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(create_sql)
            self.connection.commit()
            self.logger.info('Table created successfully')
            return True
        except Exception as e:
            self.logger.error(f'Failed to create table: {e}')
            return False
    
    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        Insert record
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs
        
        Returns:
            Last row ID if successful, None otherwise
        """
        try:
            if not self.connection:
                self.connect()
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
            
            self.cursor.execute(sql, list(data.values()))
            self.connection.commit()
            
            last_id = self.cursor.lastrowid
            self.logger.debug(f'Inserted record into {table}, ID: {last_id}')
            return last_id
        except Exception as e:
            self.logger.error(f'Failed to insert record: {e}')
            return None
    
    def query(self, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute query
        
        Args:
            sql: SQL query
            params: Query parameters
        
        Returns:
            List of dictionaries (each row is a dict)
        """
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            result = []
            for row in rows:
                result.append(dict(row))
            
            self.logger.debug(f'Query returned {len(result)} rows')
            return result
        except Exception as e:
            self.logger.error(f'Failed to execute query: {e}')
            return []
    
    def query_one(self, sql: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Execute query and return first row
        
        Args:
            sql: SQL query
            params: Query parameters
        
        Returns:
            Dictionary or None
        """
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.execute(sql, params)
            row = self.cursor.fetchone()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            self.logger.error(f'Failed to execute query: {e}')
            return None
    
    def update(self, table: str, data: Dict[str, Any], where: str = '', params: Tuple = ()) -> bool:
        """
        Update records
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs to update
            where: WHERE clause (without WHERE keyword)
            params: Parameters for WHERE clause
        
        Returns:
            True if successful
        """
        try:
            if not self.connection:
                self.connect()
            
            set_clause = ', '.join([f'{k} = ?' for k in data.keys()])
            sql = f'UPDATE {table} SET {set_clause}'
            if where:
                sql += f' WHERE {where}'
            
            self.cursor.execute(sql, list(data.values()) + list(params))
            self.connection.commit()
            
            row_count = self.cursor.rowcount
            self.logger.debug(f'Updated {row_count} rows in {table}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to update records: {e}')
            return False
    
    def delete(self, table: str, where: str = '', params: Tuple = ()) -> bool:
        """
        Delete records
        
        Args:
            table: Table name
            where: WHERE clause (without WHERE keyword)
            params: Parameters for WHERE clause
        
        Returns:
            True if successful
        """
        try:
            if not self.connection:
                self.connect()
            
            sql = f'DELETE FROM {table}'
            if where:
                sql += f' WHERE {where}'
            
            self.cursor.execute(sql, params)
            self.connection.commit()
            
            row_count = self.cursor.rowcount
            self.logger.debug(f'Deleted {row_count} rows from {table}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to delete records: {e}')
            return False
    
    def execute_script(self, sql_script: str) -> bool:
        """
        Execute SQL script (multiple statements)
        
        Args:
            sql_script: SQL script
        
        Returns:
            True if successful
        """
        try:
            if not self.connection:
                self.connect()
            
            self.cursor.executescript(sql_script)
            self.connection.commit()
            
            self.logger.info('SQL script executed successfully')
            return True
        except Exception as e:
            self.logger.error(f'Failed to execute SQL script: {e}')
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info('Database connection closed')
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example usage
if __name__ == '__main__':
    print('=== Database Helper Example ===\n')
    
    # Create database helper
    db = DBHelper('example.db')
    
    # Create table
    db.create_table('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert records
    print('1. Inserting records...')
    db.insert('users', {'name': 'Alice', 'email': 'alice@example.com', 'age': 30})
    db.insert('users', {'name': 'Bob', 'email': 'bob@example.com', 'age': 25})
    db.insert('users', {'name': 'Charlie', 'email': 'charlie@example.com', 'age': 35})
    
    # Query all records
    print('2. Querying all users...')
    users = db.query('SELECT * FROM users')
    for user in users:
        print(f'   ID: {user["id"]}, Name: {user["name"]}, Age: {user["age"]}')
    
    # Query one record
    print('\n3. Querying one user (Bob)...')
    bob = db.query_one('SELECT * FROM users WHERE name = ?', ('Bob',))
    if bob:
        print(f'   Found: {bob["name"]} ({bob["email"]})')
    
    # Update record
    print('\n4. Updating Bobs age...')
    db.update('users', {'age': 26}, 'WHERE name = ?', ('Bob',))
    
    # Query updated record
    bob = db.query_one('SELECT * FROM users WHERE name = ?', ('Bob',))
    print(f'   Bobs new age: {bob["age"]}')
    
    # Delete record
    print('\n5. Deleting Charlie...')
    db.delete('users', 'WHERE name = ?', ('Charlie',))
    
    # Query remaining users
    print('6. Remaining users...')
    users = db.query('SELECT * FROM users')
    for user in users:
        print(f'   ID: {user["id"]}, Name: {user["name"]}')
    
    # Close connection
    db.close()
    print('\n✓ Database operations completed successfully!')
    print('   Database file: example.db')
