from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.ui.pages.message import show_message
from rebot.ui.pages.alternative_message import show_alternative_message
from rebot.ui.states import States
from rebot.ui.messages import get_message_text, MessageKeys
from rebot.ui.button_labels import get_button_label, ButtonLabelKeys

from rebot.ui.page import Page
from rebot.data.types.enums import GroupSettingResult


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

    group_number: int | None = get_group_number(message.text)
    if group_number is None:
        await show_alternative_message(dialog_manager,
                                       message_text=get_message_text(MessageKeys.GROUP_INPUT_PARSE_ERROR),
                                       button_texts=(get_button_label(ButtonLabelKeys.TRY_AGAIN),
                                                     get_button_label(ButtonLabelKeys.CONTINUE)),
                                       states=(States.GROUP_INPUT, States.HOME))
        return

    user_id: int = message.from_user.id
    result: GroupSettingResult = await core.data.users.set_group(user_id=user_id, group_number=group_number)

    if result == GroupSettingResult.SUCCESS:
        await show_message(dialog_manager, message_text=get_message_text(MessageKeys.GROUP_INPUT_SUCCESS),
                           button_text=get_button_label(ButtonLabelKeys.CONTINUE), state=States.HOME)

    elif result == GroupSettingResult.NO_SCHEDULE:
        await show_message(dialog_manager, message_text=get_message_text(MessageKeys.GROUP_INPUT_SUCCESS),
                           button_text=get_button_label(ButtonLabelKeys.CONTINUE), state=States.HOME)

    elif result == GroupSettingResult.NO_GROUP:
        await show_alternative_message(dialog_manager, message_text=get_message_text(MessageKeys.GROUP_INPUT_SUCCESS),
                                       button_texts=(get_button_label(ButtonLabelKeys.TRY_AGAIN),
                                                     get_button_label(ButtonLabelKeys.CONTINUE)),
                                       states=(States.GROUP_INPUT, States.HOME))


def get_group_number(message_text: str) -> int | None:
    words: list[str] = message_text.split()
    if len(words) == 0:
        return None

    if not words[0].isdigit() or len(words[0]) != 8:
        return None

    return int(words[0])


async def on_cancel_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.START, show_mode=ShowMode.EDIT)


group_input_page = Page(
    Format(
        get_message_text(MessageKeys.GROUPS_INFO)
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
