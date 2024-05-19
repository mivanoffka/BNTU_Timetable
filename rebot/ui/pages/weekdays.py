from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode, Dialog
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Back, PrevPage
from aiogram_dialog.widgets.text import Format, Const
from rebot.ui.days import Days
from rebot.ui.states import States


async def on_back_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["weekdays_flag"] = False

    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


async def on_monday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["day"] = Days.MONDAY
    await dialog_manager.switch_to(state=States.TIMETABLE, show_mode=ShowMode.EDIT)


async def on_tuesday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["day"] = Days.TUESDAY
    await dialog_manager.switch_to(state=States.TIMETABLE, show_mode=ShowMode.EDIT)


async def on_wednesday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["day"] = Days.WEDNESDAY
    await dialog_manager.switch_to(state=States.TIMETABLE, show_mode=ShowMode.EDIT)


async def on_thursday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["day"] = Days.THURSDAY
    await dialog_manager.switch_to(state=States.TIMETABLE, show_mode=ShowMode.EDIT)


async def on_friday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["day"] = Days.FRIDAY
    await dialog_manager.switch_to(state=States.TIMETABLE, show_mode=ShowMode.EDIT)


async def on_saturday_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["day"] = Days.SATURDAY
    await dialog_manager.switch_to(state=States.TIMETABLE, show_mode=ShowMode.EDIT)


weekdays_page = Window(
    Const("<b>Выберите желаемое действие...</b>\n\n<i>🎲 Или просто тыкайте на кнопочки!</i>"),
    Row(
        Button(Const("Пн. ⚫"), id="monday_button", on_click=on_monday_button_click),
        Button(Const("Вт. ⚪️"), id="tuesday_button"),
        Button(Const("Ср. ⚫"), id="wednesday_button"),
    ),
    Row(
        Button(Const("Чт. ⚪"), id="thursday_button"),
        Button(Const("Пт. ⚫"), id="friday_button"),
        Button(Const("Сб. ⚪"), id="saturday_button"),
    ),
    Button(Const("Назад ↩️"), on_click=on_back_button_click, id="back_button"),

    state=States.WEEKDAYS
)
