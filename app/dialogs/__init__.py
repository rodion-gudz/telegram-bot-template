from aiogram_dialog import DialogRegistry


def register_dialogs(registry: DialogRegistry):
    from . import sample_dialog

    registry.register(sample_dialog.ui)
