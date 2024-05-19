from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button, Checkbox, Radio
from aiogram_dialog.widgets.text import Const, Format
from rebot.ui.messages import messages_rus, MessageKeys
from rebot.ui.states import States
from rebot.ui.pages.message import show_message


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_start_flag"] = False
    await dialog_manager.switch_to(state=States.GROUP_INPUT, show_mode=ShowMode.EDIT)


async def on_help_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, messages_rus[MessageKeys.HELP], "Назад ↩️", state=States.OPTIONS)


async def on_website_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, messages_rus[MessageKeys.WEBSITE], "Назад ↩️", state=States.OPTIONS)


async def on_donations_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, messages_rus[MessageKeys.DONATIONS], "Назад ↩️", state=States.OPTIONS)


async def on_report_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.REPORT_INPUT, show_mode=ShowMode.EDIT)


async def on_home_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


options_page = Window(
    Const(messages_rus[MessageKeys.DEFAULT]),
    Row(
        Button(Const("Сайт БНТУ 🏛️"), id="bntu_button", on_click=on_website_button_click),
        Button(Const("Указать группу ✏️"), id="group_button", on_click=on_group_button_click)
    ),
    Row(
        Button(Const("Поддержать нас денюжкой 🏦💞"), id="donations_button", on_click=on_donations_button_click)),
    Row(
        Button(Const("Назад ↩️"), id="back_button", on_click=on_home_button_click),
        Button(Const("Отзыв 📬️"), id="report_button", on_click=on_report_button_click),
        Button(Const("Справка 💡"), id="help_checkbox", on_click=on_help_button_click)
    ),
    state=States.OPTIONS,
)
