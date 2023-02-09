import data
import lines
import timetable
from datetime import datetime

from aiogram import types
from aiogram import Dispatcher

schedule = data.schedule
users_and_groups = data.users_and_groups


async def process_today_command(message: types.Message, delta=0):
    msg = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in data.users_and_groups:
        user_group = data.users_and_groups[user_id]

        if user_group in timetable.schedule:

            date = datetime.today()
            weekday = datetime.weekday(date) + delta

            weekday = weekday % 7

            msg = timetable.get_day_message(user_group, weekday)
        else:
            msg = "Извините, в данный момент у нас нет расписания твоей группы. "

    else:
        msg = "Для начала нужно указать свою группу. \nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    #msg += warning_1

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown")


async def process_tomorrow_command(message: types.Message):
    await process_today_command(message, 1)


async def process_yesterday_command(message: types.Message):
    await process_today_command(message, -1)


async def process_schedule_command(message: types.Message):
    reply_text = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in data.users_and_groups:
        user_group = data.users_and_groups[user_id]

        reply_text = "*Группа {}, расписание на неделю*\n".format(user_group.upper())

        for i in range(0, 6):
            weekday = timetable.WEEK_DAYS[i]
            reply_text += "--------------------------------\n"
            reply_text += "*{}*".format(weekday.upper())
            reply_text += timetable.print_lesson(user_group, weekday)
            reply_text += "\n\n"

    else:
        if user_group in data.users_and_groups:
            reply_text = "Извини, в данный момент у нас нет расписания твоей группы. "
        else:
            reply_text = "Для начала нужно указать свою группу. " \
                         "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"
            reply_text = "Для начала нужно указать свою группу. " \
                     "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    #reply_text += warning_1

    await data.bot.send_message(chat_id, text=reply_text, parse_mode="Markdown")


def setup():
    data.dp.register_message_handler(process_today_command, commands="today", content_types=['text'], state='*')
    data.dp.register_message_handler(process_tomorrow_command, commands="tomorrow", content_types=['text'], state='*')
    data.dp.register_message_handler(process_yesterday_command, commands="yesterday", content_types=['text'], state='*')
    data.dp.register_message_handler(process_schedule_command, commands="schedule", content_types=['text'], state='*')


