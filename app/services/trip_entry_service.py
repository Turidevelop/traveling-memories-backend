from fastapi import Depends, HTTPException, status
from app.repositories.trip_entry_repo import TripEntryRepo, get_trip_entry_repo
from app.repositories.trip_repo import TripRepo, get_trip_repo
from app.core.schemas import TripEntryCreate, TripEntryOut


class TripEntryService:
    def __init__(self, repo: TripEntryRepo, trip_repo: TripRepo):
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
                detail="No puedes modificar entradas de un viaje que no es tuyo",
            )

    async def create_trip_entry(self, entry: TripEntryCreate, current_user_id: int) -> TripEntryOut:
        # el trip al que se añade la entrada debe ser del usuario
        await self._check_trip_ownership(entry.trip_id, current_user_id)
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

    async def update_trip_entry(self, entry_id: int, entry: TripEntryCreate, current_user_id: int) -> TripEntryOut | None:
        existing = await self.repo.get_trip_entry_by_id(entry_id)
        if existing is None:
            return None
        # propiedad a través del trip padre de la entrada existente
        await self._check_trip_ownership(existing.trip_id, current_user_id)
        entry_obj = await self.repo.update_trip_entry(entry_id, entry.model_dump())
        if entry_obj is None:
            return None
        return TripEntryOut.model_validate(entry_obj)

    async def delete_trip_entry(self, entry_id: int, current_user_id: int) -> bool:
        existing = await self.repo.get_trip_entry_by_id(entry_id)
        if existing is None:
            return False
        await self._check_trip_ownership(existing.trip_id, current_user_id)
        return await self.repo.delete_trip_entry(entry_id)


def get_trip_entry_service(
    repo: TripEntryRepo = Depends(get_trip_entry_repo),
    trip_repo: TripRepo = Depends(get_trip_repo),
) -> TripEntryService:
    return TripEntryService(repo, trip_repo)