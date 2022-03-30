from typing import Any

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ChatEvent
from aiogram_dialog.exceptions import UnknownIntent
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.kbd import Button

from app.states.support import SupportDialog


async def get_data(dialog_manager: DialogManager, **kwargs):
    age = dialog_manager.current_context().dialog_data.get("age", None)
    return {
        "name": dialog_manager.current_context().dialog_data.get("name", ""),
        "age": age,
        "can_smoke": age in ("18-25", "25-40", "40+"),
    }


async def name_handler(
    m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager
):
    manager.current_context().dialog_data["name"] = m.text
    await m.answer(f"Nice to meet you, {m.text}")
    await dialog.next()


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Thank you. To start again click /start")
    await manager.done()


async def on_age_changed(
    c: ChatEvent, select: Any, manager: DialogManager, item_id: str
):
    manager.current_context().dialog_data["age"] = item_id
    await manager.dialog().next()


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SupportDialog.greeting, mode=StartMode.RESET_STACK)


async def error_handler(update, exception, dialog_manager: DialogManager):
    if isinstance(exception, UnknownIntent):
        await dialog_manager.start(SupportDialog.greeting, mode=StartMode.RESET_STACK)
    else:
        return UNHANDLED
