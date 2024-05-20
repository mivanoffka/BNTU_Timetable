from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from rebot.core import core
from rebot.data.types.enums import DistributionMode
from rebot.ui.button_labels import get_button_label, ButtonLabelKeys
from rebot.ui.messages import get_message_text, MessageKeys
from rebot.ui.page import Page
from rebot.ui.pages.message import show_message
from rebot.ui.states import States


async def on_back_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


async def on_morning_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    core.data.users.set_distribution_mode(callback_query.from_user.id, DistributionMode.MORNING)
    await show_message(dialog_manager, message_text=get_message_text(MessageKeys.DISTRIBUTION_SET_MORNING),
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.HOME)


async def on_evening_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    core.data.users.set_distribution_mode(callback_query.from_user.id, DistributionMode.EVENING)
    await show_message(dialog_manager, message_text=get_message_text(MessageKeys.DISTRIBUTION_SET_EVENING),
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.HOME)


async def on_silent_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    core.data.users.set_distribution_mode(callback_query.from_user.id, DistributionMode.SILENT)
    await show_message(dialog_manager, message_text=get_message_text(MessageKeys.DISTRIBUTION_SET_SILENT),
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.HOME)

distribution_page = Page(
    Const(get_button_label(ButtonLabelKeys.DISTRIBUTION)),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.MORNING)), id="morning_button", on_click=on_morning_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.EVENING)), id="evening_button", on_click=on_evening_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.SILENT)), id="silent_button", on_click=on_silent_button_click),
    ),

    Button(Const(get_button_label(ButtonLabelKeys.BACK)), on_click=on_back_button_click, id="back_button"),
    state=States.DISTRIBUTION
)
