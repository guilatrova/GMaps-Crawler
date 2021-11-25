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


settings = Settings()
