import os
from importlib import import_module

from app import registry

for module in os.listdir(os.path.dirname(__file__)):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    registry.register(getattr(import_module(
        f".{module[:-3]}", __package__), "ui"))
