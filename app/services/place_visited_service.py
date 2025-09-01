from fastapi import Depends
from app.repositories.place_visited_repo import PlaceVisitedRepo, get_place_visited_repo
from app.core.schemas import PlaceVisitedCreate, PlaceVisitedOut

class PlaceVisitedService:
    def __init__(self, repo: PlaceVisitedRepo):
        self.repo = repo

    async def create_place_visited(self, data: PlaceVisitedCreate) -> PlaceVisitedOut:
        obj = await self.repo.create(data.model_dump())
        return PlaceVisitedOut.model_validate(obj)

    async def get_place_visited_by_id(self, place_visited_id: int) -> PlaceVisitedOut | None:
        obj = await self.repo.get_by_id(place_visited_id)
        if obj is None:
            return None
        return PlaceVisitedOut.model_validate(obj)

def get_place_visited_service(
    repo: PlaceVisitedRepo = Depends(get_place_visited_repo),
) -> PlaceVisitedService:
    return PlaceVisitedService(repo)