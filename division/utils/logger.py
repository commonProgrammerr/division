import logging
import os
from logging import handlers

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()


formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s l:%(lineno)d f:%(filename)s: %(message)s"
)


def get_logger(log_name="division", log_file="division.log"):
    log = logging.getLogger(log_name)
    log.setLevel("DEBUG")
    handler = handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=10)
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
