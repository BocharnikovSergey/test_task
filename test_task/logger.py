import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings


def configure_logging():
    """Настройка логгирование для проекта."""

    formatter = logging.Formatter(
        fmt=settings.LOG_FORMAT,
        datefmt=settings.DT_FORMAT
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    rotating_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.MAX_BYTES,
        backupCount=settings.BACKUP_COUNT,
        encoding=settings.ENCODING,
    )
    rotating_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)
    return logger

logger_even = configure_logging()
