from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
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
