from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import owner_id


def get_author_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Author", url=f"tg://user?id={owner_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
