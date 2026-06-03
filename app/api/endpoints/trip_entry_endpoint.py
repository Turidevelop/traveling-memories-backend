from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import TripEntryCreate, TripEntryOut
from app.services.trip_entry_service import TripEntryService, get_trip_entry_service
from app.core.security import validate_api_key

router = APIRouter(
    prefix="/trip-entries",
    tags=["Trip Entries"],
    dependencies=[Depends(validate_api_key)]
)

@router.post(
    "",
    response_model=TripEntryOut,
    status_code=status.HTTP_201_CREATED
)
async def create_trip_entry(
    entry: TripEntryCreate,
    service: TripEntryService = Depends(get_trip_entry_service)
) -> TripEntryOut:
    """
    Create a new trip entry.
    """
    return await service.create_trip_entry(entry)

@router.get(
    "",
    response_model=list[TripEntryOut]
)
async def get_all_trip_entries(
    service: TripEntryService = Depends(get_trip_entry_service)
) -> list[TripEntryOut]:
    """
    Get all trip entries.
    """
    return await service.get_all_trip_entries()

@router.get(
    "/{entry_id}",
    response_model=TripEntryOut
)
async def get_trip_entry_by_id(
    entry_id: int,
    service: TripEntryService = Depends(get_trip_entry_service)
) -> TripEntryOut:
    """
    Get a trip entry by its ID.
    """
    entry = await service.get_trip_entry_by_id(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Trip entry not found")
    return entry

@router.get(
    "/trip/{trip_id}",
    response_model=list[TripEntryOut]
)
async def get_trip_entries_by_trip_id(
    trip_id: int,
    service: TripEntryService = Depends(get_trip_entry_service)
) -> list[TripEntryOut]:
    """
    Get all trip entries for a specific trip.
    """
    return await service.get_trip_entries_by_trip_id(trip_id)