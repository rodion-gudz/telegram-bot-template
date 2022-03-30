import time

from aiogram.types import Message

from app import dp


@dp.message(commands="ping", is_owner=True)
async def ping_handler(message: Message):
    start = time.perf_counter_ns()
    reply_message = await message.answer("<code>⏱ Checking ping...</code>")
    end = time.perf_counter_ns()
    ping = (end - start) * 0.000001
    await reply_message.edit_text(
        f"<b>⏱ Ping -</b> <code>{round(ping, 3)}</code> <b>ms</b>"
    )
