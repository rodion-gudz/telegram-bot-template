from aiogram import Bot, Router
from aiogram.types import Message

from app.config import Config
from app.db.functions import User

router = Router()


@router.message(commands="start")
async def cmd_start(message: Message, bot: Bot, config: Config):
    user_id = message.from_user.id
    bot_information = await bot.get_me()
    if not await User.is_registered(user_id):
        await User.register(user_id)
    await message.answer(
        f"Приветствую тебя в <b>{bot_information.full_name}</b>! \n"
        f"<b>ℹ️ Для получения информации о командах и их использовании напиши</b> /help"
    )
