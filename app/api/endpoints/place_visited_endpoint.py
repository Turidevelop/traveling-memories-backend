from fastapi import APIRouter, Depends
from app.core.schemas import PlaceVisitedCreate, PlaceVisitedOut
from app.core.security import require_auth, get_current_user_id
from app.services.place_visited_service import PlaceVisitedService

router = APIRouter(prefix="/places-visited", tags=["Places Visited"])


@router.get(
    "/trip/{trip_id}",
    response_model=list[PlaceVisitedOut],
    dependencies=[Depends(require_auth)],
)
async def get_by_trip(
    trip_id: int,
    service: PlaceVisitedService = Depends(),
) -> list[PlaceVisitedOut]:
    """Get all places visited for a trip (open to any authenticated user)."""
    return await service.get_by_trip(trip_id)


@router.post("/", response_model=PlaceVisitedOut, status_code=201)
async def create(
    data: PlaceVisitedCreate,
    service: PlaceVisitedService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> PlaceVisitedOut:
    """Create a place visited (only on your own trips)."""
    return await service.create(data, current_user_id)


@router.delete("/{place_id}", status_code=204)
async def delete(
    place_id: int,
    service: PlaceVisitedService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> None:
    """Delete a place visited (only on your own trips)."""
    await service.delete(place_id, current_user_id)