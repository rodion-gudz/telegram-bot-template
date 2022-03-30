from aiogram.dispatcher.fsm.state import StatesGroup, State


class SupportDialog(StatesGroup):
    greeting = State()
    age = State()
    finish = State()
