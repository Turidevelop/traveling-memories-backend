import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.schemas import CountryOut

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
        response = await ac.post("/countries", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "España"