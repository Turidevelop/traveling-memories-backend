from fastapi import APIRouter, Depends
from app.services.users_service import UsersService
from app.core.schemas import AppUser
from typing import List

router = APIRouter()

@router.get("/users", response_model=dict, tags=["users"])
async def get_users(service: UsersService = Depends()) -> dict:
    """
    Returns a JSON object with the list of users under the 'users' key.
    """
    users = await service.list_users()
    return {"users": users}


