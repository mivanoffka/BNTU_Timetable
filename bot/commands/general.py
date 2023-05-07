from pathlib import Path

import config
from config import BASE_DIR

import random
from datetime import datetime

from bot import *

from aiogram import types


async def process_start_command(message: types.Message):
    chat_id = str(message.chat.id)
    if message.from_user.id not in data.waiting_for_group_num:
        data.waiting_for_group_num.append(message.from_user.id)

    msg = "*Какие группы обслуживаются?*"
    msg += "\n  •  ФИТР - группы всех 4-х курсов"
    msg += "\n  •  Остальные факультеты - только 1 и 2 курсы"

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=keyboards.ReplyKeyboardRemove())

    msg = "👋* Ещё раз здравствуйте!* \n\n_Начать работу со мной очень легко._\n\n"
    msg += "*Просто введите номер своей группы и отправьте его как сообщение 📲*"

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=keyboards.ReplyKeyboardRemove())


async def process_set_command(message: types.Message):
    reply_text = ""

    group = message.get_args()

    user_id = str(message.from_user.id)

    if timetable.is_there_such_a_group(group):
        reply_text += "*Отлично! 🥳*"
        reply_text += "\n\n_Теперь вам доступно меню, из которого легко получить расписание на любой день._"
        await message.reply(reply_text, reply_markup=keyboards.short_keyborad, parse_mode="Markdown")
        data.users_and_groups[user_id] = group

    else:
        reply_text = "🥲 Кажется, вы что-то не так ввели. Либо у меня пока нету расписания для вашей группы..."
        await message.reply(reply_text, reply_markup=keyboards.start_keyboard, parse_mode="Markdown")


async def advertise(user_id):
    value = random.randint(0, 100)
    if value < 6:
        msg = "<b>Если вы довольны ботом, не забудьте " \
              "рассказать о нём друзьям!</b>\n\n💫 http://t.me/bntu_timetable_bot"
        await data.bot.send_message(user_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)
    if value > 94:
        msg = "<b>🔎 Обнаружили ошибку? Сообщите нам! " \
              "</b>\n\nСделать это можно в опциях."
        await data.bot.send_message(user_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)


async def update_warning(user_id):
    msg = "Прямо сейчас бот не может вам ответить, так как обновляет расписание... " \
          "Пожалуйста, повторите попытку через пару минуточек!"
    await data.bot.send_message(user_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)


async def process_week_command(message: types.Message):
    if data.interactions_count["week"] < 9999999:
        data.interactions_count["week"] += 1

    week_num = timetable.get_current_week()
    data.interactions_count["week"] += 1
    date = datetime.today()
    weekday = datetime.weekday(date)
    if weekday == 6:
        if week_num == 1:
            weekday = 2
        else:
            weekday = 1
        msg_text = "_С понедельника начнётся {}-я неделя!_ 👌".format(weekday)
    else:
        msg_text = "_Сейчас {}-я неделя!_ 👌".format(week_num)

    await data.bot.send_message(message.chat.id, text=msg_text, parse_mode="Markdown", reply_markup=keyboards.bntu_keyboard)


async def process_report_command(message: types.Message):
    if message.from_user.id not in data.recently_sended_report:
        report = message.get_args()
        report_mes = ""
        id = str(message.chat.id)
        group = ""
        if id in data.users_and_groups:
            group = data.users_and_groups[id]
        if group:
            report_mes += "(" + group + ") "
        report_mes += "{}:   ".format(id)
        report_mes += report

        msg = "-"
        if len(report) > 1024:
            msg = "*Ваше сообщение слишком длинное...*\n_Может, сможете выразиться лаконичнее?_👉🏻👈🏻"
        else:
            filename = "datasource/reports.txt"
            with open(Path(BASE_DIR / filename), 'a', encoding='UTF-8') as f:
                f.write(report_mes)

            data.recently_sended_report.append(message.from_user.id)

            msg = "Ваше сообщение успешно отправлено! 📨"

            await data.bot.send_message(config.ADMIN_ID, text=report_mes, parse_mode="Markdown",
                                        reply_markup=keyboards.short_keyborad)

        await data.bot.send_message(message.chat.id, text=msg, parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
    else:
        m = "⏳ _Вы совсем недавно отправляли нам сообщение... Подождите пару минуточек, прежде чем делать это снова!_"
        await data.bot.send_message(message.chat.id, text=m, parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)



def setup():
    data.dp.register_message_handler(process_start_command, commands="start", content_types=['text'], state='*')
    data.dp.register_message_handler(process_set_command, commands="set", content_types=['text'], state='*')
    data.dp.register_message_handler(process_week_command, commands="week", content_types=['text'], state='*')
    data.dp.register_message_handler(process_report_command, commands="report", content_types=['text'], state='*')