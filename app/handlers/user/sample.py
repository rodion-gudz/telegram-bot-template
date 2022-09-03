from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.dialogs.sample_dialog import SampleDialog

router = Router()


@router.message(Command(commands=["dialog"]))
async def support_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SampleDialog.greeting)
