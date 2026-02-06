# core/config.py
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict

class Settings(BaseSettings):
    # Database connection
    DATABASE_URL: PostgresDsn
    
    # Database credentials for admin operations
    DB_ADMIN_USER: str
    DB_ADMIN_PASSWORD: str
    
    # Database credentials for app user (CRUD operations)
    DB_APP_USER: str 
    DB_APP_PASSWORD: str
    
    # API Configuration
    ENVIRONMENT: str = "development"
    API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()


