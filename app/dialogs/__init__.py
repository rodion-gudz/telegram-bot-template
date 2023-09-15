from aiogram import Router


def get_dialog_router() -> Router:
    from .sample_dialog import ui

    dialog_routers = Router()

    dialog_routers.include_router(ui)

    return dialog_routers
