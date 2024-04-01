# rssapp/log_handlers.py
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class UniqueFileHandler(RotatingFileHandler):
    def __init__(self, directory, filename, maxBytes, backupCount=0, encoding=None, delay=False):
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        # Generate a unique filename with timestamp
        unique_filename = f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        super().__init__(os.path.join(directory, unique_filename), maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)