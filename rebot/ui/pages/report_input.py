import asyncio
from typing import Dict, Any

from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, BaseDialogManager, SubManager
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from rebot.core import core
from rebot.ui import text
from rebot.ui.keyboards import home_keyboard
from rebot.ui.page import Page
from rebot.ui.pages.special.dialog import show_dialog_message
from rebot.ui.pages.special.notification import show_message
from rebot.ui.states import States


async def handle_report_input(message: Message, widget, dialog_manager: DialogManager, data):
    await message.delete()

    async def on_yes(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
        await accept_report(message)
        await show_message(dialog_manager, message_text=text.get(text.MessageKeys.REPORT_INPUT_SUCCESS),
                           button_text=text.get(text.ButtonKeys.HOME), state=States.OPTIONS)

    async def on_no(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
        await dialog_manager.switch_to(States.OPTIONS, show_mode=ShowMode.EDIT)

    await show_dialog_message(
                            dialog_manager,
                            text.get(text.MessageKeys.REPORT_CONFIRMATION_DIALOG).format(message.text),
                            (text.get(text.ButtonKeys.NO), text.get(text.ButtonKeys.YES)),
                            (on_no, on_yes)
    )


async def on_cancel_button_click(callback_query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=States.OPTIONS, show_mode=ShowMode.EDIT)


async def accept_report(message: Message):
    message_for_admins = await get_admin_message_str(message)

    admin_ids: list = await core.data.users.get_admins()
    for admin_id in admin_ids:
        await core.messenger.send_emoji_delay(admin_id)
        await core.messenger.send_message(admin_id, text=message_for_admins, keyboard_to_attach=home_keyboard.as_markup())


async def get_admin_message_str(message: Message) -> str:
    group: int | None = await core.data.users.get_group(message.from_user.id)

    message_for_admin: str = ""
    message_for_admin += "\n\n – со всей ответственностью заявляет пользователь "

    if str(message.from_user.username) != "None":
        message_for_admin += "<code>{}</code> (<code>{}</code>)".format(message.from_user.username, message.from_user.id)
    else:
        message_for_admin += "<code>{}</code>".format(message.from_user.id)
    if group is not None:
        message_for_admin += " из группы <code>{}</code>".format(group)
    message_for_admin = "«" + message.text + "»" + "<b>" + message_for_admin + "</b>"
    message_for_admin = "<b>📮 Пришёл отзыв.</b>\n\n" + message_for_admin

    return message_for_admin


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    return {
        "message": text.get(text.MessageKeys.REPORT_AVAILABLE)
    }

report_input_page = Page(
        Format("{message}"),
        Row(SwitchTo(Const(text.get(text.ButtonKeys.CANCEL)), id="options_button", state=States.OPTIONS)),
        TextInput(id="report_input", on_success=handle_report_input),
        state=States.REPORT_INPUT,
        getter=getter
    )

