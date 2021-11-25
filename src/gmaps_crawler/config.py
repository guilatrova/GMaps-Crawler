import logging.config
from enum import Enum

from pydantic import BaseSettings


class StorageMode(Enum):
    DEBUG = "DEBUG"
    SQS = "SQS"


class Settings(BaseSettings):
    STORAGE_MODE: StorageMode = StorageMode.DEBUG
    SCRAPED_EVENT_SQS_URL: str = ""

    class Config:
        env_file = ".env"


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(message)s",
            "datefmt": "[%X]",
        }
    },
    "handlers": {
        "rich": {
            "level": "INFO",
            "formatter": "default",
            "class": "rich.logging.RichHandler",
            "rich_tracebacks": True,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["rich"],
    },
}
logging.config.dictConfig(LOGGING_CONFIG)


settings = Settings()
