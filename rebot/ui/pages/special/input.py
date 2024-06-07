from typing import Dict, Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format, Const

from rebot.ui.page import Page
from rebot.ui.states import States
from rebot.ui.text import *


async def show_input_message(dialog_manager: DialogManager, message_text: str, input_handler):
    dialog_manager.dialog_data["message:text"] = message_text
    dialog_manager.dialog_data["message:input_handler"] = input_handler
    dialog_manager.dialog_data["message:state_to_go"] = dialog_manager.current_context().state
    await dialog_manager.switch_to(States.INPUT, show_mode=ShowMode.EDIT)


async def on_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    state: State = dialog_manager.dialog_data["message:state_to_go"]
    await dialog_manager.switch_to(state, show_mode=ShowMode.EDIT)


async def handle_input(message: Message, widget, dialog_manager: DialogManager, data):
    try:
        await message.delete()
    except:
        pass

    await dialog_manager.dialog_data["message:input_handler"](message, widget, dialog_manager, data)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "text": dialog_manager.dialog_data["message:text"],
    }


message_page = Page(
    Format("{text}"),
    Row(Button(Const(text.get(text.ButtonKeys.BACK)), on_click=on_button_click, id="button")),
    TextInput(id="input", on_success=handle_input),
    state=States.INPUT,
    getter=getter,
    disable_web_page_preview=True
)
