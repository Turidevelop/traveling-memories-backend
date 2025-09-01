from fastapi import Depends
from app.repositories.trip_repo import TripRepo, get_trip_repo
from app.core.schemas import TripCreate, TripOut


class TripService:
    """
    Application service for Trip use cases.
    """
    def __init__(self, repo: TripRepo):
        self.repo = repo

    async def create_trip(self, trip: TripCreate) -> TripOut:
        trip_obj = await self.repo.create_trip(trip.model_dump())
        return TripOut.model_validate(trip_obj)
    
    async def get_trip_by_id(self, trip_id: int) -> TripOut | None:
        trip = await self.repo.get_trip_by_id(trip_id)
        if trip is None:
            return None
        return TripOut.model_validate(trip)

def get_trip_service(
    repo: TripRepo = Depends(get_trip_repo),
) -> TripService:
    """
    Dependency injector for TripService.
    """
    return TripService(repo)