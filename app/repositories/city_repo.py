from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.core.models import City
from fastapi import Depends
from app.database import get_db

class CityRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_city(self, data: dict) -> City:
        stmt = insert(City).values(**data).returning(City)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

async def get_city_repo(db: AsyncSession = Depends(get_db)) -> CityRepo:
    return CityRepo(db)