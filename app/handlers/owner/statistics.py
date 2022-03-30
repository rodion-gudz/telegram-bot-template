from aiogram.types import Message

from app import dp
from app.common import FMT


@dp.message(commands="stats", is_owner=True)
async def stats_handler(message: Message, f: FMT):
    count = await f.db.get_users_count()
    await message.answer(
        f"📊 <b>Количество пользователей бота -</b> <code>{count}</code>"
    )
