"""This module sets up a logger to log message for CLI application.
It provide functions to configure a logger that outputs log messages to console with timestamps, log levels and actual message."""
import logging

def setup_logger():
    """
    Sets up and returns a logger configured to output the console.
    """
    logger = logging.getLogger('github_cli')
    
    # Clear existing handlers to avoid duplicate logging
    if logger.handlers:
        logger.handlers.clear()
        
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
