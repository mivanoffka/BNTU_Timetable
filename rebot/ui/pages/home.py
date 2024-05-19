from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode, StartMode
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Start, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.ui.states import States
from rebot.ui.pages.message import show_message
from rebot.ui.button_labels import get_button_label, ButtonLabelKeys


async def on_weekdays_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["weekdays_flag"] = True
    await dialog_manager.switch_to(state=States.WEEKDAYS, show_mode=ShowMode.EDIT)


async def on_distribution_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.DISTRIBUTION, show_mode=ShowMode.EDIT)


async def on_options_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.OPTIONS, show_mode=ShowMode.EDIT)


async def on_today_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager,
                       "Рано или поздно, здесь будет расписание...", "Назад ↩️", States.HOME)


async def on_tomorrow_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager,
                       "Рано или поздно, здесь будет расписание...", "Назад ↩️", States.HOME)


home_page = Window(
    Const("<b>Выберите желаемое действие...</b>\n\n<i>🎲 Или просто тыкайте на кнопочки!</i>"),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.TODAY)),
               id="today_button",
               on_click=on_today_button_click),

        Button(Const(get_button_label(ButtonLabelKeys.TOMORROW)),
               id="tomorrow_button",
               on_click=on_tomorrow_button_click)
    ),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.WEEKDAYS)),
               on_click=on_weekdays_button_click,
               id="weekdays_button")),
    Row(
        SwitchTo(Const(get_button_label(ButtonLabelKeys.DISTRIBUTION)),
                 state=States.DISTRIBUTION,
                 id="distribution_button"),

        SwitchTo(Const(get_button_label(ButtonLabelKeys.OPTIONS)),
                 state=States.OPTIONS,
                 id="options_button")),
    state=States.HOME
)
