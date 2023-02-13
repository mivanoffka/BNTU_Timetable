import copy
from datetime import datetime

from bot import data
from bot import lines
from bot import timetable
from bot import keyboards, exceptions

from aiogram import types


async def process_start_command(message: types.Message):
    chat_id = str(message.chat.id)
    if message.from_user.id not in data.waiting_for_group_num:
        data.waiting_for_group_num.append(message.from_user.id)

    msg = "❗ Обратите внимание! В данный момент я обслуживаю *только первые и вторые курсы* ❗"

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown")

    msg = "👋_ Ещё раз здравствуйте!_* \n\n*Начать работу со мной очень легко. "
    msg += "*Просто введите номер своей группы и отправьте его как сообщение 📲*"

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=keyboards.ReplyKeyboardRemove())




async def process_help_command(message: types.Message):
    msg_text = ""

    chat_id = str(message.chat.id)

    hlp = "Список команд:   "
    hlp += "\n   /start - начало работы с ботом"
    hlp += "\n   /set <номер_группы> - так вы укажете вашу группу"
    hlp += "\n   /groups - узнать, какие группы мы обслуживаем"
    hlp += "\n   /today, /yesterday, /tomorrow - вывод расписание на сегодня, вчера и завтра соответственно"
    hlp += "\n   /schedule - расписание на всю неделю"
    hlp += "\n   /week - узнать, какая сейчас неделя (1-я или 2-я)"
    hlp += "\n   /mon, /tue, /wed, /thu, /fri, /sat - вывод расписания на соотв. день недели"
    hlp += "\n   /help - справка о командах (которую вы сейчас наблюдаете)"

    msg_text = hlp

    await data.bot.send_message(chat_id, text=msg_text)

async def process_set_command(message: types.Message):
    reply_text = ""

    group = message.get_args()

    user_id = str(message.from_user.id)

    if timetable.is_there_such_a_group(group):
        reply_text += "*Отлично! 😋*"
        reply_text += "\n\n_Теперь вам доступно меню, из которого легко получить расписание на любой день._"
        await message.reply(reply_text, reply_markup=keyboards.short_keyborad, parse_mode="Markdown")
        data.users_and_groups[user_id] = group

    else:
        reply_text = "Кажется, вы что-то не так ввели. Либо у меня пока нету расписания для вашей группы...\n\n❗ Обратите внимание! В данный момент я обслуживаю *только первые и вторые курсы* ❗"
        await message.reply(reply_text, reply_markup=keyboards.start_keyboard, parse_mode="Markdown")



async def process_groups_command(message: types.Message):
    reply_text = ""

    chat_id = str(message.chat.id)

    reply_text += "В данный момент я обслуживаю только 1-й и 2-й курсы дневной формы обучения."
    reply_text += "\nРазбираться с мириадой файлов расписаний старших курсов меня пока не научили..."

    reply_text += "\n\nСписок групп:\n\n"

    for key in data.schedule:
        reply_text += "{}, ".format(key)

    await data.bot.send_message(chat_id, text=reply_text)


async def process_week_command(message: types.Message):
    week_num = timetable.get_current_week()

    date = datetime.today()
    weekday = datetime.weekday(date)
    if weekday == 6:
        if weekday == 1:
            weekday = 2
        else:
            weekday = 1
        msg_text = "С понедельника начнётся {}-я неделя 👌".format(weekday)
    else:
        msg_text = "Сейчас {}-я неделя 👌".format(week_num)

    await data.bot.send_message(message.chat.id, text=msg_text, parse_mode="Markdown", reply_markup=keyboards.bntu_keyboard)

async def process_remove_command(message: types.Message):
    await message.reply("Убираем шаблоны сообщений", reply_markup=keyboards.ReplyKeyboardRemove())

def setup():
    data.dp.register_message_handler(process_start_command, commands="start", content_types=['text'], state='*')
    data.dp.register_message_handler(process_help_command, commands="help", content_types=['text'], state='*')
    data.dp.register_message_handler(process_set_command, commands="set", content_types=['text'], state='*')
    data.dp.register_message_handler(process_groups_command, commands="groups", content_types=['text'], state='*')
    data.dp.register_message_handler(process_week_command, commands="week", content_types=['text'], state='*')
    data.dp.register_message_handler(process_remove_command, commands="remove", content_types=['text'], state='*')
