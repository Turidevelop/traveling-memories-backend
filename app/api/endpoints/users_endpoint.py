from fastapi import APIRouter, Depends, HTTPException
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
    return {"response": users}

@router.get("/users/{user_id}", response_model=AppUser, tags=["users"])
async def get_user_by_id(user_id: int, service: UsersService = Depends()) -> AppUser:
    """
    Returns a single user by ID.
    """
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


