from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from app.core.models import TripEntry
from fastapi import Depends
from app.database import get_db

class TripEntryRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_trip_entry(self, entry_data: dict) -> TripEntry:
        stmt = insert(TripEntry).values(**entry_data).returning(TripEntry)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def get_trip_entry_by_id(self, entry_id: int) -> TripEntry | None:
        stmt = select(TripEntry).where(TripEntry.id == entry_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_trip_entries(self) -> list[TripEntry]:
        stmt = select(TripEntry)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_trip_entries_by_trip_id(self, trip_id: int) -> list[TripEntry]:
        stmt = select(TripEntry).where(TripEntry.trip_id == trip_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

async def get_trip_entry_repo(db: AsyncSession = Depends(get_db)) -> TripEntryRepo:
    """
    Async dependency injector for TripEntryRepo.
    """
    return TripEntryRepo(db)