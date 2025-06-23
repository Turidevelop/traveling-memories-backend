"""
Database initialization and session management (async version).
Follows Clean Architecture principles.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(str(settings.DATABASE_URL), echo=False, future=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async SQLAlchemy session and ensures it is closed after use.
    """
    async with SessionLocal() as session:
        yield session