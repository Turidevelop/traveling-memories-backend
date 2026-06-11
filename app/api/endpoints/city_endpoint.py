from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import CityCreate, CityOut
from app.services.city_service import CityService, get_city_service
from typing import List
from app.core.security import require_auth

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    dependencies=[Depends(require_auth)]
)

@router.post(
    "",
    response_model=CityOut,
    status_code=status.HTTP_201_CREATED
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
    "",
    response_model=List[CityOut]
)
async def list_cities(
    service: CityService = Depends(get_city_service)
) -> List[CityOut]:
    """
    Get all cities.
    """
    return await service.get_all_cities()

@router.get(
    "/{city_id}",
    response_model=CityOut
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

@router.put(
    "/{city_id}",
    response_model=CityOut
)
async def update_city(
    city_id: int,
    data: CityCreate,
    service: CityService = Depends(get_city_service)
) -> CityOut:
    """
    Update a city by its ID.
    """
    updated_city = await service.update_city(city_id, data)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city

@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_city(
    city_id: int,
    service: CityService = Depends(get_city_service)
) -> None:
    """
    Delete a city by its ID.
    """
    deleted = await service.delete_city(city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city