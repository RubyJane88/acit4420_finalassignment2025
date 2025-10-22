"""
Logging configuration for CourierOptimizer.
Provides centralized logging setup with file and console output.
"""

import logging
import os
from datetime import datetime
import time
from functools import wraps


def setup_logger(name='CourierOptimizer', log_dir='logs', level=logging.INFO):
    """
    Set up and configure logger for the application.
    
    Args:
        name (str): Name of the logger
        log_dir (str): Directory for log files
        level: Logging level (default: INFO)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Prevent adding duplicate handlers if already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename
    log_file = os.path.join(log_dir, 'run.log')
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Create file handler
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger():
    """Get the configured logger instance."""
    return setup_logger()


def timer(func):
    """
    Decorator to log function execution time.
    
    Usage:
        @timer
        def my_function():
            # code here
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = time.time()
        
        logger.info(f"Starting {func.__name__}()")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed = end_time - start_time
            logger.info(f"Completed {func.__name__}() in {elapsed:.2f}s")
            return result
            
        except Exception as e:
            end_time = time.time()
            elapsed = end_time - start_time
            logger.error(f"Failed {func.__name__}() after {elapsed:.2f}s: {e}")
            raise
    
    return wrapper
