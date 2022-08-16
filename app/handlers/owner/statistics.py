from aiogram.types import Message

from app import dp
from app.db.functions import User


@dp.message(commands="stats", is_owner=True)
async def stats_handler(message: Message):
    count = await User.get_count()
    await message.answer(
        f"📊 <b>Количество пользователей бота -</b> <code>{count}</code>"
    )
