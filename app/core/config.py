from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict, field_validator

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    ENVIRONMENT: str
    API_KEY: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_db_url(cls, v: str) -> str:
        v = str(v)
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()