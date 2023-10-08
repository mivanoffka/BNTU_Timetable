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
import time
from bot.ui.advertisement import advertise



@dispatcher.callback_query_handler(text="show_mon")
async def process_today_command(call: types.CallbackQuery):
    txt = bot.timetable.get_day_message(call.from_user.id, 0)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_tue")
async def process_today_command(call: types.CallbackQuery):
    txt = bot.timetable.get_day_message(call.from_user.id, 1)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_wed")
async def process_today_command(call: types.CallbackQuery):
    txt = bot.timetable.get_day_message(call.from_user.id, 2)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_thu")
async def process_today_command(call: types.CallbackQuery):
    txt = bot.timetable.get_day_message(call.from_user.id, 3)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_fri")
async def process_today_command(call: types.CallbackQuery):
    txt = bot.timetable.get_day_message(call.from_user.id, 4)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_sat")
async def process_today_command(call: types.CallbackQuery):
    txt = bot.timetable.get_day_message(call.from_user.id, 5)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)
