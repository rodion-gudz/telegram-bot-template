from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from cachetools import TTLCache

from app import dp
from app.common import FMT

cache = TTLCache(maxsize=10_000, ttl=0.5)


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in cache:
            return
        else:
            cache[event.chat.id] = None
        return await handler(event, data)


class FMiddleware(BaseMiddleware):
    def __init__(self, config, sessionmanager, bot, client) -> None:
        self.config = config
        self.sessionmanager = sessionmanager
        self.bot = bot
        self.client = client

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        async with self.sessionmanager() as session:
            data["session"] = session
            data["f"] = FMT(db=session, config=self.config)
            data["bot"] = self.bot
            data["client"] = self.client
            await handler(event, data)


def register(config, sessionmanager, bot, client):
    md = FMiddleware(config, sessionmanager, bot, client)
    dp.message.middleware(md)
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(md)
