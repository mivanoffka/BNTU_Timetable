from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent

from rebot.core import core
from rebot.ui.states import States


@core.error(ExceptionTypeFilter(UnknownIntent))
async def handle(*args, **kwargs):
    event_context: EventContext = kwargs["event_context"]
    dialog_manager: DialogManager = kwargs["dialog_manager"]
    await renew_dialog(dialog_manager, event_context.user_id)


async def renew_dialog(dialog_manager: DialogManager, user_id: int):
    await core.messenger.send_emoji_delay(user_id)
    await dialog_manager.start(States.HOME, show_mode=ShowMode.DELETE_AND_SEND)


