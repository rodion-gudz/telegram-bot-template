import argparse
import asyncio
import logging

from aiogram import Bot, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from pyrogram import Client

from app import db, dp, storage
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


def register_all(config, sessionmanager, bot, client):
    from app import filters
    from app import middlewares

    filters.register(config)
    # noinspection PyUnresolvedReferences
    import app.handlers
    middlewares.register(config, sessionmanager, bot, client)


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
    client = Client("bot",
                    no_updates=True,
                    api_id=2040,
                    api_hash="b18441a1ff607e10a989891a5462e627",
                    bot_token=token)
    register_all(config, sessionmanager, bot, client)

    await set_bot_commands(bot)

    try:
        await client.start()
        await dp.start_polling(bot)
    finally:
        await storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
