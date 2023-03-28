from pydantic import BaseModel
import logging
from fastapi.logger import logger as fastapi_log
from logging.config import dictConfig


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "mycoolapp"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


# Initialise logger
dictConfig(LogConfig().dict())
# Get logger
logger = logging.getLogger("mycoolapp")
# Get all handlers from both gunicorn and uvicorn. This is necessary to display all longs.
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

fastapi_log.handlers = gunicorn_error_logger.handlers

FORMAT: str = "%(levelname)s | %(asctime)s | %(message)s"
# Set up custom formating for loggers. Question can be raised if above config is necessary. It works.
fastapi_log.setLevel(logging.INFO)
fastapi_log = fastapi_log.handlers[0]
fastapi_log.setFormatter(logging.Formatter(FORMAT))
