from typing import Dict, Any

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.ui.pages.message import show_message
from rebot.ui.pages.alternative_message import show_alternative_message
from rebot.ui.states import States
from rebot.ui.messages import messages_rus, MessageKeys
from rebot.ui.button_labels import get_button_label, ButtonLabelKeys


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    if dialog_manager.dialog_data["from_start_flag"]:
        return {
            "show_start_button": True,
            "show_options_button": False
        }
    else:
        return {
            "show_start_button": False,
            "show_options_button": True
        }


async def handle_group_input(message: Message, widget, dialog_manager: DialogManager, data):
    await message.delete()

    await show_alternative_message(dialog_manager, message_text=messages_rus[MessageKeys.GROUP_INPUT_SUCCESS],
                                   button_texts=(get_button_label(ButtonLabelKeys.TRY_AGAIN),
                                                 get_button_label(ButtonLabelKeys.CONTINUE)),
                                   states=(States.GROUP_INPUT, States.HOME))

    await show_message(dialog_manager, message_text=messages_rus[MessageKeys.GROUP_INPUT_SUCCESS],
                       button_text="Продолжить ➡️", state=States.HOME)


async def on_cancel_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.START, show_mode=ShowMode.EDIT)


group_input_page = Window(
    Format(
        messages_rus[MessageKeys.GROUPS_INFO]
    ),
    Row(SwitchTo(Const(get_button_label(ButtonLabelKeys.CANCEL)),
                 id="start_button",
                 state=States.START, when="show_start_button")),

    Row(SwitchTo(Const(get_button_label(ButtonLabelKeys.CANCEL)),
                 id="options_button",
                 state=States.OPTIONS, when="show_options_button")),

    TextInput(id="group_input", on_success=handle_group_input),
    state=States.GROUP_INPUT,
    getter=getter
)
