import argparse

from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry
from pyrogram import Client
from sqlalchemy.orm import sessionmaker

from .config import Config, parse_config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process app configuration.")
    parser.add_argument(
        "--test", "-t", help="test bot token", action="store_true")
    return parser.parse_args()


owner_id: int
dp: Dispatcher
registry: DialogRegistry
sessionmanager: sessionmaker
client: Client
bot: Bot
config: Config = parse_config()
arguments = parse_arguments()
