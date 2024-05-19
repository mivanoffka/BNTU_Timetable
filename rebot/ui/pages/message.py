from typing import Dict, Any

from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode, Dialog
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Back, PrevPage, Url, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.ui.messages import messages_rus, MessageKeys
from rebot.ui.states import States


async def show_message(dialog_manager: DialogManager, message_text: str | tuple[str], button_text: str | tuple[str],
                       state: State | tuple[State]):
    dialog_manager.dialog_data["message:text"] = message_text
    dialog_manager.dialog_data["message:button_text"] = button_text
    dialog_manager.dialog_data["message:state_to_go"] = state
    await dialog_manager.switch_to(States.MESSAGE, show_mode=ShowMode.EDIT)


async def on_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    state: State = dialog_manager.dialog_data["message:state_to_go"]
    await dialog_manager.switch_to(state, show_mode=ShowMode.EDIT)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "text": dialog_manager.dialog_data["message:text"],
        "button_text": dialog_manager.dialog_data["message:button_text"]
    }

message_page = Window(
    Format("{text}"),
    Row(Button(Format("{button_text}"), on_click=on_button_click, id="button")),
    state=States.MESSAGE,
    getter=getter,
    disable_web_page_preview=True
)
