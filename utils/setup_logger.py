import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name):
    """Configure logger with file and console handlers"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create logs directory in project root
        log_dir = Path(__file__).parent.parent / 'logs'
        try:
            log_dir.mkdir(exist_ok=True)
            
            # Create log file with timestamp
            log_file = log_dir / f"{name.split('.')[-1]}_{datetime.now().strftime('%Y%m%d')}.log"
            
            # Configure handlers
            file_handler = logging.FileHandler(str(log_file), mode='a')
            console_handler = logging.StreamHandler()

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Apply formatter and add handlers
            for handler in [file_handler, console_handler]:
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                
        except PermissionError as e:
            print(f"Permission error creating log file: {e}")
            # Fallback to console-only logging
            logger.addHandler(console_handler)
        except Exception as e:
            print(f"Error setting up file logging: {e}")
            # Fallback to console-only logging
            logger.addHandler(console_handler)
    
    return logger