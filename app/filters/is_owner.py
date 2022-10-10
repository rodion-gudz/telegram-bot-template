from aiogram import types
from aiogram.filters import Filter

from app.config import Config


class IsOwner(Filter):

    def __init__(self, is_owner: bool) -> None:
        self.is_owner = is_owner

    async def __call__(self, message: types.Message, config: Config) -> bool:
        return self.is_owner is (message.from_user.id == config.settings.owner_id)
