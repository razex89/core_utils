"""
    name : logger.py
    
    purpose : logger.
    
    author : denjK
"""

# IMPORTS
import logging


def getLogger(name, log_file_path=None):
    logger = logging.getLogger(name)
    logger._format = logging.Formatter('%(asctime)s:%(name)s:%(levelno)s:%(message)s')
    logger.setLevel(logging.DEBUG)
    if log_file_path:
        file_handler = logging.FileHandler(log_file_path, mode='ab')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logger._format)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logger._format)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    return logger
