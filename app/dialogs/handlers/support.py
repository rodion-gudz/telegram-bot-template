from typing import Any

from aiogram.types import Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto

from app import bot, owner_id


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
        f"<b>Сообщение</b> - <code>{manager.current_context().dialog_data['question']}</code>",
    )

    await manager.dialog().next()
