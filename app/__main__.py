import argparse
import asyncio
import logging

from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from app import db
from app.config_parser import parse_config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process bot configuration.")
    parser.add_argument("--config", "-c", type=str, help="configuration file", default="config.toml")
    parser.add_argument("--test", "-t", help="test bot token", action="store_true")
    parser.add_argument("--redis", "-r", type=str, help="use redis storage", default=False)

    return parser.parse_args()


async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="just start")
    ]
    await bot.set_my_commands(commands, scope=types.BotCommandScopeDefault())


def register_all(dp: Router, config, sessionmanager):
    from app import filters
    from app import handlers
    from app import middlewares

    filters.register(dp, config)
    handlers.register(dp)
    middlewares.register(dp, config, sessionmanager)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt='%Y-%m-%d|%H:%M:%S',
    )

    arguments = parse_arguments()
    config = parse_config(arguments.config)

    sessionmanager = await db.init(config.engine)

    session = AiohttpSession(api=TelegramAPIServer.from_base(config.api))
    token = config.test_token if arguments.test else config.token
    bot = Bot(token, parse_mode="HTML", session=session)
    storage = MemoryStorage() if not arguments.redis else RedisStorage.from_url(arguments.redis)
    dp = Dispatcher(storage=storage)

    register_all(dp, config, sessionmanager)

    await set_bot_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
