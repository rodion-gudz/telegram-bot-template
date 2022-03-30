import os

import toml


class Config(dict):
    def __getattr__(self, name):
        return self[name]


def parse_config() -> Config:
    config_file = "config.toml"

    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file} no such file")

    with open(config_file, "r") as f:
        data = toml.load(f)

    config = Config()
    for section in data:
        setattr(config, section, Config(data[section]))
    return config
