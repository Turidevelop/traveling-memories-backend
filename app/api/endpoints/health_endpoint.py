"""
Health and database check endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/database", tags=["database"])
def get_database_url() -> dict[str, str]:
    """
    Returns the database URL from settings.
    """
    return {"database_url": str(settings.DATABASE_URL)}


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """
    Health check endpoint.
    Returns a simple message indicating the service is running.
    """
    return {"status": "ok", "environment": settings.ENVIRONMENT}


@router.get("/db-health", tags=["health"], status_code=status.HTTP_200_OK)
async def db_health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Checks database connectivity by executing a simple query.
    """
    try:
        await db.execute("SELECT 1")
        return {"db_status": "ok"}
    except Exception as e:
        return {"db_status": "error", "detail": str(e)}

