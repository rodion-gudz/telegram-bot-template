import asyncio
import logging

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import DialogRegistry
from aiohttp import web
from pyrogram import Client

from app import db
from app.arguments import parse_arguments
from app.config import Config, parse_config
from app.db import close_orm, init_orm
from app.dialogs import register_dialogs
from app.handlers import get_handlers_router
from app.inline.handlers import get_inline_router
from app.middlewares import register_middlewares
from app.commands import remove_bot_commands, setup_bot_commands


async def on_startup(
    dispatcher: Dispatcher, bot: Bot, config: Config, registry: DialogRegistry
):

    register_middlewares(dp=dispatcher, config=config)

    dispatcher.include_router(get_handlers_router())
    dispatcher.include_router(get_inline_router())

    register_dialogs(registry)

    await setup_bot_commands(bot, config)

    if config.settings.use_webhook:
        webhook_url = (
            config.webhook.url + config.webhook.path
            if config.webhook.url
            else f"http://localhost:{config.webhook.port}{config.webhook.path}"
        )
        await bot.set_webhook(
            webhook_url,
            drop_pending_updates=config.settings.drop_pending_updates,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    else:
        await bot.delete_webhook(
            drop_pending_updates=config.settings.drop_pending_updates,
        )

    tortoise_config = config.database.get_tortoise_config()
    await init_orm(tortoise_config)

    bot_info = await bot.get_me()

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


async def on_shutdown(dispatcher: Dispatcher, bot: Bot, config: Config):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot, config)
    await bot.delete_webhook(drop_pending_updates=config.settings.drop_pending_updates)
    await dispatcher.fsm.storage.close()
    await bot.session.close()
    await close_orm()


async def main():
    coloredlogs.install(level=logging.INFO)
    logging.warning("Starting bot...")

    arguments = parse_arguments()
    config = parse_config(arguments.config)

    tortoise_config = config.database.get_tortoise_config()
    try:
        await db.create_models(tortoise_config)
    except FileExistsError:
        await db.migrate_models(tortoise_config)

    session = AiohttpSession(api=TelegramAPIServer.from_base(config.api.bot_api_url, is_local=config.api.is_local))
    token = config.bot.token
    bot_settings = {"session": session, "parse_mode": "HTML"}

    bot = Bot(token, **bot_settings)

    if config.storage.use_persistent_storage:
        storage = RedisStorage(
            redis=RedisStorage.from_url(config.storage.redis_url),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    registry = DialogRegistry(dp)

    context_kwargs = {"config": config, "registry": registry}

    if config.settings.use_pyrogram_client:
        pyrogram_client = Client(
            name="bot",
            no_updates=True,
            in_memory=True,
            api_id=config.api.id,
            api_hash=config.api.hash,
            bot_token=token,
            workdir="../",
        )
        await pyrogram_client.start()
        context_kwargs["client"] = pyrogram_client

    if config.settings.use_webhook:
        logging.getLogger("aiohttp.access").setLevel(logging.CRITICAL)

        web_app = web.Application()
        SimpleRequestHandler(dispatcher=dp, bot=bot, **context_kwargs).register(
            web_app, path=config.webhook.path
        )

        setup_application(web_app, dp, bot=bot, **context_kwargs)

        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, port=config.webhook.port)
        await site.start()

        await asyncio.Event().wait()
    else:
        await dp.start_polling(bot, **context_kwargs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
