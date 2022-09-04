from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update
from cachetools import TTLCache

from app.config import Config


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, config: Config):
        self.cache = TTLCache(maxsize=10_000, ttl=config.settings.throttling_rate)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in self.cache:
            return
        self.cache[event.chat.id] = None
        return await handler(event, data)


def register_middleware(dp: Dispatcher, config: Config):
    throttling_middleware = ThrottlingMiddleware(config=config)
    dp.message.middleware(throttling_middleware)
