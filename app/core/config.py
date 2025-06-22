# core/config.py
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instancia única de configuración
settings = Settings()

