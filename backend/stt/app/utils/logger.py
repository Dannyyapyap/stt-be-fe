import logging
import sys
from pathlib import Path

# Simple singleton logger implementation
# This ensures we have a single logger instance across our application
# Good for maintaining consistent logging and avoiding duplicate logs
class Logger:
    _instance = None

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            logger = logging.getLogger('app') # Initialize logger with app name. This helps identify logs from this application
            logger.setLevel(logging.INFO)

            # Set up console handler for development visibility
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(console_handler)

            # Set up file handler for persistent logs
            root_dir = Path(__file__).parent.parent.parent  # Store in project root for easy access.
            log_file = root_dir / 'log.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(file_handler)

            cls._instance = logger

        return cls._instance


logger = Logger.get_logger()