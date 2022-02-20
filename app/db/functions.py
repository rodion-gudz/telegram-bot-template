from abc import ABC

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class DB(AsyncSession, ABC):
    async def is_registered(self, user_id: int) -> bool:
        q = exists(select(User).where(User.id == user_id)).select()
        return await self.scalar(q)

    async def register(self, user_id) -> User:
        user = User(id=user_id)
        self.add(user)
        await self.commit()
        return user
