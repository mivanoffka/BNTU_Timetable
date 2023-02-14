import copy
from datetime import datetime

import config
from bot import data
from bot import lines
from bot import timetable
from bot import keyboards, exceptions


from aiogram import types


async def process_inform_command(message: types.Message):
    if str(message.from_user.id) != config.ADMIN_ID:
        await data.bot.send_message(message.chat.id, text="У вас нет прав для выполнения данной команды.", parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
    else:
        inf_mes = message.text[8:]
        if len(inf_mes) > 4000:
            await data.bot.send_message(message.chat.id, text="Слишком длинное...",
                                        parse_mode="Markdown",
                                        reply_markup=keyboards.short_keyborad)
        else:
            for user_id in data.users_and_groups:
                await data.bot.send_message(user_id, text=inf_mes, parse_mode="Markdown",
                                            reply_markup=keyboards.short_keyborad)


async def process_userslist_command(message: types.Message):
    if str(message.from_user.id) != config.ADMIN_ID:
        await data.bot.send_message(message.chat.id, text="У вас нет прав для выполнения данной команды.", parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
    else:
        text = "Список авторизованных пользователей:\n"
        for num in data.users_and_groups:
            text += num + " - " + data.users_and_groups[num]
        await data.bot.send_message(message.chat.id, text=text, parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)


def setup():
    data.dp.register_message_handler(process_userslist_command, commands="userslist", content_types=['text'], state='*')
    data.dp.register_message_handler(process_inform_command, commands="inform", content_types=['text'], state='*')
