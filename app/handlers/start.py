from aiogram import Bot
from aiogram.types import Message

from app import dp
from app.common import FMT


@dp.message(commands="start")
async def cmd_start(message: Message, f: FMT, bot: Bot):
    user_id = message.from_user.id
    bot_information = await bot.get_me()
    if not await f.db.is_registered(user_id):
        await f.db.register(user_id)
    await message.answer(
        f"Приветствую тебя в <b>{bot_information.full_name}</b>! \n"
        f"<b>ℹ️ Для получения информации о командах и их использовании напиши</b> /help"
    )
