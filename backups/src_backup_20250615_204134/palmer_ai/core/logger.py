"""Palmer AI Production Logging System"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """Get configured logger for module"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Console handler
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            f"logs/palmer_ai_{datetime.now():%Y%m%d}.log",
            maxBytes=10_000_000,
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        ))
        
        logger.addHandler(console)
        logger.addHandler(file_handler)
    
    return logger
