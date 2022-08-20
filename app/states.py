from aiogram.fsm.state import State, StatesGroup


class SampleDialog(StatesGroup):
    greeting = State()
