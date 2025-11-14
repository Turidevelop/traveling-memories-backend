from fastapi import Depends
from app.repositories.city_repo import CityRepo, get_city_repo
from app.core.schemas import CityCreate, CityOut

class CityService:
    def __init__(self, repo: CityRepo):
        self.repo = repo

    async def create_city(self, data: CityCreate) -> CityOut:
        obj = await self.repo.create_city(data.model_dump())
        return CityOut.model_validate(obj)

async def get_city_service(repo: CityRepo = Depends(get_city_repo)) -> CityService:
    return CityService(repo)