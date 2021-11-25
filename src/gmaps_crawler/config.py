from enum import Enum

from pydantic import BaseSettings


class StorageMode(Enum):
    DEBUG = "DEBUG"


class Settings(BaseSettings):
    STORAGE_MODE: StorageMode = StorageMode.DEBUG

    class Config:
        env_file = ".env"


settings = Settings()
