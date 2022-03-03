from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from app import owner_id


class IsOwner(BaseFilter):
    is_owner: bool

    async def __call__(self, message: types.Message) -> bool:
        return self.is_owner is (message.from_user.id == owner_id)
