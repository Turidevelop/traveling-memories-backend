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
