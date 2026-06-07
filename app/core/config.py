# core/config.py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict, field_validator

# Cargar .env automáticamente
load_dotenv()

class Settings(BaseSettings):
    # Database connection (includes user, password, host, port, db name)
    DATABASE_URL: PostgresDsn
    
    # API Configuration
    ENVIRONMENT: str
    API_KEY: str

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_db_url(cls, v: str) -> str:
        v = str(v)
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()


