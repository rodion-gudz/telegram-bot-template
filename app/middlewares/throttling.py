from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from cachetools import TTLCache

from app import config, dp

cache = TTLCache(maxsize=10_000, ttl=config.settings.throttling_rate)


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


throttling_middleware = ThrottlingMiddleware()
dp.message.middleware(throttling_middleware)
