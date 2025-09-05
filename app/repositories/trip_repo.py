from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Trip
from sqlalchemy import insert, select
from app.database import get_db
from fastapi import Depends
from sqlalchemy.future import select


class TripRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_trip(self, trip_data: dict) -> Trip:
        stmt = insert(Trip).values(**trip_data).returning(Trip)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def get_trip_by_id(self, trip_id: int):
        stmt = select(Trip).where(Trip.id == trip_id)
        result = await self.db.execute(stmt)
        trip = result.scalar_one_or_none()
        return trip

async def get_trip_repo(db: AsyncSession = Depends(get_db)) -> TripRepo:
    """
    Async dependency injector for TripRepo.
    """
    return TripRepo(db)