import time
from pathlib import Path

import asyncio
from bot import data, procedures

from aiogram import types
from bot.data import dispatcher


from bot.ui.keyboards import cancel_keyboard, open_menu_keyboard, delete_keyboard, donations_and_delete_keyboard
import random


@dispatcher.callback_query_handler(text="delete_message")
async def process_cancel_command(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()


async def advertise(user_id):
    await asyncio.sleep(1)
    value = random.randint(1, 8)
    if value == 3:
        value = random.randint(1, 3)
        if value == 1:
            msg = "<b>Если вы довольны ботом, не забудьте " \
                  "рассказать о нём друзьям!</b>\n\n💫 http://t.me/bntu_timetable_bot"
            await data.bot.send_message(user_id, text=msg, parse_mode="HTML", reply_markup=delete_keyboard,
                                        disable_web_page_preview=True)
        if value == 2:
            msg = "<b>📨 Есть что сказать? Оставьте отзыв! " \
                  "</b>\n\nСделать это можно в опциях."
            await data.bot.send_message(user_id, text=msg, parse_mode="HTML", reply_markup=delete_keyboard,
                                        disable_web_page_preview=True)
        if value == 3:
            msg = "<b>💞 Хотите поддержать проект? " \
                  "</b>\n\nОтправьте нам копеечку на чай, мы тоже хотим кушать!"
            await data.bot.send_message(user_id, text=msg, parse_mode="HTML",
                                        reply_markup=donations_and_delete_keyboard, disable_web_page_preview=True)
        # if value == 4:
        #     msg = "<b>📌 Надеюсь, вы закрепили диалог с ботом? " \
        #           "</b>\n\nТак вы точно нас не потеряете!"
        #     await data.bot.send_message(user_id, text=msg, parse_mode="HTML", reply_markup=delete_keyboard,
        #                                 disable_web_page_preview=True)
