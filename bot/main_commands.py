import data
import lines
from bot import timetable

from aiogram import types


async def process_start_command(message: types.Message):
    chat_id = str(message.chat.id)
    msg = lines.welcome

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown")


async def process_help_command(message: types.Message):
    msg_text = ""

    chat_id = str(message.chat.id)

    msg_text = lines.hlp

    msg_text += lines.warning_1
    await data.bot.send_message(chat_id, text=msg_text)


async def process_set_command(message: types.Message):
    reply_text = ""

    group = message.get_args()

    user_id = str(message.from_user.id)

    if timetable.is_there_such_a_group(group):
        reply_text += "Хорошо. Я запомнил, что ваша группа - {}".format(group)
        reply_text += "\nЧтобы узнать, что делать дальше, воспользуйтесь командой /help"

        #data.users_and_groups[user_id] = group

    else:
        reply_text = "К сожалению, расписания для группы {} у нас пока нет. Постараемся это исправить".format(group)

    data.users_and_groups[user_id] = group

    await message.reply(reply_text)


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

    msg_text = "Сейчас {}-я неделя.".format(week_num)

    await data.bot.send_message(message.chat.id, text=msg_text)


def setup():
    data.dp.register_message_handler(process_start_command, commands="start", content_types=['text'], state='*')
    data.dp.register_message_handler(process_help_command, commands="help", content_types=['text'], state='*')
    data.dp.register_message_handler(process_set_command, commands="set", content_types=['text'], state='*')
    data.dp.register_message_handler(process_groups_command, commands="groups", content_types=['text'], state='*')
    data.dp.register_message_handler(process_week_command, commands="week", content_types=['text'], state='*')
