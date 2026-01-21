
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.schemas import CountryOut
from app.core.config import settings

API_KEY = settings.API_KEY
HEADERS = {"X-API-KEY": API_KEY}

@pytest.mark.asyncio
async def test_create_country(monkeypatch):
    async def mock_create_country(self, data):
        return CountryOut(
            id=1,
            name=data.name
        )
    monkeypatch.setattr(
        "app.services.country_service.CountryService.create_country",
        mock_create_country
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "name": "España"
        }
        response = await ac.post("/countries", json=payload, headers=HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "España"

@pytest.mark.asyncio
async def test_list_countries(monkeypatch):
    async def mock_get_all_countries(self):
        return [
            CountryOut(id=1, name="España"),
            CountryOut(id=2, name="Francia")
        ]
    monkeypatch.setattr(
        "app.services.country_service.CountryService.get_all_countries",
        mock_get_all_countries
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/countries", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "España"
    assert data[1]["name"] == "Francia"

@pytest.mark.asyncio
async def test_get_country_by_id(monkeypatch):
    async def mock_get_country_by_id(self, country_id):
        if country_id == 1:
            return CountryOut(id=1, name="España")
        return None
    monkeypatch.setattr(
        "app.services.country_service.CountryService.get_country_by_id",
        mock_get_country_by_id
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/countries/1", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "España"

    # Test country not found
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/countries/999", headers=HEADERS)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Country not found"