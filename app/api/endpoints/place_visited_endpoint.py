from fastapi import APIRouter, Depends
from app.core.schemas import PlaceVisitedCreate, PlaceVisitedOut
from app.core.security import require_auth
from app.services.place_visited_service import PlaceVisitedService

router = APIRouter(
    prefix="/places-visited",
    tags=["Places Visited"],
    dependencies=[Depends(require_auth)]
)

@router.get("/trip/{trip_id}", response_model=list[PlaceVisitedOut])
async def get_by_trip(trip_id: int, service: PlaceVisitedService = Depends()) -> list[PlaceVisitedOut]:
    return await service.get_by_trip(trip_id)

@router.post("/", response_model=PlaceVisitedOut, status_code=201)
async def create(data: PlaceVisitedCreate, service: PlaceVisitedService = Depends()) -> PlaceVisitedOut:
    return await service.create(data)

@router.delete("/{place_id}", status_code=204)
async def delete(place_id: int, service: PlaceVisitedService = Depends()) -> None:
    await service.delete(place_id)