from bot import data, timetable, keyboards
from datetime import datetime
from aiogram import types

from bot.commands import general, exceptions
from bot.data import dispatcher, users_and_groups
from aiogram.dispatcher import filters

schedule = data.schedule

async def process_day(message: types.Message, delta=0):
    msg = "-"

    print(users_and_groups)

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    try:
        user_group = data.users_and_groups[user_id]
        date = datetime.today()
        weekday = datetime.weekday(date) + delta

        weekday = weekday % 7

        msg = timetable.get_day_message(user_group, weekday)

        await data.bot.send_message(chat_id, text="_Сейчас поглядим..._", parse_mode="Markdown", reply_markup=keyboards.short_keyborad)
        await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=keyboards.bntu_keyboard)

        await general.advertise(user_id)

    except:
        await exceptions.handle_schedule_sending_exception(message)

    await general.advertise(message.from_user.id)


@dispatcher.message_handler(commands=['today'])
@dispatcher.message_handler(filters.Text(equals=keyboards.today_button.text))
async def process_today_command(message: types.message):
    data.increment("today", message.from_user.id)
    await process_day(message, 0)


@dispatcher.message_handler(commands=['tomorrow'])
@dispatcher.message_handler(filters.Text(equals=keyboards.tomorrow_button.text))
async def process_tomorrow_command(message: types.Message):
    data.increment("tomorrow", message.from_user.id)
    await process_day(message, 1)


@dispatcher.message_handler(commands=['yesterday'])
async def process_yesterday_command(message: types.Message):
    await process_day(message, -1)


@dispatcher.message_handler(commands=['schedule'])
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
            reply_text += timetable.day_to_str(user_group, weekday)
            reply_text += "\n\n"

    else:
        if user_group in data.users_and_groups:
            reply_text = "Извините, в данный момент у нас нет расписания твоей группы. "
        else:
            reply_text = "Для начала нужно указать свою группу. " \
                         "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"
            reply_text = "Для начала нужно указать свою группу. " \
                     "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    await data.bot.send_message(chat_id, text=reply_text, parse_mode="Markdown")



