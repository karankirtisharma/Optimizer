"""
Logging configuration for Ruddibaba Optimizer
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

class LogManager:
    """Manages logging configuration and log file handling"""
    
    def __init__(self, log_level: int = logging.INFO, log_to_file: bool = True):
        """
        Initialize the log manager
        
        Args:
            log_level: Logging level (default: logging.INFO)
            log_to_file: Whether to log to a file (default: True)
        """
        self.log_level = log_level
        self.log_to_file = log_to_file
        self.log_dir = os.path.join(
            os.environ.get('LOCALAPPDATA', ''),
            'RuddibabaOptimizer',
            'logs'
        )
        self.log_file = os.path.join(self.log_dir, 'ruddibaba_optimizer.log')
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configure logging with both console and file handlers"""
        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        
        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (rotating)
        if self.log_to_file:
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=5*1024*1024,  # 5MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger instance with the specified name
        
        Args:
            name: Logger name (usually __name__)
            
        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)

# Default logger instance
logger = LogManager().get_logger(__name__)

def setup_logging(log_level: int = logging.INFO, log_to_file: bool = True) -> LogManager:
    """
    Set up logging configuration
    
    Args:
        log_level: Logging level (default: logging.INFO)
        log_to_file: Whether to log to a file (default: True)
        
    Returns:
        LogManager instance
    """
    return LogManager(log_level=log_level, log_to_file=log_to_file)
