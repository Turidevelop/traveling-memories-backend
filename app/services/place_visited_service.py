from typing import List
from fastapi import Depends, HTTPException, status
from app.core.schemas import PlaceVisitedCreate, PlaceVisitedOut
from app.repositories.place_visited_repo import PlaceVisitedRepo
from app.repositories.trip_repo import TripRepo, get_trip_repo


class PlaceVisitedService:
    def __init__(
        self,
        repo: PlaceVisitedRepo = Depends(),
        trip_repo: TripRepo = Depends(get_trip_repo),
    ):
        self.repo = repo
        self.trip_repo = trip_repo

    async def _check_trip_ownership(self, trip_id: int, current_user_id: int) -> None:
        """Comprueba que el trip padre pertenece al usuario; lanza 403 si no."""
        trip = await self.trip_repo.get_trip_by_id(trip_id)
        if trip is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        if trip.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes modificar lugares de un viaje que no es tuyo",
            )

    async def get_by_trip(self, trip_id: int) -> List[PlaceVisitedOut]:
        places = await self.repo.get_by_trip(trip_id)
        return [PlaceVisitedOut.model_validate(p) for p in places]

    async def create(self, data: PlaceVisitedCreate, current_user_id: int) -> PlaceVisitedOut:
        # el trip al que se añade el lugar debe ser del usuario
        await self._check_trip_ownership(data.trip_id, current_user_id)
        place = await self.repo.create(data.model_dump())
        return PlaceVisitedOut.model_validate(place)

    async def delete(self, place_id: int, current_user_id: int) -> None:
        existing = await self.repo.get_by_id(place_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
        await self._check_trip_ownership(existing.trip_id, current_user_id)
        deleted = await self.repo.delete(place_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")