# core/config.py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict

# Cargar .env automáticamente
load_dotenv()

class Settings(BaseSettings):
    # Database connection (includes user, password, host, port, db name)
    DATABASE_URL: PostgresDsn
    
    # API Configuration
    ENVIRONMENT: str = "development"
    API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()


