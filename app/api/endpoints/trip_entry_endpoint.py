from fastapi import APIRouter, Depends, status
from app.core.schemas import TripEntryCreate, TripEntryOut
from app.services.trip_entry_service import TripEntryService, get_trip_entry_service

router = APIRouter()

@router.post(
    "/trip-entries",
    response_model=TripEntryOut,
    status_code=status.HTTP_201_CREATED,
    tags=["trip_entries"]
)
async def create_trip_entry(
    entry: TripEntryCreate,
    service: TripEntryService = Depends(get_trip_entry_service)
) -> TripEntryOut:
    """
    Create a new trip entry.
    """
    return await service.create_trip_entry(entry)