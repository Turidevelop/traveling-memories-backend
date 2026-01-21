from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import UserService
from app.core.schemas import UserOut
from app.core.security import validate_api_key

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(validate_api_key)]
)

@router.get("", response_model=dict)
async def get_users(service: UserService = Depends()) -> dict:
    """
    Returns a JSON object with the list of users under the 'users' key.
    """
    users = await service.list_users()
    return {"response": users}

@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, service: UserService = Depends()) -> UserOut:
    """
    Returns a single user by ID.
    """
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


