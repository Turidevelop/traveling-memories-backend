from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.core.models import Country
from fastapi import Depends
from app.database import get_db

class CountryRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_country(self, data: dict) -> Country:
        stmt = insert(Country).values(**data).returning(Country)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

async def get_country_repo(db: AsyncSession = Depends(get_db)) -> CountryRepo:
    return CountryRepo(db)