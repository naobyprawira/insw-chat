import pytest
import os
import logging
import shutil
from modules import app_logger

# Clean up logs directory before tests
@pytest.fixture(autouse=True)
def clean_logs():
    # Close any existing handlers to release file locks
    root = logging.getLogger()
    for handler in root.handlers[:]:
        handler.close()
        root.removeHandler(handler)
        
    # Also clear specific loggers
    for name in ["app_logger", "llm_logger"]:
        logger = logging.getLogger(name)
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
            
    if os.path.exists("logs"):
        try:
            shutil.rmtree("logs")
        except PermissionError:
            pass # Best effort cleanup
    yield
    
    # Cleanup after test
    for name in ["app_logger", "llm_logger"]:
        logger = logging.getLogger(name)
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

def test_setup_logger_creates_file():
    """Test that setup_logger creates the log file and directory"""
    logger = app_logger.setup_logger()
    
    assert os.path.exists("logs")
    assert os.path.exists("logs/app.log")
    assert logger.name == "app_logger"
    assert logger.level == logging.INFO

def test_setup_llm_logger_creates_file():
    """Test that setup_llm_logger creates the log file"""
    logger = app_logger.setup_llm_logger()
    
    assert os.path.exists("logs/llm_analytics.log")
    assert logger.name == "llm_logger"
    assert logger.level == logging.INFO

def test_logger_writes_to_file():
    """Test that logger actually writes content to file"""
    logger = app_logger.setup_logger()
    test_message = "Test log message"
    logger.info(test_message)
    
    with open("logs/app.log", "r") as f:
        content = f.read()
        assert test_message in content

def test_llm_logger_format():
    """Test LLM logger format"""
    logger = app_logger.setup_llm_logger()
    logger.info("LLM Call", extra={"tokens": 100, "cost": 0.01})
    
    with open("logs/llm_analytics.log", "r") as f:
        content = f.read()
        assert "LLM Call" in content
