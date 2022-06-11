from typing import Any

from aiogram.types import Message
from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Column, Select
from aiogram_dialog.widgets.text import Const, Format

from app import bot, owner_id
from app.states import SupportDialog


async def question_handler(
    m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager
):
    manager.current_context().dialog_data["question"] = m.text
    await dialog.next()


async def type_selected(
    c: ChatEvent, select: Any, manager: DialogManager, question_type: str
):
    user = c.from_user
    await bot.send_message(
        chat_id=owner_id,
        text="<b>⚠️ Новое обращение</b> \n\n"
        f"<b>Пользователь</b> - <a href='tg://user?id={user.id}'>{user.full_name}</a> \n"
        f"<b>Тип</b> - {question_type} \n"
        f"<b>Сообщение</b> - <code>{manager.current_context().dialog_data['question']}</code>"
        f"<pre><code class='language-{user.id}-{c.message.message_id}'>ㅤ</code></pre>",
    )
    await bot.send_message(
        chat_id=user.id,
        text="<b>✅ Спасибо за обращение</b> \n" "Ваш вопрос передан администратору",
    )
    await manager.done()


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
                items=["🐛 Техническая проблема", "📩 Предложение", "❓ Общий вопрос"],
                item_id_getter=lambda x: x,
                id="type",
                on_click=type_selected,
            ),
        ),
        state=SupportDialog.select_type,
    ),
)
