
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], list)


@pytest.mark.asyncio
async def test_get_user_by_id_found(monkeypatch):
    async def mock_get_user_by_id(self, user_id):
        return {"id": 1, "name": "Test User", "avatar_url": None, "bio": None}
    monkeypatch.setattr("app.services.users_service.UsersService.get_user_by_id", mock_get_user_by_id)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(monkeypatch):
    async def mock_get_user_by_id(self, user_id):
        return None
    monkeypatch.setattr("app.services.users_service.UsersService.get_user_by_id", mock_get_user_by_id)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

