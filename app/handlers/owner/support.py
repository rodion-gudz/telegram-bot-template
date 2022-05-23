from aiogram import Bot
from aiogram.types import Message

from app import dp, owner_id


@dp.message(is_owner=True)
async def question_handler(message: Message, bot: Bot):
    reply_message = message.reply_to_message

    if not reply_message or not reply_message.entities:
        return

    user_id, message_id = reply_message.entities[-1].language.split("-")

    if user_id in (bot.id, owner_id):
        return

    await bot.send_message(
        chat_id=user_id,
        reply_to_message_id=message_id,
        text=f"👨🏻‍💻 <b>Сообщение от администратора:</b>\n\n{message.html_text}",
    )

    await message.answer(
        f"<b>✅ Ответ передан пользователю {message.from_user.full_name}</b>"
    )
