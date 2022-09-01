from aiogram import types
from aiogram.filters import BaseFilter

from app.config import Config


class IsOwner(BaseFilter):
    is_owner: bool

    async def __call__(self, message: types.Message, config: Config) -> bool:
        return self.is_owner is (message.from_user.id == config.settings.owner_id)
