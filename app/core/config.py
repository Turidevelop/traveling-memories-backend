# core/config.py
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    ENVIRONMENT: str = "development"
    API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()


