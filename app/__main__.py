import asyncio
import logging

import aioredis
import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.dispatcher.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiogram_dialog import DialogRegistry
from aiohttp import web
from pyrogram import Client

import app
from app import config
from app.db import init_orm, close_orm
from app.ui.commands import remove_bot_commands, set_bot_commands
from app import db


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    # noinspection PyUnresolvedReferences
    from app import dialogs, filters, handlers, inline, middlewares

    await set_bot_commands(app.bot)
    if config.settings.use_webhook:
        webhook_url = (
            config.webhook.url + config.webhook.path
            if config.webhook.url
            else f"http://localhost:{config.webhook.port}{config.webhook.path}"
        )
        await bot.set_webhook(
            webhook_url,
            drop_pending_updates=config.settings.drop_pending_updates,
        )
    else:
        await bot.delete_webhook(
            drop_pending_updates=config.settings.drop_pending_updates,
        )

    tortoise_config = config.database.get_tortoise_config()
    await init_orm(tortoise_config)

    bot_info = await app.bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "Enabled",
        False: "Disabled",
    }

    logging.debug(f"Groups Mode - {states[bot_info.can_join_groups]}")
    logging.debug(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logging.debug(f"Inline Mode - {states[bot_info.supports_inline_queries]}")

    logging.error("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=config.settings.drop_pending_updates)
    await dispatcher.fsm.storage.close()
    await app.bot.session.close()
    await close_orm()


async def main():
    logging_level = logging.INFO
    coloredlogs.install(level=logging_level)
    logging.warning("Starting bot...")

    app.owner_id = app.config.settings.owner_id

    tortoise_config = config.database.get_tortoise_config()
    try:
        await db.create_models(tortoise_config)
    except FileExistsError:
        await db.migrate_models(tortoise_config)

    session = AiohttpSession(api=TelegramAPIServer.from_base(config.api.bot_api_url))
    token = config.bot.token
    bot_settings = {"session": session, "parse_mode": "HTML"}
    app.bot = Bot(token, **bot_settings)

    if config.storage.use_persistent_storage:
        storage = RedisStorage(
            redis=aioredis.from_url(config.storage.redis_url),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()

    app.dp = Dispatcher(storage=storage)
    app.dp.startup.register(on_startup)
    app.dp.shutdown.register(on_shutdown)
    app.registry = DialogRegistry(app.dp)
    app.client = Client(
        name="app",
        no_updates=True,
        in_memory=True,
        api_id=config.api.id,
        api_hash=config.api.hash,
        bot_token=token,
        workdir="../",
    )

    if config.settings.use_pyrogram_client:
        await app.client.start()
    if config.settings.use_webhook:
        web_app = web.Application()
        SimpleRequestHandler(dispatcher=app.dp, bot=app.bot).register(
            web_app, path=config.webhook.path
        )
        setup_application(web_app, app.dp, bot=app.bot)
        # noinspection PyProtectedMember
        await web._run_app(
            app=web_app,
            port=config.webhook.port,
            access_log=None,
            print=lambda msg: None,
        )
    else:
        await app.dp.start_polling(app.bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
