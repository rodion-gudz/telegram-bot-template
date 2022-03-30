"""There is some needed objects and types"""
from dataclasses import dataclass

from app.config import Config
from app.utils.db.functions import DB


@dataclass
class FMT:
    db: DB
    config: Config
