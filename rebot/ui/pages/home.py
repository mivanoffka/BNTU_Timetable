from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Const

from rebot.core import core
from rebot.ui.common import show_timetable_message_for_weekday
from rebot.ui import text
from rebot.ui.page import Page
from rebot.ui.states import States


async def on_weekdays_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["weekdays_flag"] = True
    await dialog_manager.switch_to(state=States.WEEKDAYS, show_mode=ShowMode.EDIT)


@core.track(key="distribution")
async def on_distribution_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.DISTRIBUTION, show_mode=ShowMode.EDIT)


async def on_options_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.OPTIONS, show_mode=ShowMode.EDIT)


@core.track(key="today")
async def on_today_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    weekday_number: int = datetime.today().weekday()
    await show_timetable_message_for_weekday(weekday_number=weekday_number,
                                             dialog_manager=dialog_manager,
                                             callback_query=callback_query,
                                             button=button, state_to_return=States.HOME)


@core.track(key="tomorrow")
async def on_tomorrow_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    weekday_number: int = (datetime.today().weekday() + 1) % 7
    await show_timetable_message_for_weekday(weekday_number=weekday_number,
                                             dialog_manager=dialog_manager,
                                             callback_query=callback_query,
                                             button=button, state_to_return=States.HOME)


home_page = Page(
    Const(text.get(text.MessageKeys.DEFAULT)),
    Row(
        Button(Const(text.get(text.ButtonKeys.TODAY)),
               id="today_button",
               on_click=on_today_button_click),

        Button(Const(text.get(text.ButtonKeys.TOMORROW)),
               id="tomorrow_button",
               on_click=on_tomorrow_button_click)
    ),
    Row(
        Button(Const(text.get(text.ButtonKeys.WEEKDAYS)),
               on_click=on_weekdays_button_click,
               id="weekdays_button")),
    Row(
        SwitchTo(Const(text.get(text.ButtonKeys.DISTRIBUTION)),
                 state=States.DISTRIBUTION,
                 id="distribution_button"),

        SwitchTo(Const(text.get(text.ButtonKeys.OPTIONS)),
                 state=States.OPTIONS,
                 id="options_button")),
    state=States.HOME
)
