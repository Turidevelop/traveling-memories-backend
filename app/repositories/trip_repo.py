from unittest import result

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Trip
from sqlalchemy import insert, select, update, delete
from app.database import get_db
from fastapi import Depends
from sqlalchemy.future import select


class TripRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def create_trip(self, trip_data: dict) -> Trip:
        stmt = insert(Trip).values(**trip_data).returning(Trip.id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        new_id = result.scalar_one()
    
        # Ahora hacemos un SELECT para traer el objeto completo
        select_stmt = select(Trip).where(Trip.id == new_id)
        result = await self.db.execute(select_stmt)
        return result.scalar_one()

    async def get_trip_by_id(self, trip_id: int) -> Trip | None:
        stmt = select(Trip).where(Trip.id == trip_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_trips_by_user_id(self, user_id: int) -> list[Trip]:
        stmt = select(Trip).where(Trip.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_trip(self, trip_id: int, trip_data: dict) -> Trip | None:
        stmt = update(Trip).where(Trip.id == trip_id).values(**trip_data).returning(Trip.id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        updated_id = result.scalar_one_or_none()
        if updated_id is None:
            return None
    
        select_stmt = select(Trip).where(Trip.id == updated_id)
        result = await self.db.execute(select_stmt)
        return result.scalar_one()

    async def delete_trip(self, trip_id: int) -> bool:
        stmt = delete(Trip).where(Trip.id == trip_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

async def get_trip_repo(db: AsyncSession = Depends(get_db)) -> TripRepo:
    """
    Async dependency injector for TripRepo.
    """
    return TripRepo(db)