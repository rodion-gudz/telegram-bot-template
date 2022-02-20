from aiogram import Router, types

from app.common import FMT

rt = Router()


async def cmd_admin_start(message: types.Message):
    await message.reply("Hi, admin!")


@rt.message(commands={"start"})
async def cmd_start(message: types.Message, f: FMT):
    user_id = message.from_user.id
    if not await f.db.is_registered(user_id):
        await f.db.register(user_id)


def register(dp):
    dp.include_router(rt)
    rt.message.register(cmd_admin_start, commands={"start"}, is_admin=True)  # FIXME
    # Usage of custom bound filters with @ is temporary impossible


