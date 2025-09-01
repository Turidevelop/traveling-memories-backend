from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import TripCreate, TripOut
from app.services.trip_service import TripService, get_trip_service

router = APIRouter()

@router.post(
    "/trips",
    response_model=TripOut,
    status_code=status.HTTP_201_CREATED,
    tags=["trips"]
)
async def create_trip(
    trip: TripCreate,
    service: TripService = Depends(get_trip_service)
) -> TripOut:
    """
    Create a new trip.
    """
    return await service.create_trip(trip)

@router.get(
    "/trips/{trip_id}",
    response_model=TripOut,
    tags=["trips"]
)
async def get_trip_by_id(
    trip_id: int,
    service: TripService = Depends(get_trip_service)
) -> TripOut:
    """
    Get a trip by its ID.
    """
    trip = await service.get_trip_by_id(trip_id)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip