from bot import data, timetable, keyboards
from datetime import datetime
from aiogram import types

from bot.commands import general, exceptions
from bot.data import dispatcher, users_and_groups
from aiogram.dispatcher import filters

schedule = data.schedule


async def process_day(id, delta=0):
    id = str(id)
    msg = "-"

    print(users_and_groups)

    user_id = id
    user_group = ""

    try:
        user_group = data.users_and_groups[user_id]
        date = datetime.today()
        weekday = datetime.weekday(date) + delta

        weekday = weekday % 7

        msg = timetable.get_day_message(id, weekday)

        #await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=keyboards.bntu_keyboard)
        return msg

    except:
        #await exceptions.handle_schedule_sending_exception(None)
        raise
        pass


# @dispatcher.message_handler(commands=['today'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.today_button.text))
# async def process_today_command(message: types.message):
#     data.increment("today", message.from_user.id)
#     await data.bot.send_message(message.from_user.id, text="_Сейчас поглядим..._", parse_mode="Markdown",
#                                 reply_markup=keyboards.short_keyborad)
#     txt = await process_day(message.from_user.id, 0)
#     await message.answer(text=txt, parse_mode="Markdown")
#     await general.advertise(message.from_user.id)


# @dispatcher.message_handler(commands=['tomorrow'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.tomorrow_button.text))
# async def process_tomorrow_command(message: types.Message):
#     data.increment("tomorrow", message.from_user.id)
#     await data.bot.send_message(message.from_user.id, text="_Сейчас поглядим..._", parse_mode="Markdown",
#                                 reply_markup=keyboards.short_keyborad)
#     await process_day(message.from_user.id, 1)
#     await general.advertise(message.from_user.id)


# @dispatcher.message_handler(commands=['yesterday'])
# async def process_yesterday_command(message: types.Message):
#     await data.bot.send_message(message.from_user.id, text="_Сейчас поглядим..._", parse_mode="Markdown",
#                                 reply_markup=keyboards.short_keyborad)
#     await process_day(message.from_user.id, -1)
#     await general.advertise(message.from_user.id)


# @dispatcher.message_handler(commands=['schedule'])
# async def process_schedule_command(message: types.Message):
#     reply_text = "-"
#
#     user_id = str(message.from_user.id)
#     chat_id = str(message.chat.id)
#     user_group = ""
#
#     if user_id in data.users_and_groups:
#         user_group = data.users_and_groups[user_id]
#
#         reply_text = "*Группа {}, расписание на неделю*\n".format(user_group.upper())
#
#         for i in range(0, 6):
#             weekday = timetable.WEEK_DAYS[i]
#             reply_text += "--------------------------------\n"
#             reply_text += "*{}*".format(weekday.upper())
#             reply_text += timetable.day_to_str(user_group, weekday)
#             reply_text += "\n\n"
#
#     else:
#         if user_group in data.users_and_groups:
#             reply_text = "Извините, в данный момент у нас нет расписания твоей группы. "
#         else:
#             reply_text = "Для начала нужно указать свою группу. " \
#                          "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"
#             reply_text = "Для начала нужно указать свою группу. " \
#                      "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"
#
#     await data.bot.send_message(chat_id, text=reply_text, parse_mode="Markdown")



