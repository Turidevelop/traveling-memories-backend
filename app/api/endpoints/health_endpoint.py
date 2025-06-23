"""
Health and database check endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/db-url", tags=["database"])
def get_database_url() -> dict[str, str]:
    """
    Returns the database URL from settings.
    """
    return {"database_url": str(settings.DATABASE_URL)}


@router.get("/environment", tags=["environment"])
def health_check() -> dict[str, str]:
    """
    Environment endpoint.
    Returns a simple message indicating the environment.
    """
    return {"environment": settings.ENVIRONMENT}


@router.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health_check_async() -> dict[str, str]:
    """
    Asynchronous health check endpoint.
    Returns a simple message indicating the service is running.
    """
    return {"status": "ok"}


@router.get("/db-health", tags=["database"], status_code=status.HTTP_200_OK)
async def db_health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Checks database connectivity by executing a simple query.
    Returns 200 OK and a message if connected.
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"message": "La base de datos está conectada"}
    except Exception as e:
        # Puedes cambiar el status code si quieres devolver 500 en caso de error
        return {"message": "Error de conexión a la base de datos", "detail": str(e)}

