from pydantic import BaseSettings


class Settings(BaseSettings):
    STORAGE_MODE: str = "DEBUG"


settings = Settings()
