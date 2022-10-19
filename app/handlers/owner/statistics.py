from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.db.functions import User
from app.filters.is_owner import IsOwner

router = Router()


@router.message(IsOwner(is_owner=True), Command(commands=["stats"]))
async def stats_handler(message: Message, i18n: TranslatorRunner):
    count = await User.get_count()
    await message.answer(i18n.stats(count=count))
