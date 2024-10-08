import asyncio
import copy
import os
import logging
import aiogram.utils.exceptions
from aiogram.types import ReplyKeyboardRemove

import bot.ui.keyboards
from bot.ui.start.keyboards import continue_inline, continue_keyboard
from bot.ui.keyboards import delete_keyboard
import config
from bot import data, procedures
from datetime import datetime
from parsing import autoparser
from aiogram import types
from bot.ui.keyboards import cancel_keyboard

from bot.data import dispatcher

from aiogram.dispatcher import filters
from bot.display import update_display
from bot.ui.home.keyboards import home_keyboard
from bot.ui.dailymail.handlers import mail


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["toggle_index"])
async def process_index_command(message: types.Message):
    await bot.display.try_delete(message)

    old_index = copy.copy(autoparser.file_index)
    autoparser.file_index = 1 if old_index == 0 else 0

    await bot.display.renew_display(config.ADMIN_ID, "Индекс обновлён {} -> {}".format(old_index, autoparser.file_index),  bot.ui.keyboards.open_menu_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["test"])
async def process_notify_command(message: types.Message):
    await bot.display.try_delete(message)

    args = message.get_args()
    arg = args[0]
    if arg == "m":
        await mail()
    elif arg == "e":
        await mail('18:00')
    else:
        await mail('06:00')
        await mail('18:00')


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["notify"])
async def process_notify_command(message: types.Message):
    await bot.display.try_delete(message)
    inf_mes = message.html_text[8:]
    lst = data.users_db.get_list()

    await notify(lst, inf_mes)


async def notify(lst, inf_mes):
    if len(inf_mes) > 4000:
        return

    else:

        lst_len = len(lst)
        sent_count = 0

        for uinfo in lst:
            try:
                await bot.display.renew_display(uinfo.id, inf_mes, home_keyboard)
                # await data.bot.send_message(uinfo.id, text=inf_mes, parse_mode="HTML",
                #                             reply_markup=bot.ui.keyboards.delete_keyboard)
                sent_count += 1
                logging.info("Message #{} sent.".format(sent_count))
            except aiogram.utils.exceptions.BotBlocked:
                try:
                    data.users_db.delete(str(uinfo.id))
                except:
                    pass

                pass
            except:
                pass

        await bot.display.renew_display(config.ADMIN_ID, "Рассылка завершена ({}/{})".format(sent_count, lst_len),
                                        home_keyboard)

        # data.bot.send_message(config.ADMIN_ID, txt="Рассылка завершена ({}/{})".format(sent_count, lst_len),
        #                       reply_markup=bot.ui.keyboards.delete_keyboard)


def get_stats_text():
    text = "Действия пользователей, начиная с {}:\n".format(data.datacollector.reset_time)

    for key in data.datacollector.stats:
        text += '\n   "{}" : {} раз'.format(key, data.datacollector.stats[key])

    text += '\n\nПроявили активность {} из {} пользователей.'.format(len(data.datacollector.recent_users),
                                                                      len(data.users_db.get_list()))

    return text


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["stats"])
async def process_stats_command(message: types.Message):
    await bot.display.try_delete(message)

    text = get_stats_text()

    args = message.get_args()
    if "reset" in args:
        data.datacollector.reset()

    # await data.bot.send_message(config.ADMIN_ID, text=txt, reply_markup=o)
    await bot.display.update_display(config.ADMIN_ID, text, bot.ui.keyboards.open_menu_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["update"])
async def process_update_command(message: types.Message):
    await bot.display.try_delete(message)
    await bot.display.renew_display(config.ADMIN_ID, "Начинаем обновление... 🔄", None)

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(update())
    except:
        await bot.display.renew_display(config.ADMIN_ID, "Не удалось обновить расписание. ❌",
                                        bot.ui.keyboards.open_menu_keyboard)
        raise


async def update():
    logging.info("Schedule updating started...")
    try:
        autoparser.download_and_parse()
        data.schedule = procedures.load_schedule()
        await bot.display.renew_display(config.ADMIN_ID, "Расписание успешно обновлено! ✅",
                                    bot.ui.keyboards.open_menu_keyboard)
        logging.info("Schedule succesfully updated!")
    except Exception as e:
        await bot.display.renew_display(config.ADMIN_ID, "Не удалось обновить расписание... ❌",
                                    bot.ui.keyboards.open_menu_keyboard)



@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["danya"])
async def process_danya_command(message: types.Message):
    await bot.display.try_delete(message)
    msg = "Сердечная благодарность вам, любимый Данила Сергеевич! Мы без вас как без рук! ❤️"
    await message.bot.send_message("154246218", text=msg, reply_markup=bot.ui.keyboards.delete_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["danik"])
async def process_danik_command(message: types.Message):
    await bot.display.try_delete(message)
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


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["animations"])
async def process_animations_command(message: types.Message):
    await bot.display.try_delete(message)

    data.global_animations = not data.global_animations

    txt = "Анимации ВЫКЛ 🔴"
    if data.global_animations:
        txt = "Анимации ВКЛ 🟢"

    await bot.display.update_display(config.ADMIN_ID, txt, bot.ui.keyboards.open_menu_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["mailing"])
async def process_animations_command(message: types.Message):
    await bot.display.try_delete(message)

    data.mailing = not data.mailing

    txt = "Рассылка ВЫКЛ 🔴"
    if data.mailing:
        txt = "Рассылка ВКЛ 🟢"

    await bot.display.update_display(config.ADMIN_ID, txt, bot.ui.keyboards.open_menu_keyboard)


@dispatcher.message_handler(filters.IDFilter(config.ADMIN_ID), commands=["message"])
async def process_message_command(message: types.Message):
    await update_display(message.from_user.id, "ы", bot.ui.keyboards.delete_keyboard, no_menu=True)
