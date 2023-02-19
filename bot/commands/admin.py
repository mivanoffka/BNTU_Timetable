import config
from bot import data, keyboards, timetable
from datetime import datetime
from parsing import autoparser
from aiogram import types


async def is_admin(user_id):
    if str(user_id) != config.ADMIN_ID:
        await data.bot.send_message(user_id, text="У вас нет прав для выполнения данной команды.", parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
        return False
    else:
        return True


async def process_notify_command(message: types.Message):
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


async def process_stats_command(message: types.Message):
    if str(message.from_user.id) != config.ADMIN_ID:
        await data.bot.send_message(message.chat.id, text="У вас нет прав для выполнения данной команды.", parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
    else:
        arg = message.get_args()

        text = "Действия пользователей, начиная с {}:\n".format(data.interactions_count["time"])

        for key in data.interactions_count:
            if key != "time":
                text += "\n   {}: {} раз(а)".format(key, data.interactions_count[key])
                if arg == "reset":
                    data.interactions_count[key] = 0

        if arg == "reset":
            now = datetime.now()
            data.interactions_count["time"] = now.strftime("%d/%m/%Y %H:%M:%S")

        await data.bot.send_message(message.chat.id, text=text, parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)


async def process_users_command(message: types.Message):
    if str(message.from_user.id) != config.ADMIN_ID:
        await data.bot.send_message(message.chat.id, text="У вас нет прав для выполнения данной команды.", parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)
    else:
        text = "Статистика пользователей:"

        group_keys = []
        for user in data.users_and_groups:
            if data.users_and_groups[user] not in group_keys:
                group_keys.append(data.users_and_groups[user])

        stats_dict = dict.fromkeys(group_keys, 0)

        for group in group_keys:
            for user in data.users_and_groups:
                if data.users_and_groups[user] == group:
                    stats_dict[group] += 1

        sum = 0
        for group in stats_dict:
            text += "\n    Гр. {} ({} чел.)".format(group, stats_dict[group])
            sum += stats_dict[group]

        text += "\n\nИтого {} чел.".format(sum)

        await data.bot.send_message(message.chat.id, text=text, parse_mode="Markdown",
                                    reply_markup=keyboards.short_keyborad)


async def process_update_command(message: types.Message):
    if await is_admin(message.from_user.id):
        await data.bot.send_message(message.chat.id, text="Начинаем обновление расписания. 🔄")
        try:
            print("Schedule updating started...")
            autoparser.download_and_parse()
            data.schedule = timetable.init()
            await data.bot.send_message(message.chat.id, text="Расписание успешно обновлено! ✅")
            print("Schedule succesfully updated!")

        except:
            await data.bot.send_message(message.chat.id, text="Не удалось обновить расписание. ❌")


async def process_menu_command(message: types.Message):
    if await is_admin(message.from_user.id):
        await data.bot.send_message(message.chat.id, text="Возвращаю меню...", reply_markup=keyboards)


def setup():
    data.dp.register_message_handler(process_users_command, commands="users", content_types=['text'], state='*')
    data.dp.register_message_handler(process_stats_command, commands="stats", content_types=['text'], state='*')
    data.dp.register_message_handler(process_notify_command, commands="notify", content_types=['text'], state='*')
    data.dp.register_message_handler(process_update_command, commands="update", content_types=['text'], state='*')

