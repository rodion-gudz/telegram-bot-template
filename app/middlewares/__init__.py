import os
from importlib import import_module

for module in os.listdir(os.path.dirname(__file__)):
    if module == "__init__.py" or module[-3:] != ".py":
        continue
    import_module(f".{module[:-3]}", __package__)
