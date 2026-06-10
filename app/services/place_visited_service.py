from typing import List, Optional
from fastapi import Depends, HTTPException, status
from app.core.schemas import PlaceVisitedCreate, PlaceVisitedOut
from app.repositories.place_visited_repo import PlaceVisitedRepo


class PlaceVisitedService:
    def __init__(self, repo: PlaceVisitedRepo = Depends()):
        self.repo = repo

    async def get_by_trip(self, trip_id: int) -> List[PlaceVisitedOut]:
        places = await self.repo.get_by_trip(trip_id)
        return [PlaceVisitedOut.model_validate(p) for p in places]

    async def create(self, data: PlaceVisitedCreate) -> PlaceVisitedOut:
        place = await self.repo.create(data.model_dump())
        return PlaceVisitedOut.model_validate(place)

    async def delete(self, place_id: int) -> None:
        deleted = await self.repo.delete(place_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")