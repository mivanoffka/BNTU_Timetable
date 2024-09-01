from pathlib import Path

from aiogram.types import ReplyKeyboardRemove

import bot.ui.options.keyboards
import config
from config import BASE_DIR

from bot import data

from aiogram import types
from bot.data import dispatcher
from aiogram.dispatcher import filters

from bot.states import GroupSettingState, ReportingState
from aiogram.dispatcher import FSMContext

from bot.ui.keyboards import cancel_keyboard, open_menu_keyboard, delete_keyboard, reply_keyboard
from bot.ui.home.keyboards import home_keyboard
from bot.ui.options.keyboards import options_keyboard
from bot.ui.advertisement import advertise
from bot.ui.start.keyboards import continue_reply_button
from bot.ui.dailymail.keyboards import dailymail_keyboard
import bot.display

import random

default_mes = "<b>Выберите желаемое действие...</b>\n\n<i>🎲 Или просто тыкайте на кнопочки!</i>"


async def send_ui(id, mes=default_mes):
    #await send_delay(id)
    #await data.bot.send_message(id, mes, reply_markup=home_keyboard)
    #await bot.display.update_display(id, mes, home_keyboard)
    await bot.display.send_display(id, mes, home_keyboard)



@dispatcher.message_handler(commands=['menu', 'home'])
@dispatcher.message_handler(filters.Text(equals=bot.ui.keyboards.open_menu_button.text))
async def process_ui_command(message: types.Message):
    await bot.display.try_delete(message)
    await send_ui(message.from_user.id)


@dispatcher.callback_query_handler(text="goto_options")
async def process_options_command(call: types.CallbackQuery):


    try:
        await call.message.edit_reply_markup(reply_markup=options_keyboard)
    except:
        pass

    data.datacollector.update_stats("options", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="goto_home")
async def process_home_command(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=home_keyboard)
    await call.answer()
    await advertise(call.from_user.id)





@dispatcher.callback_query_handler(text="goto_home_clr")
async def process_home_command(call: types.CallbackQuery):
    #await call.message.edit_reply_markup(reply_markup=home_keyboard)
    await bot.display.update_display(call.from_user.id, default_mes, home_keyboard, no_menu=True)
    await call.answer()


@dispatcher.callback_query_handler(text="delete_message")
async def process_delete_command(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()


@dispatcher.callback_query_handler(text="input_report")
async def process_devinfo_command(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in data.recently_sended_report:
        await ReportingState.awaiting.set()
        txt = "<i>🧐 Хотите указать на ошибку, предложить идею по улучшению бота или просто написать" \
              " гадостей?</i>\n\n<b>Тогда отправьте своё послание как обычное сообщение!</b>"

        await bot.display.update_display(call.from_user.id, txt, cancel_keyboard, no_menu=True)
    else:
        m = "⏳ <i>Вы совсем недавно отправляли нам сообщение... Подождите пару минуточек, прежде чем делать это снова!</i>"
        await bot.display.update_display(call.from_user.id, m, options_keyboard, no_menu=True)


@dispatcher.callback_query_handler(text="input_group")
async def process_devinfo_command(call: types.CallbackQuery, state: FSMContext):
        await GroupSettingState.awaiting.set()

        msg = "<b>❓ Какие группы обслуживаются?</b>"
        msg += "\n  •  ФИТР, ФММП и ЭФ - группы всех курсов"
        msg += "\n  •  Остальные факультеты - только 1 и 2 курсы"
        msg += "\n\n☎️ <b>Просто введите номер группы и отправьте как сообщение.</b>"

        #await call.message.edit_text(msg, parse_mode="Markdown", reply_markup=cancel_keyboard)
        await bot.display.update_display(call.from_user.id, msg, cancel_keyboard, no_menu=True)


@dispatcher.callback_query_handler(state=GroupSettingState.awaiting, text="input_cancel")
@dispatcher.callback_query_handler(state=ReportingState.awaiting, text="input_cancel")
async def process_cancel_command(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()


    await bot.display.update_display(call.from_user.id, default_mes, home_keyboard, no_menu=True)


@dispatcher.message_handler(state=ReportingState.awaiting)
async def process_send_report_command(message: types.message, state: FSMContext):
    await bot.display.try_delete(message)
    if "/menu" in message.text:
        await state.finish()
        await send_ui(message.from_user.id)
        return

    report = message.text
    report_mes = ""
    id = str(message.from_user.id)

    group = data.users_db.get_info(id).group

    report_mes += "\n\n – со всей ответственностью заявляет пользователь "
    if str(message.from_user.username) != "None":
        report_mes += "<code>{}</code> (<code>{}</code>)".format(message.from_user.username, message.from_user.id)
    else:
        report_mes += "<code>{}</code>".format(message.from_user.id)
    if group:
        report_mes += " из группы <code>{}</code>".format(group)
    report_mes = "«" + report + "»" + "<b>" + report_mes + "</b>"

    msg = "📨 <b>Ваше сообщение успешно отправлено!</b>"

    if len(report) > 1024:
        msg = "<b>Ваше сообщение слишком длинное...</b>\n<i>Может, сможете выразиться лаконичнее?</i>👉🏻👈🏻"
        await bot.display.update_display(message.from_user.id, msg, options_keyboard, no_menu=True)
    else:
        filename = "datasource/reports.txt"
        with open(Path(BASE_DIR / filename), 'a', encoding='UTF-8') as f:
            f.write(report_mes)

        data.recently_sended_report.append(message.from_user.id)

        await data.bot.send_message(config.ADMIN_ID, text=report_mes)
        await bot.display.update_display(message.from_user.id, msg, options_keyboard, no_menu=True)
        await bot.display.renew_display(config.ADMIN_ID,
                                        text="<b>📮 Пришёл отзыв.</b> \n\nПролистайте вверх, чтобы его посмотреть.",
                                        keyboard=bot.ui.home.keyboards.home_keyboard)

    data.datacollector.update_stats("report", id)
    await state.finish()
    await advertise(message.from_user.id)

