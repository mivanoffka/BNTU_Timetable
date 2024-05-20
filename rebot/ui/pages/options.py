from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from rebot.ui.button_labels import get_button_label, ButtonLabelKeys
from rebot.ui.messages import messages_rus, MessageKeys
from rebot.ui.page import Page
from rebot.ui.pages.message import show_message
from rebot.ui.states import States


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_start_flag"] = False
    await dialog_manager.switch_to(state=States.GROUP_INPUT, show_mode=ShowMode.EDIT)


async def on_help_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, messages_rus[MessageKeys.HELP], get_button_label(ButtonLabelKeys.BACK), state=States.OPTIONS)


async def on_website_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, messages_rus[MessageKeys.WEBSITE], get_button_label(ButtonLabelKeys.BACK), state=States.OPTIONS)


async def on_donations_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, messages_rus[MessageKeys.DONATIONS], get_button_label(ButtonLabelKeys.BACK), state=States.OPTIONS)


async def on_report_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.REPORT_INPUT, show_mode=ShowMode.EDIT)


async def on_home_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


options_page = Page(
    Const(messages_rus[MessageKeys.DEFAULT]),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.WEBSITE)), id="bntu_button", on_click=on_website_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.GROUP_INPUT)), id="group_button", on_click=on_group_button_click)
    ),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.DONATIONS)), id="donations_button", on_click=on_donations_button_click)),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.BACK)), id="back_button", on_click=on_home_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.REPORT)), id="report_button", on_click=on_report_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.HELP)), id="help_checkbox", on_click=on_help_button_click)
    ),
    state=States.OPTIONS,
)
