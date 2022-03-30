from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.dialogs.handlers.support import name_handler, on_age_changed, get_data, on_finish
from app.states.support import SupportDialog

ui = Dialog(
    Window(
        Const("Greetings! Please, introduce yourself:"),
        MessageInput(name_handler),
        state=SupportDialog.greeting,
    ),
    Window(
        Format("{name}! How old are you?"),
        Select(
            Format("{item}"),
            items=["0-12", "12-18", "18-25", "25-40", "40+"],
            item_id_getter=lambda x: x,
            id="w_age",
            on_click=on_age_changed,
        ),
        state=SupportDialog.age,
        getter=get_data,
        preview_data={"name": "Tishka17"},
    ),
    Window(
        Multi(
            Format("{name}! Thank you for your answers."),
            Const("Hope you are not smoking", when="can_smoke"),
            sep="\n\n",
        ),
        Row(
            Back(),
            SwitchTo(Const("Restart"), id="restart", state=SupportDialog.greeting),
            Button(Const("Finish"), on_click=on_finish, id="finish"),
        ),
        getter=get_data,
        state=SupportDialog.finish,
    ),
)
