from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app import dp
from app.common import FMT


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
    dp.callback_query.middleware(md)
