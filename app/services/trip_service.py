from fastapi import Depends, HTTPException, status
from app.repositories.trip_repo import TripRepo, get_trip_repo
from app.core.schemas import TripCreate, TripOut


class TripService:
    """
    Application service for Trip use cases.
    """
    def __init__(self, repo: TripRepo):
        self.repo = repo

    async def create_trip(self, trip: TripCreate, current_user_id: int) -> TripOut:
        data = trip.model_dump()
        data["user_id"] = current_user_id  # fuerza el dueño = usuario del token
        trip_obj = await self.repo.create_trip(data)
        return TripOut.model_validate(trip_obj)

    async def get_trip_by_id(self, trip_id: int) -> TripOut | None:
        trip = await self.repo.get_trip_by_id(trip_id)
        if trip is None:
            return None
        return TripOut.model_validate(trip)

    async def get_trips_by_user_id(self, user_id: int) -> list[TripOut]:
        trips = await self.repo.get_trips_by_user_id(user_id)
        return [TripOut.model_validate(trip) for trip in trips]

    async def update_trip(self, trip_id: int, trip: TripCreate, current_user_id: int) -> TripOut | None:
        existing = await self.repo.get_trip_by_id(trip_id)
        if existing is None:
            return None
        if existing.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes modificar un viaje que no es tuyo",
            )
        data = trip.model_dump()
        data["user_id"] = current_user_id  # evita que se reasigne a otro usuario
        trip_obj = await self.repo.update_trip(trip_id, data)
        if trip_obj is None:
            return None
        return TripOut.model_validate(trip_obj)

    async def delete_trip(self, trip_id: int, current_user_id: int) -> bool:
        existing = await self.repo.get_trip_by_id(trip_id)
        if existing is None:
            return False
        if existing.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes eliminar un viaje que no es tuyo",
            )
        return await self.repo.delete_trip(trip_id)


def get_trip_service(
    repo: TripRepo = Depends(get_trip_repo),
) -> TripService:
    """
    Dependency injector for TripService.
    """
    return TripService(repo)