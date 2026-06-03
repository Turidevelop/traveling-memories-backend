from typing import List, Optional
from fastapi import Depends
from app.core.schemas import UserOut
from app.repositories.user_repo import UserRepo

class UserService:
    """
    Service layer for user-related business logic. Uses repository pattern for scalability and testability.
    """
    def __init__(self, repo: UserRepo = Depends()):
        self.repo = repo

    async def list_users(self) -> List[UserOut]:
        users = await self.repo.get_all_users()
        return [UserOut.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        user = await self.repo.get_user_by_id(user_id)
        if user:
            return UserOut.model_validate(user)
        return None

    async def update_user(self, user_id: int, user_data: dict) -> Optional[UserOut]:
        user = await self.repo.update_user(user_id, user_data)
        if user:
            return UserOut.model_validate(user)
        return None

    async def delete_user(self, user_id: int) -> bool:
        return await self.repo.delete_user(user_id)
