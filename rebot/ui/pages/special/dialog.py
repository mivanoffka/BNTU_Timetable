import asyncio
import types
from datetime import datetime, timedelta
from typing import Dict, Any, Callable

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format
from numpy import number

from rebot.ui.page import Page
from rebot.ui.states import States


async def show_dialog_message(dialog_manager: DialogManager, message_text: str, button_texts: tuple[str, str], handlers: tuple[types.FunctionType | State, types.FunctionType | State]):
    dialog_manager.dialog_data["message:text"] = message_text
    dialog_manager.dialog_data["message:first:button_text"] = button_texts[0]
    dialog_manager.dialog_data["message:second:button_text"] = button_texts[1]

    if isinstance(handlers[0], types.FunctionType):
        dialog_manager.dialog_data["handler_one"] = handlers[0]
    elif isinstance(handlers[0], State):
        async def handler(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
            await dialog_manager.switch_to(handlers[0], show_mode=ShowMode.EDIT)
        dialog_manager.dialog_data["handler_one"] = handler
    else:
        raise TypeError

    if isinstance(handlers[1], types.FunctionType):
        dialog_manager.dialog_data["handler_two"] = handlers[1]
    elif isinstance(handlers[1], State):
        async def handler(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
            await dialog_manager.switch_to(handlers[1], show_mode=ShowMode.EDIT)
        dialog_manager.dialog_data["handler_two"] = handler
    else:
        raise TypeError

    await dialog_manager.switch_to(States.DIALOG_MESSAGE, show_mode=ShowMode.EDIT)


async def on_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    handler_1 = dialog_manager.dialog_data["handler_one"]
    handler_2 = dialog_manager.dialog_data["handler_two"]
    handler = handler_1 if button.widget_id == "button_one" else handler_2
    await handler(callback_query, button, dialog_manager)


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "button_one_text": dialog_manager.dialog_data["message:first:button_text"],
        "button_two_text": dialog_manager.dialog_data["message:second:button_text"],

        "text": dialog_manager.dialog_data["message:text"],
    }


dialog_message_page = Page(
    Format("{text}"),
    Row(Button(Format("{button_one_text}"), on_click=on_button_click, id="button_one"),
        Button(Format("{button_two_text}"), on_click=on_button_click, id="button_two")),
    state=States.DIALOG_MESSAGE,
    getter=getter,
    disable_web_page_preview=True
)
