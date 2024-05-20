import asyncio
from typing import Dict, Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format

from rebot.ui.page import Page
from rebot.ui.states import States


async def show_alternative_message(dialog_manager: DialogManager, message_text: str, button_texts: tuple[str, str],
                                   states: tuple[State, State]):
    dialog_manager.dialog_data["message:text"] = message_text

    dialog_manager.dialog_data["message:first:button_text"] = button_texts[0]
    dialog_manager.dialog_data["message:first:state_to_go"] = states[0]

    dialog_manager.dialog_data["message:second:button_text"] = button_texts[1]
    dialog_manager.dialog_data["message:second:state_to_go"] = states[1]

    await dialog_manager.switch_to(States.ALTERNATIVE_MESSAGE, show_mode=ShowMode.EDIT)


async def on_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    number: str = "first" if button.widget_id == "button_one" else "second"
    state: State | None = dialog_manager.dialog_data["message:{}:state_to_go".format(number)]
    await dialog_manager.switch_to(state, show_mode=ShowMode.EDIT)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "button_one_text": dialog_manager.dialog_data["message:first:button_text"],
        "button_two_text": dialog_manager.dialog_data["message:second:button_text"],

        "text": dialog_manager.dialog_data["message:text"],
    }


alternative_message_page = Page(
    Format("{text}"),
    Row(Button(Format("{button_one_text}"), on_click=on_button_click, id="button_one"),
        Button(Format("{button_two_text}"), on_click=on_button_click, id="button_two")),
    state=States.ALTERNATIVE_MESSAGE,
    getter=getter,
    disable_web_page_preview=True
)
