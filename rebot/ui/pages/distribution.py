from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from rebot.core import core
from rebot.data.types.enums import DistributionMode
from rebot.ui import text
from rebot.ui.page import Page
from rebot.ui.pages.special.notification import show_message
from rebot.ui.states import States


async def on_back_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


async def on_morning_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await core.data.users.set_distribution_mode(callback_query.from_user.id, DistributionMode.MORNING)
    await show_message(
        dialog_manager,
        message_text=text.text.get(text.text.MessageKeys.DISTRIBUTION_SET_MORNING),
        button_text=text.text.get(text.text.ButtonKeys.HOME),
        state=States.HOME
    )


async def on_evening_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await core.data.users.set_distribution_mode(callback_query.from_user.id, DistributionMode.EVENING)
    await show_message(
        dialog_manager,
        message_text=text.get(text.MessageKeys.DISTRIBUTION_SET_EVENING),
        button_text=text.get(text.ButtonKeys.HOME),
        state=States.HOME
    )


async def on_silent_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await core.data.users.set_distribution_mode(callback_query.from_user.id, DistributionMode.SILENT)
    await show_message(
        dialog_manager,
        message_text=text.get(text.MessageKeys.DISTRIBUTION_SET_SILENT),
        button_text=text.get(text.ButtonKeys.HOME),
        state=States.HOME
    )


distribution_page = Page(
    Const(text.text.get(text.MessageKeys.DISTRIBUTION)),

    Row(
        Button(
            Const(text.get(text.ButtonKeys.MORNING)),
            id="morning_button",
            on_click=on_morning_button_click),

        Button(
            Const(text.get(text.ButtonKeys.EVENING)),
            id="evening_button",
            on_click=on_evening_button_click),

        Button(
            Const(text.get(text.ButtonKeys.SILENT)),
            id="silent_button",
            on_click=on_silent_button_click),
    ),

    Button(
        Const(text.get(text.ButtonKeys.BACK)),
        on_click=on_back_button_click,
        id="back_button"),

    state=States.DISTRIBUTION
)
