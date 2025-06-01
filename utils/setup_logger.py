import logging
import os
from datetime import datetime

def setup_logger(name):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logs_dir = 'logs'
        
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            
        file_handler = logging.FileHandler(
            f'logs/dashboard_{datetime.now().strftime("%Y%m%d")}.log'
        )
        console_handler = logging.StreamHandler()
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger