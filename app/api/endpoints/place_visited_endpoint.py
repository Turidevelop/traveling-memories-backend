from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import PlaceVisitedCreate, PlaceVisitedOut
from app.services.place_visited_service import PlaceVisitedService, get_place_visited_service
from app.core.security import validate_api_key

router = APIRouter(
    prefix="/places-visited",
    tags=["Places Visited"],
    dependencies=[Depends(validate_api_key)]
)

@router.post(
    "",
    response_model=PlaceVisitedOut,
    status_code=status.HTTP_201_CREATED
)
async def create_place_visited(
    data: PlaceVisitedCreate,
    service: PlaceVisitedService = Depends(get_place_visited_service)
) -> PlaceVisitedOut:
    """
    Create a new place visited.
    """
    return await service.create_place_visited(data)

@router.get(
    "/{place_visited_id}",
    response_model=PlaceVisitedOut
)
async def get_place_visited_by_id(
    place_visited_id: int,
    service: PlaceVisitedService = Depends(get_place_visited_service)
) -> PlaceVisitedOut:
    """
    Get a place visited by its ID.
    """
    obj = await service.get_place_visited_by_id(place_visited_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="PlaceVisited not found")
    return obj