from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from rebot.core import core
from rebot.ui import text
from rebot.ui.pages.special.notification import show_message
from rebot.ui.states import States


async def show_timetable_message_for_weekday(weekday_number: int, callback_query: CallbackQuery,
                                             button: Button, dialog_manager: DialogManager, state_to_return: State=States.WEEKDAYS):
    message_text: str = await core.data.timetable.get_timetable_message_text(
        user_id=callback_query.from_user.id, weekday_number=weekday_number)
    message_text = str(weekday_number) + ": " + message_text

    await show_message(dialog_manager,
                       message_text, text.get(text.ButtonKeys.BACK), state_to_return)
