from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from rebot.core import core
from rebot.ui.button_labels import ButtonLabelKeys, get_button_label
from rebot.ui.pages.message import show_message
from rebot.ui.states import States


async def show_timetable_message_for_weekday(weekday_number: int, callback_query: CallbackQuery,
                                             button: Button, dialog_manager: DialogManager, state_to_return: State=States.WEEKDAYS):
    message_text: str = await core.data.timetable.get_timetable_message_text(
        user_id=callback_query.from_user.id, weekday_number=weekday_number)
    message_text = str(weekday_number) + ": " + message_text

    await show_message(dialog_manager,
                       message_text, get_button_label(ButtonLabelKeys.BACK), state_to_return)
