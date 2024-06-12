from typing import Dict, Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format

from rebot.ui.page import Page
from rebot.ui.states import States


async def show_message(dialog_manager: DialogManager, message_text: str, button_text: str,
                       state: State):
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

message_page = Page(
    Format("{text}"),
    Row(Button(Format("{button_text}"), on_click=on_button_click, id="button")),
    state=States.MESSAGE,
    getter=getter,
    disable_web_page_preview=True
)
