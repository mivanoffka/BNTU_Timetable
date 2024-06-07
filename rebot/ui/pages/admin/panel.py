from typing import Dict, Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from rebot.core import core
from rebot.ui import text
from rebot.ui.page import Page
from rebot.ui.pages.special.notification import show_message
from rebot.ui.pages.special.input import show_input_message
from rebot.ui.pages.special.dialog import show_dialog_message
from rebot.ui.states import States
from rebot.ui import text


async def on_back_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(States.OPTIONS, show_mode=ShowMode.EDIT)


async def on_yes(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, text.get(text.MessageKeys.BROADCAST_IN_PROCESS), text.get(text.ButtonKeys.BACK), States.ADMIN)


async def on_no(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(States.ADMIN)


async def on_broadcast_text_input(message: Message, widget, dialog_manager: DialogManager, data):
    await show_dialog_message(
        dialog_manager, text.get(text.MessageKeys.BROADCAST_CONFIRMATION).format(message.text),
        (text.get(text.ButtonKeys.NO), text.get(text.ButtonKeys.YES)),
        (on_no, on_yes)
    )


async def on_broadcast_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_input_message(dialog_manager, text.get(text.MessageKeys.BROADCAST_INPUT), on_broadcast_text_input)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    admin: bool = await core.data.users.is_admin(dialog_manager.event.from_user.id)
    return {
        "admin": admin,
    }

admin_page = Page(
    Const(text.get(text.MessageKeys.ADMIN_PANEL)),
    Row(
        Button(Const(text.get(text.ButtonKeys.BROADCAST)), id="broadcast_button", on_click=on_broadcast_button_click),
        Button(Const(text.get(text.ButtonKeys.STATS)), id="stats_button"),
        when="admin"
    ),
    Row(
        Button(Const(text.get(text.ButtonKeys.TIMETABLE_SETTINGS)), id="timetable_button", on_click=None),
        when="admin"
    ),
    Row(
        Button(Const(text.get(text.ButtonKeys.BACK)), id="back_button", on_click=on_back_button_click),
        Button(Const(text.get(text.ButtonKeys.MESSENGER)), id="messenger_button", when="admin"),

    ),
    state=States.ADMIN,
    getter=getter
)
