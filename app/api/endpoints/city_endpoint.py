from fastapi import APIRouter, Depends, status
from app.core.schemas import CityCreate, CityOut
from app.services.city_service import CityService, get_city_service

router = APIRouter()

@router.post(
    "/cities",
    response_model=CityOut,
    status_code=status.HTTP_201_CREATED,
    tags=["cities"]
)
async def create_city(
    data: CityCreate,
    service: CityService = Depends(get_city_service)
) -> CityOut:
    """
    Create a new city with name, lat, lng and country_id.
    """
    return await service.create_city(data)