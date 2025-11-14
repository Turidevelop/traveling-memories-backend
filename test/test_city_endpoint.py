import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.schemas import CityOut

@pytest.mark.asyncio
async def test_create_city(monkeypatch):
    async def mock_create_city(self, data):
        return CityOut(
            id=1,
            name=data.name,
            lat=data.lat,
            lng=data.lng,
            country_id=data.country_id
        )
    monkeypatch.setattr(
        "app.services.city_service.CityService.create_city",
        mock_create_city
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "name": "Madrid",
            "lat": 40.4168,
            "lng": -3.7038,
            "country_id": 1
        }
        response = await ac.post("/cities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Madrid"
    assert data["lat"] == 40.4168
    assert data["lng"] == -3.7038
    assert data["country_id"] == 1