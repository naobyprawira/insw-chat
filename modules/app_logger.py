import logging
import os
from logging.handlers import RotatingFileHandler
import sys

# Ensure logs directory exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logger(name="app_logger", log_file="app.log", level=logging.INFO):
    """Function to setup a logger; can be used for different log files"""
    
    # Ensure logs directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if logger already has handlers to avoid duplicates
    if not logger.handlers:
        # Create handlers
        # 1. File Handler (Rotating)
        log_path = os.path.join(LOG_DIR, log_file)
        file_handler = RotatingFileHandler(log_path, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setLevel(level)
        
        # 2. Console Handler (Stream to stdout for Docker)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

def setup_llm_logger():
    """Setup specialized logger for LLM analytics"""
    return setup_logger(name="llm_logger", log_file="llm_analytics.log")
