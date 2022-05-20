from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import owner_id


def get_author_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Автор", url=f"tg://user?id={owner_id}")
    return keyboard.as_markup()
