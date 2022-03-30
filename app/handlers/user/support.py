from aiogram.types import Message
from aiogram_dialog import DialogManager

from app import dp
from app.states.support import SupportDialog


@dp.message(commands="support")
async def support_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SupportDialog.greeting)
