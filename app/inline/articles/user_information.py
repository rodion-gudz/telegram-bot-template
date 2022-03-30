from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, User


def get_user_information_article(user: User):
    return InlineQueryResultArticle(
        id="user_information",
        title="ℹ️ Информация о пользователе",
        description=f"Username и ID пользователя {user.full_name}",
        input_message_content=InputTextMessageContent(
            message_text=f"<b>🙍‍ Пользователь:</b> @{user.username} \n"
            f"<b>📌 ID:</b> <code>{user.id}</code>"
        ),
    )
