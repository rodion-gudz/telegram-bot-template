from app import dp
from .is_admin import IsAdmin
from .is_owner import IsOwner

filters = (IsAdmin, IsOwner)
for aiogram_filter in filters:
    dp.message.bind_filter(aiogram_filter)
    dp.callback_query.bind_filter(aiogram_filter)
    dp.inline_query.bind_filter(aiogram_filter)
