import argparse
import asyncio
import logging

import coloredlogs
from aiogram import Bot, types, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry
from pyrogram import Client

import app
from app import db
from app.config_parser import parse_config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process app configuration.")
    parser.add_argument("--config", "-c", type=str, help="configuration file", default="config.toml")
    parser.add_argument("--test", "-t", help="test bot token", action="store_true")
    parser.add_argument("--pyrogram", "-p", help="activate pyrogram session", action="store_true")
    parser.add_argument("--redis", "-r", type=str, help="use redis storage", default=False)

    return parser.parse_args()


async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="just start")
    ]
    await bot.set_my_commands(commands, scope=types.BotCommandScopeDefault())


# noinspection PyUnresolvedReferences
def register_all():
    from app import filters, middlewares, handlers, dialogs


async def main():
    coloredlogs.install()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt='%Y-%m-%d|%H:%M:%S',
    )

    arguments = parse_arguments()
    app.config = parse_config(arguments.config)
    app.owner_id = app.config.owner_id
    app.admin_ids = app.config.admin_ids

    app.sessionmanager = await db.init(app.config.engine)

    session = AiohttpSession(api=TelegramAPIServer.from_base(app.config.api))
    token = app.config.test_token if arguments.test else app.config.token
    app.bot = Bot(token, parse_mode="HTML", session=session)
    storage = MemoryStorage()
    app.dp = Dispatcher(storage=storage)
    app.registry = DialogRegistry(app.dp)
    app.client = Client("app",
                        no_updates=True,
                        parse_mode="HTML",
                        api_id=2040,
                        api_hash="b18441a1ff607e10a989891a5462e627",
                        bot_token=token,
                        workdir='../')
    register_all()

    await set_bot_commands(app.bot)

    try:
        if arguments.pyrogram:
            await app.client.start()
        await app.dp.start_polling(app.bot)
    finally:
        await storage.close()
        await app.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
