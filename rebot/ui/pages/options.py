from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from rebot.core import core
from rebot.ui import text
from rebot.ui.page import Page
from rebot.ui.common import handle_group_input
from rebot.ui.pages.special.input import show_input_message
from rebot.ui.pages.special.notification import show_message
from rebot.ui.states import States


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_input_message(dialog_manager, text.get(text.MessageKeys.GROUPS_INFO), handle_group_input)


async def on_help_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, text.get(text.MessageKeys.HELP), text.get(text.ButtonKeys.BACK), state=States.OPTIONS)


async def on_website_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, text.get(text.MessageKeys.WEBSITE), text.get(text.ButtonKeys.BACK), state=States.OPTIONS)


async def on_donations_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, text.get(text.MessageKeys.DONATIONS), text.get(text.ButtonKeys.BACK), state=States.OPTIONS)


async def on_report_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.REPORT_INPUT, show_mode=ShowMode.EDIT)


async def on_home_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


async def on_admin_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if await core.data.users.is_admin(callback_query.from_user.id):
        await dialog_manager.switch_to(state=States.ADMIN, show_mode=ShowMode.EDIT)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    admin: bool = await core.data.users.is_admin(dialog_manager.event.from_user.id)
    return {
        "admin": admin,
        "not_admin": not admin,
    }

options_page = Page(
    Const(text.get(text.text.MessageKeys.DEFAULT)),
    Row(
        Button(Const(text.get(text.ButtonKeys.WEBSITE)), id="bntu_button", on_click=on_website_button_click),
        Button(Const(text.get(text.ButtonKeys.GROUP_INPUT)), id="group_button", on_click=on_group_button_click),
        when="not_admin"
    ),
    Row(
        Button(Const(text.get(text.ButtonKeys.WEBSITE_SHORTENED)), id="bntu_button", on_click=on_website_button_click),
        Button(Const(text.get(text.ButtonKeys.ADMIN_PANEL)), id="admin_panel", on_click=on_admin_button_click),
        Button(Const(text.get(text.ButtonKeys.GROUP_INPUT_SHORTENED)), id="group_button", on_click=on_group_button_click),
        when="admin"
    ),
    Row(
        Button(Const(text.get(text.ButtonKeys.DONATIONS)), id="donations_button", on_click=on_donations_button_click)),
    Row(
        Button(Const(text.get(text.ButtonKeys.BACK)), id="back_button", on_click=on_home_button_click),
        Button(Const(text.get(text.ButtonKeys.REPORT)), id="report_button", on_click=on_report_button_click),
        Button(Const(text.get(text.ButtonKeys.HELP)), id="help_checkbox", on_click=on_help_button_click)
    ),
    state=States.OPTIONS,
    getter=getter
)
