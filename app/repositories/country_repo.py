from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
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

    async def get_all_countries(self) -> list[Country]:
        result = await self.db.execute(select(Country))
        return result.scalars().all()

    async def get_country_by_id(self, country_id: int) -> Country | None:
        result = await self.db.execute(select(Country).where(Country.id == country_id))
        return result.scalar_one_or_none()

    async def update_country(self, country_id: int, data: dict) -> Country | None:
        stmt = update(Country).where(Country.id == country_id).values(**data).returning(Country)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_country(self, country_id: int) -> bool:
        stmt = delete(Country).where(Country.id == country_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

async def get_country_repo(db: AsyncSession = Depends(get_db)) -> CountryRepo:
    return CountryRepo(db)