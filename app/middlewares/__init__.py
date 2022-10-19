from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

from app.config import Config


def register_middlewares(dp: Dispatcher, config: Config, registry: DialogRegistry):
    from . import localization, throttling

    throttling.register_middleware(dp=dp, config=config)
    localization.register_middleware(dp=dp, registry=registry)
