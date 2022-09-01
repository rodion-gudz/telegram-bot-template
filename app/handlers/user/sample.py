from aiogram import Router
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.states import SampleDialog

router = Router()


@router.message(commands="dialog")
async def support_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SampleDialog.greeting)
