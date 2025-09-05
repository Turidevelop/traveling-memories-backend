from fastapi import Depends
from app.repositories.trip_entry_repo import TripEntryRepo, get_trip_entry_repo
from app.core.schemas import TripEntryCreate, TripEntryOut

class TripEntryService:
    def __init__(self, repo: TripEntryRepo):
        self.repo = repo

    async def create_trip_entry(self, entry: TripEntryCreate) -> TripEntryOut:
        entry_obj = await self.repo.create_trip_entry(entry.model_dump())
        return TripEntryOut.model_validate(entry_obj)

def get_trip_entry_service(
    repo: TripEntryRepo = Depends(get_trip_entry_repo),
) -> TripEntryService:
    return TripEntryService(repo)