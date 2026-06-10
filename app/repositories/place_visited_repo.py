from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select, insert, delete
from app.core.models import PlaceVisited
from app.database import get_db


class PlaceVisitedRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_trip(self, trip_id: int) -> List[PlaceVisited]:
        result = await self.db.execute(
            select(PlaceVisited).where(PlaceVisited.trip_id == trip_id)
        )
        return result.scalars().all()

    async def get_by_id(self, place_id: int) -> Optional[PlaceVisited]:
        result = await self.db.execute(
            select(PlaceVisited).where(PlaceVisited.id == place_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> PlaceVisited:
        stmt = insert(PlaceVisited).values(**data).returning(PlaceVisited)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def delete(self, place_id: int) -> bool:
        result = await self.db.execute(
            delete(PlaceVisited).where(PlaceVisited.id == place_id)
        )
        await self.db.commit()
        return result.rowcount > 0