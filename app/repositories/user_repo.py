from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select, update, delete
from app.core.models import User
from app.database import get_db

class UserRepo:
    """
    Repository for user data access. Uses SQLAlchemy ORM for scalability and maintainability.
    """
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_users(self) -> List[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return users

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        stmt = update(User).where(User.id == user_id).values(**user_data).returning(User)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> bool:
        stmt = delete(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0
