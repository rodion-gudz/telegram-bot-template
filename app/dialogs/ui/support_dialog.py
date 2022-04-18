from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, Select
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.handlers.support import question_handler, type_selected
from app.states.support import SupportDialog

ui = Dialog(
    Window(
        Const("<b>📎 Напиши сообщение, которое нужно передать администратору</b>"),
        MessageInput(question_handler),
        state=SupportDialog.greeting,
    ),
    Window(
        Format("<b>📤 Выбери тип обращения</b>"),
        Column(
            Select(
                Format("{item}"),
                items=["🐛 Техническая проблема",
                       "📩 Предложение", "❓ Общий вопрос"],
                item_id_getter=lambda x: x,
                id="type",
                on_click=type_selected,
            ),
        ),
        state=SupportDialog.select_type,
    ),
    Window(
        Const("<b>✅ Спасибо за обращение</b>"),
        Const("Ваш вопрос передан администратору"),
        state=SupportDialog.finish,
    ),
)
