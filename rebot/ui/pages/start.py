from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Row, Start, Button
from aiogram_dialog.widgets.text import Format, Const
from rebot.core import core
from rebot.ui.states import States


async def on_group_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["from_start_flag"] = True
    await dialog_manager.switch_to(state=States.GROUP_INPUT, show_mode=ShowMode.EDIT)

start_page = Window(
        Format(
            "👋<b> Ещё раз здравствуйте!</b> \n\n<i>Перед тем, как продолжить,"
            " вам необходимо указать группу, студентом которой вы являетесь.</i> \n\n"
        ),
        Row(
            Button(Const("Указать группу ✏️"), id="group_button", on_click=on_group_button_click),
        ),
        state=States.START
    )


@core.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await message.delete()
    await core.messenger.send_emoji_delay(message.from_user.id)
    await dialog_manager.start(States.START, show_mode=ShowMode.DELETE_AND_SEND)
