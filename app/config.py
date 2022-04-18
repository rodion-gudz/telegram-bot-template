# sourcery skip: avoid-builtin-shadow
import os
from dataclasses import MISSING, dataclass, fields

import toml


@dataclass
class ConfigBot:
    token: str
    test_token: str


@dataclass
class ConfigDatabase:
    database_url: str
    test_database_url: str


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


def parse_config() -> Config:
    config_file = "config.toml"
    if not os.path.isfile(config_file) and not config_file.endswith(".toml"):
        config_file += ".toml"

    if not os.path.isfile(config_file):
        raise FileNotFoundError(
            f"Config file not found: {config_file} no such file")

    with open(config_file, "r") as f:
        data = toml.load(f)

    return Config.parse(dict(data))
