import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.schemas import PlaceVisitedOut

@pytest.mark.asyncio
async def test_create_place_visited(monkeypatch):
    """
    Test POST /places-visited endpoint for creating a place visited.
    """
    async def mock_create_place_visited(self, data):
        return PlaceVisitedOut(
            id=1,
            trip_id=data.trip_id,
            country_id=data.country_id,
            city_id=data.city_id
        )
    monkeypatch.setattr(
        "app.services.place_visited_service.PlaceVisitedService.create_place_visited",
        mock_create_place_visited
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "trip_id": 1,
            "country_id": 2,
            "city_id": 3
        }
        response = await ac.post("/places-visited", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["trip_id"] == 1
    assert data["country_id"] == 2
    assert data["city_id"] == 3