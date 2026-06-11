from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import UserService
from app.core.schemas import UserOut
from app.core.security import require_auth

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_auth)]
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

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_data: dict,
    service: UserService = Depends()
) -> UserOut:
    """
    Update a user by its ID.
    """
    updated_user = await service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends()
) -> None:
    """
    Delete a user by its ID.
    """
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")


