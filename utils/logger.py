import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler,WatchedFileHandler

MAX_LOG_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_DIR = "logs/"
FILE_NAME = "{}/{}.log".format(LOG_DIR, datetime.now().strftime("%Y-%b-%d"))


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


# Single file for changes

# def get_file_handler(filename, formatter):
#     file_handler = WatchedFileHandler(filename)
#     file_handler.setFormatter(formatter)
#     return file_handler

# Automatically rotates log
def get_file_handler(filename, formatter):
    file_handler = RotatingFileHandler(
        filename,
        maxBytes=MAX_LOG_SIZE_BYTES,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    return file_handler


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(FILE_NAME, FORMATTER))
    logger.propagate = False
    return logger
