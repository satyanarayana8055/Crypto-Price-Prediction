"""Centralized logging with rotation for CryptoPredictor"""

import logging
import os 
from logging.handlers import RotatingFileHandler
from utils.helper import ensure_directory
from config.config import LOG_CONFIG

def get_logger(name: str) -> logging.Logger:
    """Create a logger with rotation
       Tell the function name is str only and it should return the logging.logger only 
       It is for code readability and maintainability"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_CONFIG['level']))

        log_dir = 'logs'
        ensure_directory(log_dir)

        log_file = os.path.join(log_dir, f'{name}.log')

        handler = RotatingFileHandler(
            log_file, 
            maxBytes=LOG_CONFIG['max_bytes'],
            backupCount=LOG_CONFIG['backup_count']
        )

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

