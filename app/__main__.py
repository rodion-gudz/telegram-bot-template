import argparse
import asyncio
import logging

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiogram_dialog import DialogRegistry
from aiohttp import web
from pyrogram import Client

import app
from app import (
    API_HASH,
    API_ID,
    API_URL,
    DROP_PENDING_UPDATES,
    USE_PYROGRAM_CLIENT,
    config,
)
from app.ui.setup import remove_bot_commands, set_bot_commands
from app.utils import db


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process app configuration.")
    parser.add_argument(
        "--test", "-t", help="test bot token", action="store_true")
    return parser.parse_args()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    # noinspection PyUnresolvedReferences
    from app import dialogs, filters, handlers, inline, middlewares

    await set_bot_commands(app.bot)
    if config.webhook.use_webhook:
        await bot.set_webhook(
            f"{config.webhook.BASE_URL}{config.webhook.MAIN_BOT_PATH}",
            drop_pending_updates=DROP_PENDING_UPDATES,
        )
    else:
        await bot.delete_webhook(
            drop_pending_updates=DROP_PENDING_UPDATES,
        )


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.fsm.storage.close()
    await app.bot.session.close()


async def main():
    coloredlogs.install()
    logging.warning("Starting bot...")

    arguments = parse_arguments()
    app.owner_id = app.config.bot.OWNER_ID

    app.sessionmanager = await db.init(config.database.engine)

    session = AiohttpSession(api=TelegramAPIServer.from_base(API_URL))
    token = config.bot.TEST_TOKEN if arguments.test else config.bot.TOKEN
    bot_settings = {"session": session, "parse_mode": "HTML"}
    app.bot = Bot(token, **bot_settings)
    bot_info = await app.bot.get_me()
    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")
    storage = MemoryStorage()
    app.dp = Dispatcher(storage=storage)
    app.dp.startup.register(on_startup)
    app.dp.shutdown.register(on_shutdown)
    app.registry = DialogRegistry(app.dp)
    app.client = Client(
        "app",
        no_updates=True,
        parse_mode="HTML",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=token,
        workdir="../",
    )

    if USE_PYROGRAM_CLIENT:
        await app.client.start()
    if config.webhook.use_webhook:
        web_app = web.Application()
        SimpleRequestHandler(dispatcher=app.dp, bot=app.bot).register(
            web_app, path=config.webhook.MAIN_BOT_PATH
        )
        setup_application(web_app, app.dp, bot=app.bot)
        await web._run_app(
            web_app,
            host=config.webhook.WEB_SERVER_HOST,
            port=config.webhook.WEB_SERVER_PORT,
            access_log=None,
            print=lambda x: logging.error("Bot started!"),
        )
    else:
        await app.dp.start_polling(app.bot)
        logging.error("Bot started!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
