# utils/logger.py

import logging
from config.settings import LOG_FILE, LOG_LEVEL


def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
