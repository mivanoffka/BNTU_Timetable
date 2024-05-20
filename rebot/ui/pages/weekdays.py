from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from rebot.ui.button_labels import get_button_label, ButtonLabelKeys
from rebot.ui.common import show_timetable_message_for_weekday
from rebot.ui.messages import get_message_text, MessageKeys
from rebot.ui.page import Page
from rebot.ui.states import States


async def on_back_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["weekdays_flag"] = False
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


async def on_monday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_timetable_message_for_weekday(weekday_number=0, callback_query=callback_query,
                                             button=button, dialog_manager=dialog_manager)


async def on_tuesday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_timetable_message_for_weekday(weekday_number=1, callback_query=callback_query,
                                             button=button, dialog_manager=dialog_manager)


async def on_wednesday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_timetable_message_for_weekday(weekday_number=2, callback_query=callback_query,
                                             button=button, dialog_manager=dialog_manager)


async def on_thursday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_timetable_message_for_weekday(weekday_number=3, callback_query=callback_query,
                                             button=button, dialog_manager=dialog_manager)


async def on_friday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_timetable_message_for_weekday(weekday_number=4, callback_query=callback_query,
                                             button=button, dialog_manager=dialog_manager)


async def on_saturday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_timetable_message_for_weekday(weekday_number=5, callback_query=callback_query,
                                             button=button, dialog_manager=dialog_manager)


weekdays_page = Page(
    Const(get_message_text(MessageKeys.DEFAULT)),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.MONDAY)), id="monday_button", on_click=on_monday_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.TUESDAY)), id="tuesday_button", on_click=on_tuesday_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.WEDNESDAY)), id="wednesday_button", on_click=on_wednesday_button_click),
    ),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.THURSDAY)), id="thursday_button", on_click=on_thursday_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.FRIDAY)), id="friday_button", on_click=on_friday_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.SATURDAY)), id="saturday_button", on_click=on_saturday_button_click),
    ),
    Button(Const("Назад ↩️"), on_click=on_back_button_click, id="back_button"),

    state=States.WEEKDAYS
)
