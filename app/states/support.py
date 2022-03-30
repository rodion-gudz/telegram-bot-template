from aiogram.dispatcher.fsm.state import State, StatesGroup


class SupportDialog(StatesGroup):
    greeting = State()
    select_type = State()
    finish = State()
