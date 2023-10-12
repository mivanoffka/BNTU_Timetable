from pathlib import Path

import bot.ui.options.keyboards
import config
from config import BASE_DIR

from bot import data

from aiogram import types
from bot.data import dispatcher
from aiogram.dispatcher import filters

from bot.states import GroupSettingState, ReportingState
from aiogram.dispatcher import FSMContext

from bot.ui.keyboards import cancel_keyboard, menu_keyboard, delete_keyboard
from bot.ui.home.keyboards import home_keyboard
from bot.ui.options.keyboards import options_keyboard
from bot.ui.advertisement import advertise
from bot.ui.start.keyboards import continue_reply_button

import random

default_mes = "<b>Выберите желаемое действие...</b>\n\n<i>🎲 Или просто тыкайте на кнопочки!</i>"

async def send_ui(id, mes=default_mes):
    await data.bot.send_message(id, mes, reply_markup=home_keyboard)


@dispatcher.message_handler(commands=['menu'])
@dispatcher.message_handler(filters.Text(equals=bot.ui.keyboards.open_menu_button.text))
async def process_ui_command(message: types.Message):
    await send_ui(message.from_user.id)


@dispatcher.callback_query_handler(text="goto_options")
async def process_options_command(call: types.CallbackQuery):
    bot.data.increment("settings", call.from_user.id)

    try:
        await call.message.edit_reply_markup(reply_markup=options_keyboard)
    except:
        pass
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="goto_home")
async def process_home_command(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=home_keyboard)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="delete_message")
async def process_delete_command(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()


@dispatcher.callback_query_handler(text="input_report")
async def process_devinfo_command(call: types.CallbackQuery, state: FSMContext):

    await ReportingState.awaiting.set()
    await call.message.edit_text("_🧐 Хотите указать на ошибку, предложить идею по улучшению бота или просто написать"
                                 " гадостей?_\n\n*Тогда отправьте своё послание как обычное сообщение!*",
                                 parse_mode="Markdown", reply_markup=cancel_keyboard)


@dispatcher.callback_query_handler(text="input_group")
async def process_devinfo_command(call: types.CallbackQuery, state: FSMContext):
        await GroupSettingState.awaiting.set()

        msg = "*❓ Какие группы обслуживаются?*"
        msg += "\n  •  ФИТР - группы всех 4-х курсов"
        msg += "\n  •  Остальные факультеты - только 1 и 2 курсы"
        msg += "\n\n☎️ *Просто введите номер группы и отправьте как сообщение.*"

        await call.message.edit_text(msg, parse_mode="Markdown", reply_markup=cancel_keyboard)


@dispatcher.callback_query_handler(state=GroupSettingState.awaiting, text="input_cancel")
@dispatcher.callback_query_handler(state=ReportingState.awaiting, text="input_cancel")
async def process_cancel_command(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    data.increment("cancel", call.from_user.id)

    await call.message.delete()
    await send_ui(call.from_user.id)


@dispatcher.message_handler(state=ReportingState.awaiting)
async def process_send_report_command(message: types.message, state: FSMContext):
    if message.from_user.id not in data.recently_sended_report:
        report = message.text
        report_mes = ""
        id = str(message.chat.id)

        group = data.users_db.get_info(id).group

        report_mes += "\n\nПользователь "
        if str(message.from_user.username) != "None":
            report_mes += "{} ({})".format(message.from_user.username, message.from_user.id)
        else:
            report_mes += "{}".format(message.from_user.id)
        if group:
            report_mes += " из группы {}".format(group)
        report_mes = "«" + report + "»" + "*" + report_mes + "*"

        msg = "-"
        if len(report) > 1024:
            msg = "*Ваше сообщение слишком длинное...*\n_Может, сможете выразиться лаконичнее?_👉🏻👈🏻"
        else:
            filename = "datasource/reports.txt"
            with open(Path(BASE_DIR / filename), 'a', encoding='UTF-8') as f:
                f.write(report_mes)

            data.recently_sended_report.append(message.from_user.id)

            msg = "Сообщение успешно отправлено! 📨"

            await data.bot.send_message(config.ADMIN_ID, text=report_mes, parse_mode="Markdown")

        await send_ui(message.from_user.id, "Сообщение успешно отправлено! 📨")
    else:
        m = "⏳ _Вы совсем недавно отправляли нам сообщение... Подождите пару минуточек, прежде чем делать это снова!_"
        await data.bot.send_message(message.chat.id, text=m, parse_mode="Markdown", reply_markup=options_keyboard)
    await state.finish()
    await advertise(message.from_user.id)

