from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_author_keyboard(owner_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Автор", url=f"tg://user?id={owner_id}")
    return keyboard.as_markup()
