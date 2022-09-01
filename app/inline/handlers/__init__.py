from aiogram import Router


def get_inline_router() -> Router:
    from . import user_information

    router = Router()
    router.include_router(user_information.router)

    return router
