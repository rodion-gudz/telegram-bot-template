from aiogram import types, Bot
from pyrogram import Client

from app import dp
from app.common import FMT


@dp.message(commands={"start"}, is_admin=True)
async def cmd_admin_start(message: types.Message, client: Client):
    message = await message.reply("Привет, администратор!")
    await client.edit_message_text(text='ura', chat_id=message.chat.id, message_id=message.message_id)


@dp.message(commands={"start"})
async def cmd_start(message: types.Message, f: FMT, bot: Bot):
    user_id = message.from_user.id
    if not await f.db.is_registered(user_id):
        await f.db.register(user_id)
    await message.reply(bot.me())
