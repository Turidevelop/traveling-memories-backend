from fastapi import APIRouter, Depends, status
from app.core.schemas import CountryCreate, CountryOut
from app.services.country_service import CountryService, get_country_service

router = APIRouter()

@router.post(
    "/countries",
    response_model=CountryOut,
    status_code=status.HTTP_201_CREATED,
    tags=["countries"]
)
async def create_country(
    data: CountryCreate,
    service: CountryService = Depends(get_country_service)
) -> CountryOut:
    """
    Create a new country with name.
    """
    return await service.create_country(data)

