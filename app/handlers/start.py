from aiogram import types

from app import dp
from app.common import FMT


@dp.message(commands="start", is_admin=True)
async def cmd_admin_start(message: types.Message):
    await message.reply("Привет, администратор!")


@dp.message(commands="start")
async def cmd_start(message: types.Message, f: FMT):
    user_id = message.from_user.id
    if not await f.db.is_registered(user_id):
        await f.db.register(user_id)
    await message.answer("Privet")
