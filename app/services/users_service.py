from typing import List
from fastapi import Depends
from app.core.schemas import AppUser
from app.repositorires.users_repo import UsersRepo

class UsersService:
    """
    Service layer for user-related business logic. Uses repository pattern for scalability and testability.
    """
    def __init__(self, repo: UsersRepo = Depends()):
        self.repo = repo

    async def list_users(self) -> List[AppUser]:
        users = await self.repo.get_all_users()
        return [AppUser.model_validate(user) for user in users]
