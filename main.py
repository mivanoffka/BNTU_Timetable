import copy
import schedule
import xlrd

import json
import codecs
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЧтобы получить своё расписание, пожалуйста, укажи номер группы!"
                        "\n\nДля этого воспользуйся командой\n   /set <номер группы>")


def get_day_message(user_group, weekday):
    msg = ""
    if weekday != 6:
        weekday = schedule.WEEK_DAYS[weekday]

        msg = "*Группа {}, {}*".format(user_group.upper(), weekday.upper())

        msg += schedule.print_lesson(user_group, weekday)

    else:
        msg = "Сегодня воскресенье. Отдыхаем!"

    return msg


@dp.message_handler(commands=['today'])
async def process_today_command(message: types.Message, delta=0):
    msg = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in users:
        user_group = users[user_id]

        date = datetime.today()
        weekday = datetime.weekday(date) + delta

        weekday = weekday % 7

        msg = get_day_message(user_group, weekday)

    else:
        msg = "Для начала нужно указать свою группу. \nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    #await message.reply(reply_text, parse_mode="Markdown")
    await bot.send_message(chat_id, text=msg, parse_mode="Markdown")


@dp.message_handler(commands=['tomorrow'])
async def process_tomorrow_command(message: types.Message):
    await process_today_command(message, 1)


@dp.message_handler(commands=['yesterday'])
async def process_yesterday_command(message: types.Message):
    await process_today_command(message, -1)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message, delta=0):
    reply_text = ""

    chat_id = str(message.chat.id)

    reply_text += "Список команд:   "
    reply_text += "\n   /start - начало работы с ботом"
    reply_text += "\n   /set <номер_группы> - так вы укажете вашу группу"
    reply_text += "\n   /my_group - вывод номера группы, который вы ранее указали"
    reply_text += "\n   /today, /yesterday, /tomorrow - вывод расписание на сегодня, вчера и завтра соответственно"
    reply_text += "\n   /week - расписание на всю неделю"

    await bot.send_message(chat_id, text=reply_text)


@dp.message_handler(commands=['week'])
async def process_week_command(message: types.Message):
    reply_text = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in users:
        user_group = users[user_id]

        reply_text = "*Группа {}, расписание на неделю*\n".format(user_group.upper())

        for i in range(0, 6):
            weekday = schedule.WEEK_DAYS[i]
            reply_text += "--------------------------------\n"
            reply_text += "*{}*".format(weekday.upper())
            reply_text += schedule.print_lesson(user_group, weekday)
            reply_text += "\n\n"

    else:
        reply_text = "Для начала нужно указать свою группу. " \
                     "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    print(reply_text)
    await bot.send_message(chat_id, text=reply_text, parse_mode="Markdown")


@dp.message_handler(commands=['my_group'])
async def process_my_group_command(message: types.Message):
    reply_text = "-"

    user_id = str(message.from_user.id)

    if user_id in users:
        reply_text = "Твоя группа - {}".format(users[user_id])
    else:
        reply_text = "Кажется, ты раньше не указывал группу... \nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    await message.reply(reply_text)


@dp.message_handler(commands=['set'])
async def process_set_command(message: types.Message):
    reply_text = ""

    group = message.get_args()

    user_id = str(message.from_user.id)

    if schedule.is_there_such_a_group(group):
        reply_text = "Принято. Твоя группа - {}".format(group)

        users[user_id] = group

    else:
        reply_text = "К сожалению, пока мы не обслуживаем вашу группу. Постараемся это исправить"

        if user_id in users:
            users.pop(user_id)

    await message.reply(reply_text)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    msg_text = "Неизвестная команда. Используйте /help для получения списка команд"
    await bot.send_message(msg.from_user.id, msg_text)


def read_userlist():
    global users

    with codecs.open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)

    print("Список пользователей открыт.\n")

    for user in users:
        print("{} - {}".format(user, users[user]))


def save_userlist():
    with codecs.open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=3)

    print("Список пользователей сохранён")


if __name__ == '__main__':
    schedule.init()

    read_userlist()

    executor.start_polling(dp)

    save_userlist()
