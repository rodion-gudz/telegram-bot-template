from asyncio import sleep

from aiogram import types, Bot, flags
from pyrogram import Client

from app import dp
from app.common import FMT
from app.keyboards import get_author_keyboard


@dp.message(commands={"start"}, is_admin=True)
async def cmd_admin_start(message: types.Message, client: Client):
    await message.reply("Привет, администратор!")


@dp.message(commands={"start"})
async def cmd_start(message: types.Message, f: FMT, bot: Bot):
    user_id = message.from_user.id
    await sleep(2)
    if not await f.db.is_registered(user_id):
        await f.db.register(user_id)
    await message.reply("Hi, there!", reply_markup=get_author_keyboard())
