

from bot import procedures

from aiogram import types
from bot.data import dispatcher

from bot import data


from bot.ui.weekdays.keyboards import weekdays_keyboard
from bot.ui.advertisement import advertise

from bot.ui.handlers import send_ui
import bot.display

@dispatcher.callback_query_handler(text="show_mon")
async def process_monday_command(call: types.CallbackQuery):
    txt = bot.procedures.get_day_message(call.from_user.id, 0)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
        await bot.display.update_display(call.from_user.id, txt, weekdays_keyboard)
    except:
        pass

    data.datacollector.update_stats("weekday", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_tue")
async def process_tuesday_command(call: types.CallbackQuery):
    txt = bot.procedures.get_day_message(call.from_user.id, 1)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
        await bot.display.update_display(call.from_user.id, txt, weekdays_keyboard)
    except:
        pass

    data.datacollector.update_stats("weekday", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_wed")
async def process_wednesday_command(call: types.CallbackQuery):
    txt = bot.procedures.get_day_message(call.from_user.id, 2)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
        await bot.display.update_display(call.from_user.id, txt, weekdays_keyboard)
    except:
        pass

    data.datacollector.update_stats("weekday", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_thu")
async def process_thursday_command(call: types.CallbackQuery):
    txt = bot.procedures.get_day_message(call.from_user.id, 3)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
        await bot.display.update_display(call.from_user.id, txt, weekdays_keyboard)
    except:
        pass

    data.datacollector.update_stats("weekday", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_fri")
async def process_friday_command(call: types.CallbackQuery):
    txt = bot.procedures.get_day_message(call.from_user.id, 4)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
        await bot.display.update_display(call.from_user.id, txt, weekdays_keyboard)
    except:
        pass

    data.datacollector.update_stats("weekday", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_sat")
async def process_saturday_command(call: types.CallbackQuery):
    txt = bot.procedures.get_day_message(call.from_user.id, 5)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=weekdays_keyboard)
        await bot.display.update_display(call.from_user.id, txt, weekdays_keyboard)
    except:
        pass

    data.datacollector.update_stats("weekday", call.from_user.id)
    await call.answer()
    await advertise(call.from_user.id)

