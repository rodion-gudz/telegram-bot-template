from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update
from cachetools import TTLCache

from app.config import Config

cache: TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in cache:
            return
        cache[event.chat.id] = None
        return await handler(event, data)


def register_middleware(dp: Dispatcher, config: Config):
    global cache

    cache = TTLCache(maxsize=10_000, ttl=config.settings.throttling_rate)

    throttling_middleware = ThrottlingMiddleware()
    dp.message.middleware(throttling_middleware)
