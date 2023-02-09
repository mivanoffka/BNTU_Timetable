import data
import lines
import timetable
from datetime import datetime

from aiogram import types
from aiogram import Dispatcher

schedule = data.schedule
users_and_groups = data.users_and_groups


async def for_day_of_week(message: types.Message, weekday):
    msg = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in data.users_and_groups:
        user_group = data.users_and_groups[user_id]

        date = datetime.today()

        msg = timetable.get_day_message(user_group, weekday)

    else:
        if user_group in data.users_and_groups:
            msg = "Извини, в данный момент у нас нет расписания твоей группы. "
        else:
            msg = "Для начала нужно указать свою группу. \nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown")


async def process_mon_command(message: types.Message):
    await for_day_of_week(message, 0)


async def process_tue_command(message: types.Message):
    await for_day_of_week(message, 1)


async def process_wed_command(message: types.Message):
    await for_day_of_week(message, 2)


async def process_thu_command(message: types.Message):
    await for_day_of_week(message, 3)


async def process_fri_command(message: types.Message):
    await for_day_of_week(message, 4)


async def process_sat_command(message: types.Message):
    await for_day_of_week(message, 5)


def setup():
    data.dp.register_message_handler(process_mon_command, commands="mon", content_types=['text'], state='*')
    data.dp.register_message_handler(process_tue_command, commands="tue", content_types=['text'], state='*')
    data.dp.register_message_handler(process_wed_command, commands="wed", content_types=['text'], state='*')
    data.dp.register_message_handler(process_thu_command, commands="thu", content_types=['text'], state='*')
    data.dp.register_message_handler(process_fri_command, commands="fri", content_types=['text'], state='*')
    data.dp.register_message_handler(process_sat_command, commands="sat", content_types=['text'], state='*')

