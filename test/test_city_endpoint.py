
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.schemas import CityOut

@pytest.mark.asyncio
async def test_list_cities(monkeypatch):
    async def mock_get_all_cities(self):
        return [
            CityOut(id=1, name="Madrid", lat=40.4168, lng=-3.7038, country_id=1),
            CityOut(id=2, name="Barcelona", lat=41.3874, lng=2.1686, country_id=1)
        ]
    monkeypatch.setattr(
        "app.services.city_service.CityService.get_all_cities",
        mock_get_all_cities
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Madrid"
    assert data[1]["name"] == "Barcelona"

@pytest.mark.asyncio
async def test_get_city_by_id(monkeypatch):
    async def mock_get_city_by_id(self, city_id):
        if city_id == 1:
            return CityOut(id=1, name="Madrid", lat=40.4168, lng=-3.7038, country_id=1)
        return None
    monkeypatch.setattr(
        "app.services.city_service.CityService.get_city_by_id",
        mock_get_city_by_id
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cities/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Madrid"
    assert data["lat"] == 40.4168
    assert data["lng"] == -3.7038
    assert data["country_id"] == 1

    # Test city not found
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/cities/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "City not found"

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