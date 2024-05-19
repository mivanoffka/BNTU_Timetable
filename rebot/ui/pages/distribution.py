from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Cancel, Button, Back
from aiogram_dialog.widgets.text import Format, Const

from rebot.ui.states import States
from rebot.ui.button_labels import get_button_label, ButtonLabelKeys
from rebot.ui.messages import get_message_text, MessageKeys
from rebot.ui.pages.message import show_message


async def on_back_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.HOME, show_mode=ShowMode.EDIT)


async def on_morning_button_click(calback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, message_text=get_message_text(MessageKeys.DISTRIBUTION_SET_MORNING),
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.HOME)


async def on_evening_button_click(calback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, message_text=get_message_text(MessageKeys.DISTRIBUTION_SET_EVENING),
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.HOME)


async def on_silent_button_click(calback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await show_message(dialog_manager, message_text=get_message_text(MessageKeys.DISTRIBUTION_SET_SILENT),
                       button_text=get_button_label(ButtonLabelKeys.HOME), state=States.HOME)

distribution_page = Window(
    Const("<i>📬 Хотите, чтобы расписание само отправлялось вам каждый день? Подпишитесь на рассылку! </i>"
          "\n\n<b>❓ Когда бы вы хотели получать сообщения с расписанием?</b>"),
    Row(
        Button(Const(get_button_label(ButtonLabelKeys.MORNING)), id="morning_button", on_click=on_morning_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.EVENING)), id="evening_button", on_click=on_evening_button_click),
        Button(Const(get_button_label(ButtonLabelKeys.SILENT)), id="silent_button", on_click=on_silent_button_click),
    ),

    Button(Const("Назад ↩️"), on_click=on_back_button_click, id="back_button"),
    state=States.DISTRIBUTION
)