from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.core.schemas import UserOut
from typing import List

router = APIRouter()

@router.get("/users", response_model=dict, tags=["users"])
async def get_users(service: UserService = Depends()) -> dict:
    """
    Returns a JSON object with the list of users under the 'users' key.
    """
    users = await service.list_users()
    return {"response": users}

@router.get("/user/{user_id}", response_model=UserOut, tags=["user"])
async def get_user_by_id(user_id: int, service: UserService = Depends()) -> UserOut:
    """
    Returns a single user by ID.
    """
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


