
from fastapi import APIRouter, Depends, status, HTTPException
from app.core.schemas import CountryCreate, CountryOut
from app.services.country_service import CountryService, get_country_service
from typing import List
from app.core.security import require_auth

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
    dependencies=[Depends(require_auth)]
)

@router.post(
    "",
    response_model=CountryOut,
    status_code=status.HTTP_201_CREATED
)
async def create_country(
    data: CountryCreate,
    service: CountryService = Depends(get_country_service)
) -> CountryOut:
    """
    Create a new country with name.
    """
    return await service.create_country(data)

@router.get(
    "",
    response_model=List[CountryOut]
)
async def list_countries(
    service: CountryService = Depends(get_country_service)
) -> List[CountryOut]:
    """
    Get all countries.
    """
    return await service.get_all_countries()

@router.get(
    "/{country_id}",
    response_model=CountryOut
)
async def get_country_by_id(
    country_id: int,
    service: CountryService = Depends(get_country_service)
) -> CountryOut:
    """
    Get a country by its ID.
    """
    country = await service.get_country_by_id(country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.put(
    "/{country_id}",
    response_model=CountryOut
)
async def update_country(
    country_id: int,
    data: CountryCreate,
    service: CountryService = Depends(get_country_service)
) -> CountryOut:
    """
    Update a country by its ID.
    """
    updated_country = await service.update_country(country_id, data)
    if updated_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return updated_country

@router.delete(
    "/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_country(
    country_id: int,
    service: CountryService = Depends(get_country_service)
) -> None:
    """
    Delete a country by its ID.
    """
    deleted = await service.delete_country(country_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    country = await service.get_country_by_id(country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

