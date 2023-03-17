import asyncio
import aiogram.utils.exceptions
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
        inf_mes = message.html_text[8:]
        if len(inf_mes) > 4000:
            await data.bot.send_message(message.chat.id, text="Слишком длинное...",
                                        parse_mode="Markdown",
                                        reply_markup=keyboards.short_keyborad)
        else:
            mx = len(data.users_and_groups)
            mn = 0
            for user_id in data.users_and_groups:
                try:
                    if not data.users_and_groups[user_id] == "BLOCKED":
                        await data.bot.send_message(user_id, text=inf_mes, parse_mode="HTML",
                                            reply_markup=keyboards.short_keyborad)
                        print("Message #{} sent.".format(mn))
                        mn += 1

                    await asyncio.sleep(1)
                except aiogram.utils.exceptions.BotBlocked:
                    data.users_and_groups[user_id] = "BLOCKED"
                except:
                    pass

            await data.bot.send_message(config.ADMIN_ID, text="Рассылка завершена!\n{}/{}".format(mn, mx), parse_mode="HTML",
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

        text += "\n\nУникальных пользователей: " + str(len(data.recent_users))

        if arg == "reset":
            now = datetime.now()
            data.interactions_count["time"] = now.strftime("%d/%m/%Y %H:%M:%S")
            data.recent_users.clear()

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
        await data.bot.send_message(message.chat.id, text="Начинаем обновление... 🔄")
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


async def process_danik_command(message: types.Message):
    if await is_admin(message.from_user.id):
        msg = "даник, иди нахуй"
        await data.bot.send_message("1344775275", text=msg)


async def process_reply_command(message: types.Message):
    if await is_admin(message.from_user.id):
        args = message.get_args()
        id = str(args.split()[0])

        mes = args[len(id)+1:]

        text = "*Вам поступило сообщение*!\n\n_{}_".format(mes)
        try:
            await data.bot.send_message(id, text=text, parse_mode="Markdown", reply_markup=keyboards.short_keyborad)
            await data.bot.send_message(config.ADMIN_ID, text="Сообщение успешно отправлено!",
                                        parse_mode="Markdown", reply_markup=keyboards.short_keyborad)
        except:
            await data.bot.send_message(config.ADMIN_ID, text="Не удалось отправить сообщение...",
                                        parse_mode="Markdown", reply_markup=keyboards.short_keyborad)


def setup():
    data.dp.register_message_handler(process_danik_command, commands="danik", content_types=['text'], state='*')
    data.dp.register_message_handler(process_users_command, commands="users", content_types=['text'], state='*')
    data.dp.register_message_handler(process_stats_command, commands="stats", content_types=['text'], state='*')
    data.dp.register_message_handler(process_notify_command, commands="notify", content_types=['text'], state='*')
    data.dp.register_message_handler(process_update_command, commands="update", content_types=['text'], state='*')
    data.dp.register_message_handler(process_reply_command, commands="reply", content_types=['text'], state='*')

