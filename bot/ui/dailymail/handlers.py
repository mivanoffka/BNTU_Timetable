import asyncio
import copy
import time


from config import ADMIN_ID
import aiogram.utils.exceptions


from bot import data, display, procedures
import bot.ui.dailymail.keyboards
from bot import data, display, procedures

from aiogram import types
from bot.data import dispatcher

from bot.ui.home.keyboards import home_keyboard
from bot.ui.weekdays.keyboards import weekdays_keyboard
from bot.ui.advertisement import advertise
from datetime import datetime

@dispatcher.callback_query_handler(text="set_morning")
async def process_set_morning_command(call: types.CallbackQuery):
    data.users_db.update_time(call.from_user.id, "morning")

    await display.update_display(call.from_user.id, "<b>☑️ Успешно настроено!</b> \n\nТеперь вы будете"
                                                    " получать расписание на текущий день каждое утро.", home_keyboard)

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="set_evening")
async def process_set_morning_command(call: types.CallbackQuery):
    data.users_db.update_time(call.from_user.id, "evening")

    await display.update_display(call.from_user.id, "<b>☑️ Успешно настроено!</b> \n\nТеперь вы будете"
                                                    " получать расписание на следующий день каждый вечер.", home_keyboard)

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="set_none")
async def process_set_morning_command(call: types.CallbackQuery):
    data.users_db.update_time(call.from_user.id, "none")

    await display.update_display(call.from_user.id, "<b>☑️ Успешно настроено!</b> \n\nВы"
                                                    " больше не будете получать ежедневную рассылку расписания.", home_keyboard)


    await call.answer()
    await advertise(call.from_user.id)


async def mailing_loop():
    while data.users_db is None:
        await asyncio.sleep(1)

    times = list()
    if data.users_db is not None:
        times_raw = data.users_db.times

    print("Mailing set to {} and {}".format(times_raw[0][0], times_raw[1][0]))
    for item in times_raw:
        times.append(datetime.strptime(item[0], '%H:%M'))

    zero_time = datetime.strptime('23:55', '%H:%M')
    times.append(zero_time)

    times_iteration = []
    last_time = ""

    while True:
        if len(times_iteration) == 0:
            times_iteration = copy.copy(times)

        print("Checking time...")

        current_time = datetime.now()
        current_time = datetime(1900, 1, 1, datetime.now().hour, datetime.now().minute)

        for t in times_iteration:
            if current_time >= t:
                dt = abs(current_time.hour * 60 + current_time.minute - t.hour * 60 + t.minute)
                if dt < 60 and last_time is not t:
                    last_time = t

                    if t != zero_time:
                        await mail(t)
                    else:
                        await display.renew_display(ADMIN_ID, str(times_iteration),
                                                    home_keyboard)

        await asyncio.sleep(20)


async def mail(t):
    try:
        t = datetime.strptime(t, '%H:%M')
    except:
        pass

    lst = data.users_db.get_list()
    times = list()
    times_raw = data.users_db.times
    for item in times_raw:
        times.append(item[0])

    msg = "Рассылка... Пустая, правда"
    t_str = t.strftime('%H:%M')
    delta = times.index(t_str)

    new_lst = []
    for user in lst:
        if user.time is not None:
            if int(user.time) - 1 == delta:
                new_lst.append(user)

    lst_len = len(lst)
    sent_count = 0

    for uinfo in new_lst:
        try:
            msg = await procedures.process_day(uinfo.id, delta)
            if delta == 0:
                msg = "<b>Вот ваше расписание на сегодня!</b>\n" + msg
            if delta == 1:
                msg = "<b>Вот ваше расписание на завтра!</b>\n" + msg
            await bot.display.renew_display(uinfo.id, msg, home_keyboard)
            # await data.bot.send_message(uinfo.id, text=inf_mes, parse_mode="HTML",
            #                             reply_markup=bot.ui.keyboards.delete_keyboard)
            sent_count += 1
            print("Message #{} sent.".format(sent_count))
        except aiogram.utils.exceptions.BotBlocked:
            try:
                data.users_db.delete(str(uinfo.id))
            except:
                pass

            pass
        except:
            pass






