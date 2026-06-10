from typing import List, Optional
from fastapi import Depends, HTTPException, status
from app.core.schemas import UserOut, UserCreate, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repo import UserRepo


class UserService:
    def __init__(self, repo: UserRepo = Depends()):
        self.repo = repo

    async def list_users(self) -> List[UserOut]:
        users = await self.repo.get_all_users()
        return [UserOut.model_validate(u) for u in users]

    async def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        user = await self.repo.get_user_by_id(user_id)
        return UserOut.model_validate(user) if user else None

    async def update_user(self, user_id: int, user_data: dict) -> Optional[UserOut]:
        user = await self.repo.update_user(user_id, user_data)
        return UserOut.model_validate(user) if user else None

    async def delete_user(self, user_id: int) -> bool:
        return await self.repo.delete_user(user_id)

    async def register(self, data: UserCreate) -> UserOut:
        existing = await self.repo.get_user_by_name(data.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
        payload = {
            "name": data.name,
            "password_hash": hash_password(data.password),
            "avatar_url": data.avatar_url,
            "bio": data.bio,
        }
        user = await self.repo.create_user(payload)
        return UserOut.model_validate(user)

    async def login(self, name: str, password: str) -> Token:
        user = await self.repo.get_user_by_name(name)
        if not user or not verify_password(password, user.password_hash or ""):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = create_access_token({"sub": str(user.id)})
        return Token(access_token=token)