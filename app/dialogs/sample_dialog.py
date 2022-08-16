from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from app.states import SampleDialog


async def show_alert(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer("❗️ Тестовые уведомление", show_alert=True, cache_time=0)
    await c.message.delete()
    await manager.done()


ui = Dialog(
    Window(
        Const("<b>📎 Тестовый диалог</b>"),
        Button(Const("Кнопка"), id="test_button", on_click=show_alert),
        state=SampleDialog.greeting,
    ),
)
