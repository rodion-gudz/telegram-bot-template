from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update
from aiogram_dialog import DialogRegistry
from fluentogram import TranslatorRunner, TranslatorHub


class LangMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        fluent: TranslatorHub = data["fluent"]
        translator_runner: TranslatorRunner = fluent.get_translator_by_locale(
            locale=data["event_from_user"].language_code
        )
        data["i18n"] = translator_runner
        return await handler(event, data)


def register_middleware(dp: Dispatcher, registry: DialogRegistry):
    lang_middleware = LangMiddleware()
    registry.update_handler.middleware(lang_middleware)
    dp.message.middleware(lang_middleware)
