from fastapi import Depends
from app.repositories.country_repo import CountryRepo, get_country_repo
from app.core.schemas import CountryCreate, CountryOut


class CountryService:
    def __init__(self, repo: CountryRepo):
        self.repo = repo

    async def create_country(self, data: CountryCreate) -> CountryOut:
        obj = await self.repo.create_country(data.model_dump())
        return CountryOut.model_validate(obj)

    async def get_all_countries(self) -> list[CountryOut]:
        countries = await self.repo.get_all_countries()
        return [CountryOut.model_validate(c) for c in countries]

    async def get_country_by_id(self, country_id: int) -> CountryOut | None:
        country = await self.repo.get_country_by_id(country_id)
        if country is None:
            return None
        return CountryOut.model_validate(country)

async def get_country_service(repo: CountryRepo = Depends(get_country_repo)) -> CountryService:
    return CountryService(repo)