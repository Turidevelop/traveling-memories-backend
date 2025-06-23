from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
from app.core.models import User
from app.database import get_db

class UsersRepo:
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
