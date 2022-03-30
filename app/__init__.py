from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry
from pyrogram import Client
from sqlalchemy.orm import sessionmaker

from .config import Config, parse_config
from .const import *

owner_id: id
dp: Dispatcher
registry: DialogRegistry
sessionmanager: sessionmaker
client: Client
bot: Bot
config: Config = parse_config()
