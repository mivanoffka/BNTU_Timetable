import config
from bot import data, keyboards, timetable

from parsing import autoparser
from aiogram import types


async def is_admin(user_id):
    if str(user_id) != config.ADMIN_ID:
        await data.bot.send_message(user_id, text="У вас нет прав для выполнения данной команды.", parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
        return False
    else:
        return True


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
            text += num + " - " + data.users_and_groups[num] + "\n"
        await data.bot.send_message(message.chat.id, text=text, parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)


async def process_update_command(message: types.Message):
    if await is_admin(message.from_user.id):
        await data.bot.send_message(message.chat.id, text="Начинаем обновление расписания. 🔄")
        try:
            autoparser.download_and_parse()
            data.schedule = timetable.init()
            await data.bot.send_message(message.chat.id, text="Расписание успешно обновлено! ✅")

        except:
            await data.bot.send_message(message.chat.id, text="Не удалось обновить расписание. ❌")


async def process_menu_command(message: types.Message):
    if await is_admin(message.from_user.id):
        await data.bot.send_message(message.chat.id, text="Возвращаю меню...", reply_markup=keyboards)


def setup():
    data.dp.register_message_handler(process_userslist_command, commands="users", content_types=['text'], state='*')
    data.dp.register_message_handler(process_inform_command, commands="inform", content_types=['text'], state='*')
    data.dp.register_message_handler(process_update_command, commands="update", content_types=['text'], state='*')
