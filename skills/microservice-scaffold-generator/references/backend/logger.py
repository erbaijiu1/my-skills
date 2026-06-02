import os
import logging
from logging.handlers import RotatingFileHandler

# Project paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GLOBAL_LOG_PATH = os.path.join(DATA_DIR, "app.log")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def setup_logger(name, log_file=GLOBAL_LOG_PATH, level=logging.DEBUG):
    """Setup project global logger"""
    formatter = logging.Formatter('%(asctime)s|[%(filename)s: %(lineno)d]|%(levelname)s|%(thread)d|%(message)s ')

    # Rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=500*1024*1024, backupCount=20)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times if logger already exists
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger("{project_name}")
