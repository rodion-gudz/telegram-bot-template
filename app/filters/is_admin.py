from aiogram import types
from aiogram.dispatcher.filters import BaseFilter


def generate(config):
    class IsAdmin(BaseFilter):
        is_admin: bool

        async def __call__(self, message: types.Message) -> bool:
            return self.is_admin is (message.from_user.id in config.admins)

    return IsAdmin


def register(dp, config):
    IsAdmin = generate(config)
    dp.message.bind_filter(IsAdmin)
    dp.callback_query.bind_filter(IsAdmin)
