"""There is some needed objects and types"""
from dataclasses import dataclass

from app.config_parser import Config
from app.db.functions import DB


@dataclass
class FMT:
    db: DB
    config: Config
