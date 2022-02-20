from aiogram import Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
