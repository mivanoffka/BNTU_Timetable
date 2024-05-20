from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.data.types.enums import TrackerKeys
from rebot.ui.states import States
from rebot.ui.messages import messages_rus, MessageKeys
from rebot.ui.button_labels import get_button_label, ButtonLabelKeys
from rebot.ui.pages.message import show_message
from rebot.ui.messages import get_message_text
from rebot.ui.pages.alternative_message import show_alternative_message

from rebot.ui.page import Page


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "message": messages_rus[MessageKeys.REPORT_AVAILABLE]
    }


async def handle_report_input(message: Message, widget, dialog_manager: DialogManager, data):
    await message.delete()

    await core.accept_report(user_id=message.from_user.id, report_text=message.text)
    await show_message(dialog_manager, message_text=messages_rus[MessageKeys.REPORT_INPUT_SUCCESS],
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.OPTIONS)


async def on_cancel_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.OPTIONS, show_mode=ShowMode.EDIT)


report_input_page = Page(
        Format("{message}"),
        Row(SwitchTo(Const(get_button_label(ButtonLabelKeys.CANCEL)), id="options_button", state=States.OPTIONS)),
        TextInput(id="report_input", on_success=handle_report_input),
        state=States.REPORT_INPUT,
        getter=getter
    )

