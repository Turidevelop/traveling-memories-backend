from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import CityCreate, CityOut
from app.services.city_service import CityService, get_city_service
from typing import List

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

@router.get(
    "/cities",
    response_model=List[CityOut],
    tags=["cities"]
)
async def list_cities(
    service: CityService = Depends(get_city_service)
) -> List[CityOut]:
    """
    Get all cities.
    """
    return await service.get_all_cities()

@router.get(
    "/cities/{city_id}",
    response_model=CityOut,
    tags=["cities"]
)
async def get_city_by_id(
    city_id: int,
    service: CityService = Depends(get_city_service)
) -> CityOut:
    """
    Get a city by its ID.
    """
    city = await service.get_city_by_id(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city