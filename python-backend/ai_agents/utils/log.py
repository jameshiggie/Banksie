import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    logger_name: Optional[str] = None,
    format_string: str = '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    date_format: str = '%H:%M:%S'
) -> logging.Logger:
    """
    Set up logging configuration optimized for VS Code debug console.
    
    Args:
        level: Logging level (default: INFO)
        logger_name: Name for the logger (default: None for root logger)
        format_string: Log message format
        date_format: Date format for timestamps
    
    Returns:
        Configured logger instance
    """
    
    # Configure root logger only once
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        # Enhanced logging configuration for VS Code debug console
        logging.basicConfig(
            level=level,
            format=format_string,
            datefmt=date_format,
            handlers=[
                logging.StreamHandler(sys.stdout)  # Ensures output goes to console that VS Code can capture
            ]
        )
    
    # Get specific logger if name provided
    if logger_name:
        logger = logging.getLogger(logger_name)
        
        # Add dedicated handler for named loggers to ensure they show up in VS Code
        if not logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            
            formatter = logging.Formatter(
                fmt=format_string,
                datefmt=date_format
            )
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.setLevel(level)
            logger.propagate = False  # Prevent duplicate messages
            
        return logger
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    return setup_logging(logger_name=name)