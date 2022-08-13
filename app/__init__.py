import argparse

from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry
from pyrogram import Client
from sqlalchemy.orm import sessionmaker

from .config import Config, parse_config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process app configuration.")
    parser.add_argument(
        "--config", "-c", type=str, help="configuration file", default="config.toml"
    )
    return parser.parse_args()


owner_id: int
dp: Dispatcher
registry: DialogRegistry
sessionmanager: sessionmaker
client: Client
bot: Bot
arguments = parse_arguments()
config: Config = parse_config(arguments.config)
