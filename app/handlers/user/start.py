from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.db.functions import User

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, i18n: TranslatorRunner):
    user_id = message.from_user.id
    bot_information = await bot.get_me()

    if not await User.is_registered(user_id):
        await User.register(user_id)
    await message.answer(i18n.welcome(bot_full_name=bot_information.full_name))
