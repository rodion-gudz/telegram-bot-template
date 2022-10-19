import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner

from app.filters.is_owner import IsOwner

router = Router()


@router.message(IsOwner(is_owner=True), Command(commands=["ping"]))
async def ping_handler(message: Message, i18n: TranslatorRunner):
    start = time.perf_counter_ns()
    reply_message = await message.answer(i18n.ping.checking())
    end = time.perf_counter_ns()
    ping = (end - start) * 0.000001
    await reply_message.edit_text(i18n.ping.result(ping=round(ping, 3)))
