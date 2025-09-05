import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_trip(monkeypatch):
    # Mock TripService.create_trip para no depender de la BD real
    async def mock_create_trip(self, trip):
        return {
            "id": 1,
            "title": trip.title,
            "start_date": str(trip.start_date) if trip.start_date else None,
            "end_date": str(trip.end_date) if trip.end_date else None,
            "user_id": trip.user_id,
            "cover_photo_url": trip.cover_photo_url,
            "summary": trip.summary,
            "created_at": None
        }
    monkeypatch.setattr("app.services.trip_service.TripService.create_trip", mock_create_trip)

    trip_data = {
        "title": "Viaje de prueba",
        "start_date": "2025-08-28",
        "end_date": "2025-08-30",
        "user_id": 1,
        "cover_photo_url": "http://example.com/foto.jpg",
        "summary": "Un viaje de prueba."
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/trips", json=trip_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == trip_data["title"]
    assert data["user_id"] == trip_data["user_id"]

    assert data["summary"] == trip_data["summary"]


@pytest.mark.asyncio
async def test_get_trip_by_id_found(monkeypatch):
    # Mock TripService.get_trip_by_id para no depender de la BD real
    from app.core.schemas import TripOut
    async def mock_get_trip_by_id(self, trip_id):
        return TripOut(
            id=trip_id,
            title="Viaje de prueba",
            start_date="2025-08-28",
            end_date="2025-08-30",
            user_id=1,
            cover_photo_url="http://example.com/foto.jpg",
            summary="Un viaje de prueba.",
            created_at=None
        )
    monkeypatch.setattr("app.services.trip_service.TripService.get_trip_by_id", mock_get_trip_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/trips/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Viaje de prueba"


@pytest.mark.asyncio
async def test_get_trip_by_id_not_found(monkeypatch):
    async def mock_get_trip_by_id(self, trip_id):
        return None
    monkeypatch.setattr("app.services.trip_service.TripService.get_trip_by_id", mock_get_trip_by_id)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/trips/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Trip not found"
