"""
Simple and practical logger utility
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional

class Logger:
    """
    Simple logger with file and console output
    
    Usage:
        log = Logger('my_app')
        log.info('Application started')
        log.error('Something went wrong', exc_info=True)
    """
    
    def __init__(self, name: str = 'app', log_dir: str = 'logs', level: int = logging.DEBUG):
        """
        Initialize logger
        
        Args:
            name: Logger name
            log_dir: Directory to save log files
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            # Ensure log directory exists
            os.makedirs(log_dir, exist_ok=True)
            
            # File handler
            log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, msg: str):
        """Log debug message"""
        self.logger.debug(msg)
    
    def info(self, msg: str):
        """Log info message"""
        self.logger.info(msg)
    
    def warning(self, msg: str):
        """Log warning message"""
        self.logger.warning(msg)
    
    def error(self, msg: str, exc_info: bool = False):
        """
        Log error message
        
        Args:
            msg: Error message
            exc_info: Include exception info
        """
        self.logger.error(msg, exc_info=exc_info)
    
    def critical(self, msg: str, exc_info: bool = False):
        """
        Log critical message
        
        Args:
            msg: Critical message
            exc_info: Include exception info
        """
        self.logger.critical(msg, exc_info=exc_info)
    
    def get_logger(self) -> logging.Logger:
        """
        Get underlying logger object
        
        Returns:
            logging.Logger object
        """
        return self.logger


# Global logger instance
_default_logger = None

def get_logger(name: str = 'app') -> Logger:
    """
    Get default logger instance (singleton pattern)
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = Logger(name)
    return _default_logger


# Example usage
if __name__ == '__main__':
    # Create logger
    log = Logger('test_app')
    
    # Log messages
    log.debug('This is a debug message')
    log.info('Application started')
    log.warning('This is a warning')
    log.error('This is an error')
    
    # Log with exception info
    try:
        result = 10 / 0
    except Exception as e:
        log.error(f'Exception occurred: {e}', exc_info=True)
    
    print('\nLog files saved to: logs/ directory')
