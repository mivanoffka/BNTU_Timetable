from pathlib import Path

import bot.commands.days
import config
from config import BASE_DIR

from bot import data, timetable

from aiogram import types
from bot.commands import buttoned
from bot.data import dispatcher
from aiogram.dispatcher import filters

from bot.states import GroupSettingState, ReportingState
from aiogram.dispatcher import FSMContext
from bot.ui.home.keyboards import home_keyboard
from bot.ui.weekdays.keyboards import weekdays_keyboard
from bot.ui.advertisement import advertise
import time


unauthorized_text = "Чтобы посмотреть расписание, необходимо указать группу... Cделать это можно в опциях!"


@dispatcher.callback_query_handler(text="show_today")
async def process_today_command(call: types.CallbackQuery):

    txt = unauthorized_text
    if data.is_authorized(call.from_user.id):
        txt = await bot.commands.days.process_day(call.from_user.id, 0)

    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    except:
        pass
    await call.answer()
    await advertise(call.from_user.id)




@dispatcher.callback_query_handler(text="show_tomorrow")
async def process_tomorrow_command(call: types.CallbackQuery):
    txt = unauthorized_text
    if data.is_authorized(call.from_user.id):
        txt = await bot.commands.days.process_day(call.from_user.id, 1)

    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="goto_weekdays")
async def process_weekdays_command(call: types.CallbackQuery):
    if data.is_authorized(call.from_user.id):
        try:
            await call.message.edit_reply_markup(reply_markup=weekdays_keyboard)
        except:
            pass
    else:
        try:
            await call.message.edit_text(unauthorized_text, parse_mode="Markdown", reply_markup=home_keyboard)
        except:
            pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_week")
async def process_week_command(call: types.CallbackQuery):
    txt = await bot.commands.general.get_week(call.from_user.id)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)



