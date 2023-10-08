import bot.timetable
from bot import keyboards, data, timetable
from bot.commands import general, exceptions
from datetime import datetime


import random

from aiogram import types

from bot.data import dispatcher
from aiogram.dispatcher import filters

schedule = data.schedule
users_and_groups = data.users_and_groups


# @dispatcher.message_handler(filters.Text(equals=keyboards.weekdays_keyboard))
# async def for_day_of_week(message: types.Message, weekday):
#     await data.bot.send_message(message.from_user.id, text="_Сейчас поглядим..._", parse_mode="Markdown",
#                                 reply_markup=keyboards.short_keyborad_2)
#     msg = bot.timetable.get_day_message(message.from_user.id, weekday)
#     await data.bot.send_message(message.chat.id, text=msg, parse_mode="Markdown", reply_markup=keyboards.bntu_keyboard)
#
#     await general.advertise(message.from_user.id)


# @dispatcher.message_handler(commands=["monday", "mon"])
# @dispatcher.message_handler(filters.Text(equals=keyboards.mon_button.text))
# async def process_mon_command(message: types.Message):
#     await for_day_of_week(message, 0)
#
#
# @dispatcher.message_handler(commands=["tuesday", "tue"])
# @dispatcher.message_handler(filters.Text(equals=keyboards.tue_button.text))
# async def process_tue_command(message: types.Message):
#     await for_day_of_week(message, 1)
#
#
# @dispatcher.message_handler(commands=["wednesday", "wed"])
# @dispatcher.message_handler(filters.Text(equals=keyboards.wed_button.text))
# async def process_wed_command(message: types.Message):
#     await for_day_of_week(message, 2)
#
#
# @dispatcher.message_handler(commands=["thursday", "thu"])
# @dispatcher.message_handler(filters.Text(equals=keyboards.thu_button.text))
# async def process_thu_command(message: types.Message):
#     await for_day_of_week(message, 3)
#
#
# @dispatcher.message_handler(commands=["friday", "fri"])
# @dispatcher.message_handler(filters.Text(equals=keyboards.fri_button.text))
# async def process_fri_command(message: types.Message):
#     await for_day_of_week(message, 4)
#
#
# @dispatcher.message_handler(commands=["saturday", "sat"])
# @dispatcher.message_handler(filters.Text(equals=keyboards.sat_button.text))
# async def process_sat_command(message: types.Message):
#     await for_day_of_week(message, 5)


async def is_user_set(user_id):
    result = False

    user_id = str(user_id)

    if user_id in data.users_and_groups:
        result = True

    return result


async def is_group_in_schedule(user_group):
    result = False

    user_group = str(user_group)

    if user_group in data.schedule:
        result = True

    return result




