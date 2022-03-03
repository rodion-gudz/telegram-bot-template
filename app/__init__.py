from aiogram import Dispatcher, Bot
from aiogram_dialog import DialogRegistry
from pyrogram import Client
from sqlalchemy.orm import sessionmaker

from app.config_parser import Config

owner_id: id
admin_ids: list
dp: Dispatcher
registry: DialogRegistry
sessionmanager: sessionmaker
client: Client
bot: Bot
config: Config
