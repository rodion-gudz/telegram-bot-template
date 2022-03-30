from aiogram import Bot
from aiogram.types import Message

from app import dp, owner_id
from app.keyboards.inline.author_keyboard import get_author_keyboard
from app.ui.commands import owner_commands, users_commands


@dp.message(commands="help")
async def help_handler(message: Message):
    text = "ℹ️ <b>Список команд:</b> \n\n"
    commands = (
        owner_commands.items()
        if message.from_user.id == owner_id
        else users_commands.items()
    )
    for command, description in commands:
        text += f"/{command} - <b>{description}</b> \n"
    await message.answer(text)


@dp.message(commands="about")
async def about_handler(message: Message, bot: Bot):
    bot_information = await bot.get_me()
    text = (
        "<b>ℹ️ Информация о боте:</b> \n\n"
        f"<b>Название - </b> {bot_information.full_name} \n"
        f"<b>Username - </b> @{bot_information.username} \n"
        f"<b>ID - </b> <code>{bot_information.id}</code> \n"
    )
    await message.answer(text, reply_markup=get_author_keyboard())
