from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.filters import CommandStart
from aiogram.filters import ExceptionTypeFilter, Command
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.ui.page import Page
from rebot.ui.states import States
from rebot.ui import text


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_start_flag"] = True
    await dialog_manager.switch_to(state=States.GROUP_INPUT, show_mode=ShowMode.EDIT)

start_page = Page(
        Format(
            text.get(text.MessageKeys.WELCOME)
        ),
        Row(
            Button(Const(text.get(text.ButtonKeys.GROUP_INPUT)), id="group_button", on_click=on_group_button_click),
        ),
        state=States.START
    )


@core.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await message.delete()

    await core.data.users.register(message.from_user.id)

    await core.messenger.send_emoji_delay(message.from_user.id)
    await dialog_manager.start(States.START, show_mode=ShowMode.DELETE_AND_SEND)


@core.error(ExceptionTypeFilter(UnknownIntent))
async def handle(*args, **kwargs):
    event_context: EventContext = kwargs["event_context"]
    dialog_manager: DialogManager = kwargs["dialog_manager"]
    await restart(dialog_manager, event_context.user_id)


@core.message(Command("home"))
async def on_home_command(message: Message, dialog_manager: DialogManager):
    await restart(dialog_manager, message.from_user.id)


async def restart(dialog_manager: DialogManager, user_id: int):
    await core.messenger.send_emoji_delay(user_id)
    state: State = States.HOME if await core.data.users.get_group(user_id) is not None else States.START
    await dialog_manager.start(state, show_mode=ShowMode.DELETE_AND_SEND)
