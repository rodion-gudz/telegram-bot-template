from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.common import FMT


class FMiddleware(BaseMiddleware):
    def __init__(self, config, sessionmanager) -> None:
        self.config = config
        self.sessionmanager = sessionmanager

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with self.sessionmanager() as session:
            data["session"] = session
            data["f"] = FMT(db=session, config=self.config)
            await handler(event, data)


def register(dp, config, sessionmanager):
    md = FMiddleware(config, sessionmanager)
    dp.message.middleware(md)
    dp.callback_query.middleware(md)
