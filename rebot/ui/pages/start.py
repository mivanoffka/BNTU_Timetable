from aiogram import F
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
from rebot.ui.pages.special.input import show_input_message
from rebot.ui.common import handle_group_input


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_input_message(dialog_manager, text.get(text.MessageKeys.GROUPS_INFO), handle_group_input)

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

    print(message.from_user.id)

    await core.messenger.send_emoji_delay(message.from_user.id)
    await dialog_manager.start(States.START, show_mode=ShowMode.DELETE_AND_SEND)


@core.error(ExceptionTypeFilter(UnknownIntent))
async def handle(*args, **kwargs):
    event_context: EventContext = kwargs["event_context"]
    dialog_manager: DialogManager = kwargs["dialog_manager"]
    await restart(dialog_manager, event_context.user_id)


@core.callback_query(F.data.startswith('restart'))
@core.message(Command("home"))
async def on_home_command(message: Message, dialog_manager: DialogManager):
    await restart(dialog_manager, message.from_user.id)


@core.foo
async def restart(dialog_manager: DialogManager, user_id: int):
    await core.messenger.send_emoji_delay(user_id)
    state: State = States.HOME if await core.data.users.get_group(user_id) is not None else States.START
    await dialog_manager.start(state, show_mode=ShowMode.SEND)


