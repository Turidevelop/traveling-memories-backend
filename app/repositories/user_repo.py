from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select, update, delete, insert
from app.core.models import User
from app.database import get_db


class UserRepo:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_users(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_name(self, name: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.name == name))
        return result.scalar_one_or_none()

    async def create_user(self, data: dict) -> User:
        stmt = insert(User).values(**data).returning(User)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one()

    async def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        stmt = update(User).where(User.id == user_id).values(**user_data).returning(User)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> bool:
        result = await self.db.execute(delete(User).where(User.id == user_id))
        await self.db.commit()
        return result.rowcount > 0