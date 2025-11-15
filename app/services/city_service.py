
from fastapi import Depends
from app.repositories.city_repo import CityRepo, get_city_repo
from app.core.schemas import CityCreate, CityOut

class CityService:
    def __init__(self, repo: CityRepo):
        self.repo = repo


    async def create_city(self, data: CityCreate) -> CityOut:
        obj = await self.repo.create_city(data.model_dump())
        return CityOut.model_validate(obj)

    async def get_all_cities(self) -> list[CityOut]:
        cities = await self.repo.get_all_cities()
        return [CityOut.model_validate(city) for city in cities]

    async def get_city_by_id(self, city_id: int) -> CityOut | None:
        city = await self.repo.get_city_by_id(city_id)
        if city is None:
            return None
        return CityOut.model_validate(city)

async def get_city_service(repo: CityRepo = Depends(get_city_repo)) -> CityService:
    return CityService(repo)