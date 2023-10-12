import asyncio
import copy
import os

import aiogram.utils.exceptions

import bot.ui.keyboards
from bot.ui.start.keyboards import continue_inline, continue_keyboard
from bot.ui.keyboards import delete_keyboard
import config
from bot import data, timetable
from datetime import datetime
from parsing import autoparser
from aiogram import types

from bot.data import dispatcher

from aiogram.dispatcher import filters


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["notify"])
async def process_notify_command(message: types.Message):
    inf_mes = message.html_text[8:]
    if len(inf_mes) > 4000:
        return

    else:
        lst = data.users_db.get_list()
        lst_len = len(lst)
        sent_count = 0

        for uinfo in lst:
            try:
                await data.bot.send_message(uinfo.id, text=inf_mes, parse_mode="HTML",
                                            reply_markup=bot.ui.keyboards.delete_keyboard)
                sent_count += 1
                print("Message #{} sent.".format(sent_count))
            except aiogram.utils.exceptions.BotBlocked:
                try:
                    data.users_db.delete(str(uinfo.id))
                except:
                    pass

                pass

        data.bot.send_message(config.ADMIN_ID, txt="Рассылка завершена ({}/{})".format(sent_count, lst_len),
                              reply_markup=bot.ui.keyboards.delete_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["inform"])
async def process_inform_command(message: types.Message):
    mx = len(data.users_and_groups)
    mn = 0

    lst = copy.copy(data.users_and_groups)

    mes_1 = "🚩 <b>Свистать всех наверх!</b>"
    mes_1 += "\n\n🤖 <i>Бот обновился! Теперь весь его интерфейс устроен несколько иначе...</i>"
    mes_1 += "\n\n🙈 Это может показаться непривычным, но поверьте – так гораздо удобнее! (а главное, нагрузка на сервер куда меньше...)"
    mes_1 +=  "<a href='https://pay.netmonet.alfabank.by/42308250'>\n\n<b><i>💖 Кроме того, теперь вы можете финансово поддержать вашего любимого бота и его не менее любимого разработчика!</i></b></a>"

    mes_2 = "❗ <b>Обратите внимание!</b>"
    mes_2 += "\n\n📝 <i>Всем пользователям необходимо пройти перерегистрацию и заново указать свою учебную группу</i>"
    mes_2 += "\n\n📲 <b>Для этого воспользуйтесь кнопкой «Продолжить ➡️», или же введите команду</b> /start <b>из меню</b>"


    for user_id in lst:
        try:
            if not lst[user_id] == "BLOCKED":
                await data.bot.send_message(user_id, mes_1, parse_mode="HTML", reply_markup=continue_keyboard,
                                            disable_web_page_preview=True)
                await asyncio.sleep(0.5)
                await data.bot.send_message(user_id, mes_2, parse_mode="HTML")

                mn += 1
                print("Message #{} sent.".format(mn))

            await asyncio.sleep(0.5)
        except aiogram.utils.exceptions.BotBlocked:
            try:
                data.users_and_groups[user_id] = "BLOCKED"
            except:
                pass
        except:
            pass

    await data.bot.send_message(config.ADMIN_ID, text="Рассылка завершена!\n{}/{}".format(mn, mx),
                                parse_mode="HTML")


def get_stats_text(message: types.Message):
    arg = message.get_args()

    text = "Действия пользователей, начиная с {}:\n".format(data.interactions_count["time"])

    for key in data.interactions_count:
        if key != "time":
            text += "\n   {}: {} раз(а)".format(key, data.interactions_count[key])
            if arg == "reset":
                data.interactions_count[key] = 0

    text += "\n\nВсего пользователей: " + str(len(data.users_db.get_list()))
    text += "\nНедавно пользовались: " + str(len(data.recent_users))

    if arg == "reset":
        now = datetime.now()
        data.interactions_count["time"] = now.strftime("%d/%m/%Y %H:%M:%S")
        data.recent_users.clear()

    return text


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["stats"])
async def process_stats_command(message: types.Message):
    txt = get_stats_text(message)
    await data.bot.send_message(config.ADMIN_ID, text=txt, reply_markup=delete_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["update"])
async def process_update_command(message: types.Message):
    await data.bot.send_message(message.chat.id, text="Начинаем обновление... 🔄",
                                reply_markup=bot.ui.keyboards.delete_keyboard)
    try:
        data.is_updating = True
        print("Schedule updating started...")
        autoparser.download_and_parse()
        data.schedule = timetable.init()
        await data.bot.send_message(message.chat.id, text="Расписание успешно обновлено! ✅",
                                    reply_markup=bot.ui.keyboards.delete_keyboard)
        print("Schedule succesfully updated!")
        data.is_updating = False
    except:
        data.is_updating = False
        await data.bot.send_message(message.chat.id, text="Не удалось обновить расписание. ❌",
                                    reply_markup=bot.ui.keyboards.delete_keyboard)
        raise
    data.is_updating = False


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["danya"])
async def process_danya_command(message: types.Message):
    msg = "Сердечная благодарность вам, любимый Данила Сергеевич! Мы без вас как без рук! ❤️"
    await message.bot.send_message("154246218", text=msg, reply_markup=bot.ui.keyboards.delete_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["danik"])
async def process_danik_command(message: types.Message):
    msg = "Даниил Дмитриевич, не соизволите ли вы отправиться в пешее эротическое путешествие? 💩"
    await message.bot.send_message("1344775275", text=msg, reply_markup=bot.ui.keyboards.delete_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["reply"])
async def process_reply_command(message: types.Message):
    args = message.get_args()
    id = str(args.split()[0])

    mes = args[len(id) + 1:]

    text = "*Вам поступило сообщение от администрации бота*!\n\n_{}_".format(mes)
    try:
        await data.bot.send_message(id, text=text, parse_mode="Markdown")
        await data.bot.send_message(config.ADMIN_ID, text="Сообщение успешно отправлено!",
                                    parse_mode="Markdown", reply_markup=bot.ui.keyboards.delete_keyboard)
    except:
        await data.bot.send_message(config.ADMIN_ID, text="Не удалось отправить сообщение...",
                                    parse_mode="Markdown")



