import copy
import timetable
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

users_and_groups = {}

warning_1 = "\n---------------------------------------\nВ расписании могут встретиться пары, помеченные значком (?). Это значит, что, возможно, мне не удалось корректно обработать и показать вам эту позицию в расписании. В таком случае стоит свериться с оригиналом расписания, представленным здесь: bntu.by/raspisanie "

warning_2 = "\n\n\n---------------------------------------\nЗначок (?) в некоторых местах означает, что мне не удалось аккуратно обработать данный "\
            "участок расписания. Отображение таких пар может быть не очень корректным."\
            "Стоит свериться с расписанием на сайте БНТУ. "\
            "Просим прощения и постараемся исправиться.\n\nhttps://bntu.by/raspisanie"

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = str(message.chat.id)
    msg = "Доброго времени суток! \nМеня создали, чтобы помочь вам разобраться с расписанием.\n" \
          "\nОбратите внимание, что сейчас я нахожусь на ранней стадии разработки, и работаю, как погалается, через одно место!"\
                        "\n\nЧтобы узнать своё расписание, пожалуйста, укажите номер вашей группы."\
                        "\n\nДля этого воспользуйтесь командой\n   /set <номер группы>"

    await bot.send_message(chat_id, text=msg, parse_mode="Markdown")


def get_day_message(user_group, weekday):
    msg = ""
    if weekday != 6:
        weekday = schedule.WEEK_DAYS[weekday]

        msg = "*Группа {}, {}*".format(user_group.upper(), weekday.upper())

        msg += schedule.print_lesson(user_group, weekday)

    else:
        msg = "Сегодня воскресенье. Отдыхаем!"

    return msg


async def for_day_of_week(message: types.Message, weekday):
    msg = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in users_and_groups:
        user_group = users_and_groups[user_id]

        date = datetime.today()

        msg = get_day_message(user_group, weekday)

    else:
        if user_group in users_and_groups:
            msg = "Извини, в данный момент у нас нет расписания твоей группы. "
        else:
            msg = "Для начала нужно указать свою группу. \nЭто можно сделать при помощи команды\n   /set <номер_группы>"


    #msg += warning_1
    await bot.send_message(chat_id, text=msg, parse_mode="Markdown")


@dp.message_handler(commands=['today'])
async def process_today_command(message: types.Message, delta=0):
    msg = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in users_and_groups:
        user_group = users_and_groups[user_id]

        if user_group in timetable.schedule:

            date = datetime.today()
            weekday = datetime.weekday(date) + delta

            weekday = weekday % 7

            msg = get_day_message(user_group, weekday)
        else:
            msg = "Извините, в данный момент у нас нет расписания твоей группы. "

    else:
        msg = "Для начала нужно указать свою группу. \nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    #msg += warning_1

    await bot.send_message(chat_id, text=msg, parse_mode="Markdown")


@dp.message_handler(commands=['mon'])
async def process_monday_command(message: types.Message):
    await for_day_of_week(message, 0)


@dp.message_handler(commands=['tue'])
async def process_tuesday_command(message: types.Message):
    await for_day_of_week(message, 1)


@dp.message_handler(commands=['wed'])
async def process_wednesday_command(message: types.Message):
    await for_day_of_week(message, 2)


@dp.message_handler(commands=['thu'])
async def process_thursday_command(message: types.Message):
    await for_day_of_week(message, 3)


@dp.message_handler(commands=['fri'])
async def process_friday_command(message: types.Message):
    await for_day_of_week(message, 4)


@dp.message_handler(commands=['sat'])
async def process_saturday_command(message: types.Message):
    await for_day_of_week(message, 5)


@dp.message_handler(commands=['tomorrow'])
async def process_tomorrow_command(message: types.Message):
    await process_today_command(message, 1)


@dp.message_handler(commands=['yesterday'])
async def process_yesterday_command(message: types.Message):
    await process_today_command(message, -1)

# ------------------------
# Дни недели


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    reply_text = ""

    chat_id = str(message.chat.id)

    reply_text += "Список команд:   "
    reply_text += "\n   /start - начало работы с ботом"
    reply_text += "\n   /set <номер_группы> - так вы укажете вашу группу"
    reply_text += "\n   /my_group - вывод номера группы, который вы ранее указали"
    reply_text += "\n   /groups - узнать, какие группы мы обслуживаем"
    reply_text += "\n   /today, /yesterday, /tomorrow - вывод расписание на сегодня, вчера и завтра соответственно"
    reply_text += "\n   /schedule - расписание на всю неделю"
    reply_text += "\n   /mon, /tue, /wed, /thu, /fri, /sat - вывод расписания на соотв. день недели"

    reply_text += warning_1
    await bot.send_message(chat_id, text=reply_text)


@dp.message_handler(commands=['groups'])
async def process_groups_command(message: types.Message):
    reply_text = ""

    chat_id = str(message.chat.id)

    reply_text += "В данный момент я обслуживаю только 1-й и 2-й курсы дневной формы обучения."
    reply_text += "\nРазбираться с мириадой файлов расписаний старших курсов меня пока не научили..."

    reply_text += "\n\nСписок групп:\n\n"

    for key in timetable.schedule:
        reply_text += "{}, ".format(key)

    await bot.send_message(chat_id, text=reply_text)


@dp.message_handler(commands=['schedule'])
async def process_week_command(message: types.Message):
    reply_text = "-"

    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    user_group = ""

    if user_id in users_and_groups:
        user_group = users_and_groups[user_id]

        reply_text = "*Группа {}, расписание на неделю*\n".format(user_group.upper())

        for i in range(0, 6):
            weekday = timetable.WEEK_DAYS[i]
            reply_text += "--------------------------------\n"
            reply_text += "*{}*".format(weekday.upper())
            reply_text += timetable.print_lesson(user_group, weekday)
            reply_text += "\n\n"

    else:
        if user_group in users_and_groups:
            reply_text = "Извини, в данный момент у нас нет расписания твоей группы. "
        else:
            reply_text = "Для начала нужно указать свою группу. " \
                         "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"
            reply_text = "Для начала нужно указать свою группу. " \
                     "\nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    #reply_text += warning_1

    await bot.send_message(chat_id, text=reply_text, parse_mode="Markdown")


@dp.message_handler(commands=['my_group'])
async def process_my_group_command(message: types.Message):
    reply_text = "-"

    user_id = str(message.from_user.id)

    if user_id in users_and_groups:
        reply_text = "Твоя группа - {}".format(users_and_groups[user_id])
    else:
        reply_text = "Кажется, вы раньше не указывали группу... \nЭто можно сделать при помощи команды\n   /set <номер_группы>"

    await message.reply(reply_text)


@dp.message_handler(commands=['set'])
async def process_set_command(message: types.Message):
    reply_text = ""

    group = message.get_args()

    user_id = str(message.from_user.id)

    if timetable.is_there_such_a_group(group):
        reply_text += "Хорошо. Я запомнил, что ваша группа - {}".format(group)
        reply_text += "\nЧтобы узнать, что делать дальше, воспользуйтесь командой /help"

        users_and_groups[user_id] = group

    else:
        reply_text = "К сожалению, расписания вашей группы у нас пока нет. Постараемся это исправить"

        if user_id in users_and_groups:
            users_and_groups.pop(user_id)

    await message.reply(reply_text)


@dp.message_handler()
async def echo_message(msg: types.Message):
    msg_text = "Неизвестная команда. Используйте /help для получения списка команд"
    await bot.send_message(msg.from_user.id, msg_text)


def read_userlist():
    global users_and_groups

    with codecs.open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)

    print("Список пользователей открыт.\n")

    for user in users:
        print("{} - {}".format(user, users[user]))


def save_userlist():
    with codecs.open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_and_groups, f, ensure_ascii=False, indent=3)

    with codecs.open('bot/users.json', 'w', encoding='utf-8') as f:
        json.dump(users_and_groups, f, ensure_ascii=False, indent=3)

    print("Список пользователей сохранён")


if __name__ == '__main__':
    timetable.init()

    read_userlist()

    executor.start_polling(dp)

    save_userlist()
