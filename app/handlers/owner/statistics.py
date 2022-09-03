from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.functions import User
from app.filters.is_owner import IsOwner

router = Router()


@router.message(IsOwner(is_owner=True), Command(commands=["stats"]))
async def stats_handler(message: Message):
    count = await User.get_count()
    await message.answer(
        f"📊 <b>Количество пользователей бота -</b> <code>{count}</code>"
    )
