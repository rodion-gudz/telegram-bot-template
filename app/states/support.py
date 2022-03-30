from aiogram.dispatcher.fsm.state import StatesGroup, State


class SupportDialog(StatesGroup):
    greeting = State()
    select_type = State()
    finish = State()
