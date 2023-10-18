import bot.procedures

from bot import data, display

from aiogram import types
from bot.data import dispatcher

from bot.ui.home.keyboards import home_keyboard
from bot.ui.weekdays.keyboards import weekdays_keyboard
from bot.ui.advertisement import advertise


unauthorized_text = ("⚠️ <b>Для начала укажите группу!</b> \n\n"
                     "<i>Сделать это можно в опциях, либо перезапустив бота.</i>")


@dispatcher.callback_query_handler(text="show_today")
async def process_today_command(call: types.CallbackQuery):
    txt = unauthorized_text
    data.increment("today", call.from_user.id)

    uinfo = data.users_db.get_info(str(call.from_user.id))
    if uinfo is not None:
        if uinfo.group is not None:
            txt = await bot.procedures.process_day(call.from_user.id, 0)

    # try:
    #     await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    # except:
    #     pass
    await bot.display.update_display(call.from_user.id, txt, home_keyboard)

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_tomorrow")
async def process_tomorrow_command(call: types.CallbackQuery):
    txt = unauthorized_text
    data.increment("tomorrow", call.from_user.id)

    uinfo = data.users_db.get_info(str(call.from_user.id))
    if uinfo is not None:
        if uinfo.group is not None:
            txt = await bot.procedures.process_day(call.from_user.id, 1)

    # try:
    #     await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    # except:
    #     pass

    await bot.display.update_display(call.from_user.id, txt, home_keyboard)

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="goto_weekdays")
async def process_weekdays_command(call: types.CallbackQuery):
    uinfo = data.users_db.get_info(str(call.from_user.id))

    if uinfo.group is not None:
        try:
            await call.message.edit_reply_markup(reply_markup=weekdays_keyboard)
        except:
            pass
    else:
        try:
            #await call.message.edit_text(unauthorized_text, parse_mode="Markdown", reply_markup=home_keyboard)
            await bot.display.update_display(call.from_user.id, unauthorized_text, home_keyboard)
        except:
            pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_week")
async def process_week_command(call: types.CallbackQuery):
    txt = await bot.procedures.get_week(call.from_user.id)
    try:
        #await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
        await bot.display.update_display(call.from_user.id, txt, home_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)



