from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from rebot.core import core
from rebot.data.types.enums import GroupSettingResult
from rebot.ui import text
from rebot.ui.pages.special.dialog import show_dialog_message
from rebot.ui.pages.special.notification import show_message
from rebot.ui.states import States


async def show_timetable_message_for_weekday(weekday_number: int, callback_query: CallbackQuery,
                                             button: Button, dialog_manager: DialogManager, state_to_return: State=States.WEEKDAYS):
    message_text: str = await core.data.timetable.get_timetable_message_text(
        user_id=callback_query.from_user.id, weekday_number=weekday_number)
    message_text = str(weekday_number) + ": " + message_text

    await show_message(dialog_manager,
                       message_text, text.get(text.ButtonKeys.BACK), state_to_return)


async def handle_group_input(message: Message, widget, dialog_manager: DialogManager, data):
    group_number: int | None = _get_group_number(message.text)
    if group_number is None:
        await show_dialog_message(dialog_manager,
                                  message_text=text.get(text.MessageKeys.GROUP_INPUT_PARSE_ERROR),
                                  button_texts=(text.get(text.ButtonKeys.TRY_AGAIN),
                                                text.get(text.ButtonKeys.CONTINUE)),
                                  handlers=(States.GROUP_INPUT, States.HOME))
        return

    user_id: int = message.from_user.id
    result: GroupSettingResult = await core.data.users.set_group(user_id=user_id, group_number=group_number)

    if result == GroupSettingResult.SUCCESS:
        await show_message(dialog_manager, message_text=text.get(text.MessageKeys.GROUP_INPUT_SUCCESS),
                           button_text=text.get(text.ButtonKeys.CONTINUE), state=States.HOME)

    elif result == GroupSettingResult.NO_SCHEDULE:
        await show_message(dialog_manager, message_text=text.get(text.MessageKeys.GROUP_INPUT_SUCCESS),
                           button_text=text.get(text.ButtonKeys.CONTINUE), state=States.HOME)

    elif result == GroupSettingResult.NO_GROUP:
        await show_dialog_message(dialog_manager, message_text=text.get(text.MessageKeys.GROUP_INPUT_SUCCESS),
                                  button_texts=(text.get(text.ButtonKeys.TRY_AGAIN),
                                                text.get(text.ButtonKeys.CONTINUE)),
                                  handlers=(States.GROUP_INPUT, States.HOME))


def _get_group_number(message_text: str) -> int | None:
    words: list[str] = message_text.split()
    if len(words) == 0:
        return None

    if not words[0].isdigit() or len(words[0]) != 8:
        return None

    return int(words[0])
