from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import TripCreate, TripOut
from app.services.trip_service import TripService, get_trip_service
from app.core.security import require_auth


router = APIRouter(
    prefix="/trips",
    tags=["Trips"],
    dependencies=[Depends(require_auth)]
)

@router.post(
    "",
    response_model=TripOut,
    status_code=status.HTTP_201_CREATED
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
    "/user/{user_id}",
    response_model=list[TripOut]
)
async def get_trips_by_user_id(
    user_id: int,
    service: TripService = Depends(get_trip_service)
) -> list[TripOut]:
    """
    Get all trips for a specific user.
    """
    return await service.get_trips_by_user_id(user_id)

@router.get(
    "/{trip_id}",
    response_model=TripOut
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

@router.put(
    "/{trip_id}",
    response_model=TripOut
)
async def update_trip(
    trip_id: int,
    trip: TripCreate,
    service: TripService = Depends(get_trip_service)
) -> TripOut:
    """
    Update a trip by its ID.
    """
    updated_trip = await service.update_trip(trip_id, trip)
    if updated_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return updated_trip

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(
    trip_id: int,
    service: TripService = Depends(get_trip_service)
) -> None:
    deleted = await service.delete_trip(trip_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Trip not found")