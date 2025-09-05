from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.core.models import PlaceVisited
from fastapi import Depends
from app.database import get_db
from sqlalchemy.future import select

class PlaceVisitedRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> PlaceVisited:
        stmt = insert(PlaceVisited).values(**data).returning(PlaceVisited)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def get_by_id(self, place_visited_id: int) -> PlaceVisited | None:
        stmt = select(PlaceVisited).where(PlaceVisited.id == place_visited_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

async def get_place_visited_repo(db: AsyncSession = Depends(get_db)) -> PlaceVisitedRepo:
    """
    Async dependency injector for PlaceVisitedRepo.
    """
    return PlaceVisitedRepo(db)