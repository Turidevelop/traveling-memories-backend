from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import TripEntryCreate, TripEntryOut
from app.services.trip_entry_service import TripEntryService, get_trip_entry_service
from app.core.security import require_auth, get_current_user_id

router = APIRouter(prefix="/trip-entries", tags=["Trip Entries"])


@router.post("", response_model=TripEntryOut, status_code=status.HTTP_201_CREATED)
async def create_trip_entry(
    entry: TripEntryCreate,
    service: TripEntryService = Depends(get_trip_entry_service),
    current_user_id: int = Depends(get_current_user_id),
) -> TripEntryOut:
    """Create a new trip entry (only on your own trips)."""
    return await service.create_trip_entry(entry, current_user_id)


@router.get("", response_model=list[TripEntryOut], dependencies=[Depends(require_auth)])
async def get_all_trip_entries(
    service: TripEntryService = Depends(get_trip_entry_service),
) -> list[TripEntryOut]:
    """Get all trip entries (open to any authenticated user)."""
    return await service.get_all_trip_entries()


@router.get("/{entry_id}", response_model=TripEntryOut, dependencies=[Depends(require_auth)])
async def get_trip_entry_by_id(
    entry_id: int,
    service: TripEntryService = Depends(get_trip_entry_service),
) -> TripEntryOut:
    """Get a trip entry by its ID (open to any authenticated user)."""
    entry = await service.get_trip_entry_by_id(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Trip entry not found")
    return entry


@router.get("/trip/{trip_id}", response_model=list[TripEntryOut], dependencies=[Depends(require_auth)])
async def get_trip_entries_by_trip_id(
    trip_id: int,
    service: TripEntryService = Depends(get_trip_entry_service),
) -> list[TripEntryOut]:
    """Get all trip entries for a specific trip (open to any authenticated user)."""
    return await service.get_trip_entries_by_trip_id(trip_id)


@router.put("/{entry_id}", response_model=TripEntryOut)
async def update_trip_entry(
    entry_id: int,
    entry: TripEntryCreate,
    service: TripEntryService = Depends(get_trip_entry_service),
    current_user_id: int = Depends(get_current_user_id),
) -> TripEntryOut:
    """Update a trip entry (only on your own trips)."""
    updated_entry = await service.update_trip_entry(entry_id, entry, current_user_id)
    if updated_entry is None:
        raise HTTPException(status_code=404, detail="Trip entry not found")
    return updated_entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip_entry(
    entry_id: int,
    service: TripEntryService = Depends(get_trip_entry_service),
    current_user_id: int = Depends(get_current_user_id),
) -> None:
    """Delete a trip entry (only on your own trips)."""
    deleted = await service.delete_trip_entry(entry_id, current_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Trip entry not found")