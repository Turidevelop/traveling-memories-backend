    
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

    async def get_all_cities(self) -> list[City]:
        from sqlalchemy import select
        result = await self.db.execute(select(City))
        return result.scalars().all()

    async def get_city_by_id(self, city_id: int) -> City | None:
        from sqlalchemy import select
        result = await self.db.execute(select(City).where(City.id == city_id))
        return result.scalar_one_or_none()

async def get_city_repo(db: AsyncSession = Depends(get_db)) -> CityRepo:
    return CityRepo(db)