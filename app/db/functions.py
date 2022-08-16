from tortoise.exceptions import DoesNotExist

from app.db import models


class User(models.User):
    @classmethod
    async def is_registered(cls, telegram_id: int) -> [models.User, bool]:
        try:
            user = await cls.get(telegram_id=telegram_id)
        except DoesNotExist:
            return False
        return user

    @classmethod
    async def register(cls, telegram_id) -> [models.User, bool]:
        user = User(telegram_id=telegram_id)
        await user.save()

    @classmethod
    async def get_count(cls) -> int:
        return await cls.all().count()
