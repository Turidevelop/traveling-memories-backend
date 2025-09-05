import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.schemas import TripEntryOut

@pytest.mark.asyncio
async def test_create_trip_entry(monkeypatch):
    """
    Test POST /trip-entries endpoint for creating a trip entry.
    """
    async def mock_create_trip_entry(self, entry):
        return TripEntryOut(
            id=1,
            trip_id=entry.trip_id,
            entry_date=entry.entry_date,
            title=entry.title,
            content=entry.content
        )
    monkeypatch.setattr(
        "app.services.trip_entry_service.TripEntryService.create_trip_entry",
        mock_create_trip_entry
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "trip_id": 1,
            "entry_date": "2025-09-05",
            "title": "Mi primer día",
            "content": "Hoy visité muchos lugares interesantes."
        }
        response = await ac.post("/trip-entries", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["trip_id"] == 1
    assert data["entry_date"] == "2025-09-05"
    assert data["title"] == "Mi primer día"
    assert data["content"] == "Hoy visité muchos lugares interesantes."