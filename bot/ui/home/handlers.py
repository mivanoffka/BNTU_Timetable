import bot.ui.dailymail.keyboards
from bot import data, display, procedures

from aiogram import types
from bot.data import dispatcher

from bot.ui.home.keyboards import home_keyboard
from bot.ui.weekdays.keyboards import weekdays_keyboard
from bot.ui.advertisement import advertise


unauthorized_text = ("⚠️ <b>Для начала укажите группу!</b> \n\n"
                     "<i>Сделать это можно в разделе «Прочее».</i>")


@dispatcher.callback_query_handler(text="show_today")
async def process_today_command(call: types.CallbackQuery):

    txt = unauthorized_text

    uinfo = data.users_db.get_info(str(call.from_user.id))
    if uinfo is not None:
        if uinfo.group is not None:
            txt = await procedures.process_day(call.from_user.id, 0)


    # try:
    #     await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    # except:
    #     pass
    await display.update_display(call.from_user.id, txt, home_keyboard)

    data.datacollector.update_stats("today", call.from_user.id)

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_tomorrow")
async def process_tomorrow_command(call: types.CallbackQuery):
    txt = unauthorized_text

    uinfo = data.users_db.get_info(str(call.from_user.id))
    if uinfo is not None:
        if uinfo.group is not None:
            txt = await procedures.process_day(call.from_user.id, 1)

    # try:
    #     await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=home_keyboard)
    # except:
    #     pass

    await display.update_display(call.from_user.id, txt, home_keyboard)

    data.datacollector.update_stats("tomorrow", call.from_user.id)

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="goto_dailymail")
async def process_home_command(call: types.CallbackQuery):
    uinfo = data.users_db.get_info(str(call.from_user.id))
    if uinfo.group is not None:
        txt = "<i>📬 Хотите, чтобы расписание само отправлялось вам каждый день? Подпишитесь на рассылку! </i>"
        txt += "\n\n<b>❓ Когда бы вы хотели получать сообщения с расписанием?</b>"
        await display.update_display(call.from_user.id, txt, bot.ui.dailymail.keyboards.dailymail_keyboard)
        # await call.message.edit_reply_markup(reply_markup=dailymail_keyboard)

    else:
        txt = unauthorized_text
        await display.update_display(call.from_user.id, txt, bot.ui.home.keyboards.home_keyboard)

    data.datacollector.update_stats("dailymail", call.from_user.id)
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
            await display.update_display(call.from_user.id, unauthorized_text, home_keyboard)
        except:
            pass

    await call.answer()
    await advertise(call.from_user.id)




