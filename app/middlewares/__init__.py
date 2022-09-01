from aiogram import Dispatcher

from app.config import Config


def register_middlewares(dp: Dispatcher, config: Config):
    from . import throttling

    throttling.register_middleware(dp=dp, config=config)
