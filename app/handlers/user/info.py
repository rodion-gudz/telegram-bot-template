from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.commands import owner_commands, users_commands
from app.config import Config
from app.keyboards.inline import get_author_keyboard

router = Router()


@router.message(Command(commands=["help"]))
async def help_handler(message: Message, config: Config, i18n: TranslatorRunner):
    text = i18n.help() + "\n\n"
    commands = (
        owner_commands.items()
        if message.from_user.id == config.settings.owner_id
        else users_commands.items()
    )
    for command, description in commands:
        text += f"/{command} - <b>{description}</b> \n"
    await message.answer(text)


@router.message(Command(commands=["about"]))
async def about_handler(
    message: Message, bot: Bot, config: Config, i18n: TranslatorRunner
):
    bot_information = await bot.get_me()
    await message.answer(
        i18n.about(
            bot_full_name=bot_information.full_name,
            bot_username=bot_information.username,
            bot_id=str(bot_information.id),
        ),
        reply_markup=get_author_keyboard(owner_id=config.settings.owner_id),
    )
