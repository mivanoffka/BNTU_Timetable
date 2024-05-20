from aiogram.filters import CommandStart
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.ui.button_labels import ButtonLabelKeys, get_button_label
from rebot.ui.messages import get_message_text, MessageKeys
from rebot.ui.page import Page
from rebot.ui.states import States

from rebot.data.types.enums import TrackerKeys


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_start_flag"] = True
    await dialog_manager.switch_to(state=States.GROUP_INPUT, show_mode=ShowMode.EDIT)

start_page = Page(
        Format(
            get_message_text(MessageKeys.WELCOME)
        ),
        Row(
            Button(Const(get_button_label(ButtonLabelKeys.GROUP_INPUT)), id="group_button", on_click=on_group_button_click),
        ),
        state=States.START
    )


@core.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await message.delete()

    await core.data.users.register(message.from_user.id)

    await core.messenger.send_emoji_delay(message.from_user.id)
    await dialog_manager.start(States.START, show_mode=ShowMode.DELETE_AND_SEND)
