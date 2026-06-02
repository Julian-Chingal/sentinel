import logging
import os
from logging.handlers import RotatingFileHandler
from config.config import Config

def get_logger(name="sentinel"):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Ensure log directory exists
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler (Rotating)
        log_file = os.path.join(Config.LOG_DIR, "sentinel.log")
        fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger

logger = get_logger()
