import os
from dataclasses import dataclass
from typing import List

import toml


@dataclass
class Config:
    token: str
    test_token: str
    api: str
    owner_id: int
    admin_ids: List[int]
    engine: str


def parse_config(config_file: str) -> Config:
    if not os.path.isfile(config_file) and not config_file.endswith(".toml"):
        config_file += ".toml"

    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    with open(config_file, "r") as f:
        data = toml.load(f)

    # TODO: automatic config parsing based on class fields
    return Config(
        token=data["bot"]["token"],
        test_token=data["bot"]["test_token"],
        api=data["bot"].get("api", "https://api.telegram.org/"),
        owner_id=data["bot"]["owner"],
        admin_ids=data["bot"]["admins"],
        engine=data["database"]["engine"]
    )
