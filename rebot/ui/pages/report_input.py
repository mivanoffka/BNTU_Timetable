from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.ui.states import States
from rebot.ui.messages import messages_rus, MessageKeys
from rebot.ui.pages.message import show_message


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "message": messages_rus[MessageKeys.REPORT_AVAILABLE]
    }


async def handle_report_input(message: Message, widget, dialog_manager: DialogManager, data):
    await message.delete()
    await show_message(dialog_manager, message_text=messages_rus[MessageKeys.REPORT_INPUT_SUCCESS],
                       button_text="На главную 🏠", state=States.OPTIONS)


async def on_cancel_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.OPTIONS, show_mode=ShowMode.EDIT)


report_input_page = Window(
        Format("{message}"),
        Row(SwitchTo(Const("Отмена ✖️"), id="options_button", state=States.OPTIONS)),
        TextInput(id="report_input", on_success=handle_report_input),
        state=States.REPORT_INPUT,
        getter=getter
    )

