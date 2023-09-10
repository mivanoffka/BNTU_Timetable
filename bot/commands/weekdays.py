from bot import keyboards, data, timetable
from bot.commands import general, exceptions
from datetime import datetime


import random

from aiogram import types

from bot.data import dispatcher
from aiogram.dispatcher import filters

schedule = data.schedule
users_and_groups = data.users_and_groups


@dispatcher.message_handler(filters.Text(equals=keyboards.weekdays_keyboard))
async def for_day_of_week(message: types.Message, weekday):
    msg = "-"

    data.increment("weekdays", message.from_user.id)

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    try:
        user_group = data.users_and_groups[user_id]

        date = datetime.today()

        msg = timetable.get_day_message(user_group, weekday)

        await data.bot.send_message(chat_id, text="_Сейчас поглядим..._", parse_mode="Markdown", reply_markup=keyboards.short_keyborad_2)
        await data.bot.send_message(message.chat.id, text=msg, parse_mode="Markdown", reply_markup=keyboards.bntu_keyboard)

        await general.advertise(user_id)

    except:
        await exceptions.handle_schedule_sending_exception(message)

    await general.advertise(message.from_user.id)


@dispatcher.message_handler(commands=["monday", "mon"])
@dispatcher.message_handler(filters.Text(equals=keyboards.mon_button.text))
async def process_mon_command(message: types.Message):
    await for_day_of_week(message, 0)


@dispatcher.message_handler(commands=["tuesday", "tue"])
@dispatcher.message_handler(filters.Text(equals=keyboards.tue_button.text))
async def process_tue_command(message: types.Message):
    await for_day_of_week(message, 1)


@dispatcher.message_handler(commands=["wednesday", "wed"])
@dispatcher.message_handler(filters.Text(equals=keyboards.wed_button.text))
async def process_wed_command(message: types.Message):
    await for_day_of_week(message, 2)


@dispatcher.message_handler(commands=["thursday", "thu"])
@dispatcher.message_handler(filters.Text(equals=keyboards.thu_button.text))
async def process_thu_command(message: types.Message):
    await for_day_of_week(message, 3)


@dispatcher.message_handler(commands=["friday", "fri"])
@dispatcher.message_handler(filters.Text(equals=keyboards.fri_button.text))
async def process_fri_command(message: types.Message):
    await for_day_of_week(message, 4)


@dispatcher.message_handler(commands=["saturday", "sat"])
@dispatcher.message_handler(filters.Text(equals=keyboards.sat_button.text))
async def process_sat_command(message: types.Message):
    await for_day_of_week(message, 5)


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


# def setup():
#     data.dp.register_message_handler(process_mon_command, commands="mon", content_types=['text'], state='*')
#     data.dp.register_message_handler(process_tue_command, commands="tue", content_types=['text'], state='*')
#     data.dp.register_message_handler(process_wed_command, commands="wed", content_types=['text'], state='*')
#     data.dp.register_message_handler(process_thu_command, commands="thu", content_types=['text'], state='*')
#     data.dp.register_message_handler(process_fri_command, commands="fri", content_types=['text'], state='*')
#     data.dp.register_message_handler(process_sat_command, commands="sat", content_types=['text'], state='*')

