from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

# test/test_users_endpoint.py
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], list)

def test_get_user_by_id_found(monkeypatch):
    async def mock_get_user_by_id(self, user_id):
        return {"id": 1, "name": "Test User", "avatar_url": None, "bio": None}
    monkeypatch.setattr("app.services.users_service.UsersService.get_user_by_id", mock_get_user_by_id)
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test User"

def test_get_user_by_id_not_found(monkeypatch):
    async def mock_get_user_by_id(self, user_id):
        return None
    monkeypatch.setattr("app.services.users_service.UsersService.get_user_by_id", mock_get_user_by_id)
    response = client.get("/users/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

