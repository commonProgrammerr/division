import logging
import os
from logging import handlers

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()

log = logging.getLogger("division")

formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s l:%(lineno)d f:%(filename)s: %(message)s"
)


def get_logger(log_file="division.log"):
    handler = handlers.RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=10)
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
