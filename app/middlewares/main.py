from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app import bot, client, config, dp, sessionmanager
from app.common import FMT


class MainMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.config = config
        self.sessionmanager = sessionmanager
        self.bot = bot
        self.client = client

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmanager() as session:
            data["session"] = session
            data["f"] = FMT(db=session, config=self.config)
            data["bot"] = self.bot
            data["client"] = self.client
            await handler(event, data)


md = MainMiddleware()
dp.message.middleware(md)
dp.callback_query.middleware(md)
