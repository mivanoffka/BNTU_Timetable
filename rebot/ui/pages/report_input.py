from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.ui.states import States
from rebot.ui.pages.special.notification import show_message
from rebot.ui.pages.special.dialog import show_dialog_message
from rebot.ui import text

from rebot.ui.page import Page


async def handle_report_input(message: Message, widget, dialog_manager: DialogManager, data):
    await message.delete()

    async def on_yes(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
        await core.accept_report(user_id=message.from_user.id, report_text=message.text)
        await show_message(dialog_manager, message_text=text.get(text.MessageKeys.REPORT_INPUT_SUCCESS),
                           button_text=text.get(text.ButtonKeys.HOME), state=States.OPTIONS)

    async def on_no(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(States.OPTIONS, show_mode=ShowMode.EDIT)

    await show_dialog_message(
                            dialog_manager,
                            text.get(text.MessageKeys.REPORT_CONFIRMATION_DIALOG).format(message.text),
                            (text.get(text.ButtonKeys.NO), text.get(text.ButtonKeys.YES)),
                            (on_no, on_yes))


async def on_cancel_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.OPTIONS, show_mode=ShowMode.EDIT)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "message": text.get(text.MessageKeys.REPORT_AVAILABLE)
    }

report_input_page = Page(
        Format("{message}"),
        Row(SwitchTo(Const(text.get(text.ButtonKeys.CANCEL)), id="options_button", state=States.OPTIONS)),
        TextInput(id="report_input", on_success=handle_report_input),
        state=States.REPORT_INPUT,
        getter=getter
    )

