from aiogram import F
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.filters import CommandStart
from aiogram.filters import ExceptionTypeFilter, Command
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery, Update, ErrorEvent
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.ui.page import Page
from rebot.ui.states import States
from rebot.ui import text
from rebot.ui.pages.special.input import show_input_message
from rebot.ui.common import goto_group_input


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["return_from_group_input_to"] = States.START
    await goto_group_input(callback_query, button, dialog_manager)


async def msg_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    await core.messenger.try_delete(message)
    dialog_manager.show_mode = ShowMode.EDIT

start_page = Page(
        Format(
            text.get(text.MessageKeys.WELCOME)
        ),
        Row(
            Button(Const(text.get(text.ButtonKeys.GROUP_INPUT)), id="group_button", on_click=on_group_button_click),
        ),
        MessageInput(
            func=msg_handler
        ),
        state=States.START
    )


@core.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await core.messenger.try_delete(message)

    await core.data.users.register(message.from_user.id)

    print(message.from_user.id)

    await core.messenger.send_emoji_delay(message.from_user.id)
    await dialog_manager.start(States.START, show_mode=ShowMode.DELETE_AND_SEND)


@core.error(ExceptionTypeFilter(UnknownIntent))
async def handle(*args, **kwargs):
    for arg in args:
        print(arg)

    for arg in kwargs:
        print(str(arg) + " : " + str(kwargs[arg]))

    error_event: ErrorEvent = args[0]
    print(type(args[0]))
    message: Message = error_event.update.callback_query.message

    await core.messenger.try_delete(message)

    event_context: EventContext = kwargs["event_context"]
    dialog_manager: DialogManager = kwargs["dialog_manager"]
    await resume(dialog_manager, event_context.user_id)


@core.callback_query(F.data.startswith('restart'))
@core.message(Command("home"))
async def on_home_command(message: Message, dialog_manager: DialogManager):
    await core.messenger.try_delete(message)
    await core.messenger.send_emoji_delay(message.from_user.id)
    await resume(dialog_manager, message.from_user.id)


@core.track(key="resume")
async def resume(dialog_manager: DialogManager, user_id: int):
    state: State = States.HOME if await core.data.users.get_group(user_id) is not None else States.START
    await dialog_manager.start(state, show_mode=ShowMode.SEND)


