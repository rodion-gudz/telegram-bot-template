from abc import ABC

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from .models import User


class DB(AsyncSession, ABC):
    async def is_registered(self, user_id: int) -> bool:
        q = exists(select(User.id).where(User.id == user_id)).select()
        return await self.scalar(q)

    async def register(self, user_id) -> User:
        user = User(id=user_id)
        self.add(user)
        await self.commit()
        return user

    async def get_users_count(self):
        q = func.count(User.id)
        return await self.scalar(q)
