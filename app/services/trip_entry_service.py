from fastapi import Depends
from app.repositories.trip_entry_repo import TripEntryRepo, get_trip_entry_repo
from app.core.schemas import TripEntryCreate, TripEntryOut

class TripEntryService:
    def __init__(self, repo: TripEntryRepo):
        self.repo = repo

    async def create_trip_entry(self, entry: TripEntryCreate) -> TripEntryOut:
        entry_obj = await self.repo.create_trip_entry(entry.model_dump())
        return TripEntryOut.model_validate(entry_obj)

    async def get_trip_entry_by_id(self, entry_id: int) -> TripEntryOut | None:
        entry = await self.repo.get_trip_entry_by_id(entry_id)
        if entry is None:
            return None
        return TripEntryOut.model_validate(entry)

    async def get_all_trip_entries(self) -> list[TripEntryOut]:
        entries = await self.repo.get_all_trip_entries()
        return [TripEntryOut.model_validate(entry) for entry in entries]

    async def get_trip_entries_by_trip_id(self, trip_id: int) -> list[TripEntryOut]:
        entries = await self.repo.get_trip_entries_by_trip_id(trip_id)
        return [TripEntryOut.model_validate(entry) for entry in entries]

def get_trip_entry_service(
    repo: TripEntryRepo = Depends(get_trip_entry_repo),
) -> TripEntryService:
    return TripEntryService(repo)