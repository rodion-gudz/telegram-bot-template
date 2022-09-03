# sourcery skip: avoid-builtin-shadow
import os
from dataclasses import MISSING, dataclass, fields

import toml


@dataclass
class ConfigBot:
    token: str


@dataclass
class ConfigDatabase:
    models: list[str]
    protocol: str = "sqlite"
    file_name: str = "production-database.sqlite3"
    user: str = None
    password: str = None
    host: str = None
    port: str = None

    def get_db_url(self):
        if self.protocol == "sqlite":
            return f"{self.protocol}://{self.file_name}"
        return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}"

    def get_tortoise_config(self):
        return {
            "connections": {"default": self.get_db_url()},
            "apps": {
                "models": {
                    "models": self.models,
                    "default_connection": "default",
                },
            },
        }


@dataclass
class ConfigStorage:
    use_persistent_storage: bool
    redis_url: str = None


@dataclass
class ConfigWebhook:
    port: int
    path: str = "/webhook"
    url: str = None


@dataclass
class ConfigSettings:
    owner_id: int
    throttling_rate: float = 0.5
    use_webhook: bool = False
    use_pyrogram_client: bool = False
    drop_pending_updates: bool = True


@dataclass
class ConfigApi:
    id: int = 2040
    hash: str = "b18441a1ff607e10a989891a5462e627"
    bot_api_url: str = "https://api.telegram.org"

    @property
    def is_local(self):
        return self.bot_api_url != "https://api.telegram.org"


@dataclass
class Config:
    bot: ConfigBot
    database: ConfigDatabase
    storage: ConfigStorage
    webhook: ConfigWebhook
    settings: ConfigSettings
    api: ConfigApi

    @classmethod
    def parse(cls, data: dict) -> "Config":
        sections = {}

        for section in fields(cls):
            pre = {}
            current = data[section.name]

            for field in fields(section.type):
                if field.name in current:
                    pre[field.name] = current[field.name]
                elif field.default is not MISSING:
                    pre[field.name] = field.default
                else:
                    raise ValueError(
                        f"Missing field {field.name} in section {section.name}"
                    )

            sections[section.name] = section.type(**pre)

        return cls(**sections)


def parse_config(config_file: str) -> Config:
    if not os.path.isfile(config_file) and not config_file.endswith(".toml"):
        config_file += ".toml"

    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    with open(config_file, "r") as f:
        data = toml.load(f)

    return Config.parse(dict(data))
