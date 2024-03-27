import time
from pathlib import Path

import asyncio
from bot import data, procedures

from aiogram import types
from bot.data import dispatcher

from bot.ui.keyboards import cancel_keyboard, open_menu_keyboard, delete_keyboard, donations_and_delete_keyboard
import random

ads = ["<b>Если вы довольны ботом, не забудьте рассказать о нём друзьям!</b>\n\n💫 http://t.me/bntu_timetable_bot",
       "<b>🗳️ Есть что сказать? Оставьте отзыв! </b>\n\nСделать это можно в разделе «Опции».",
       "<b>💞 Хотите поддержать проект? </b>\n\nОтправьте нам копеечку на чай, мы тоже хотим кушать!",
       "<b>📩 Расписание не обязательно проверять вручную!</b>\n\nВ разделе «Рассылка» можно "
       "настроить ежедневную доставку расписания."
       ]

keyboards = [delete_keyboard, delete_keyboard, donations_and_delete_keyboard, delete_keyboard]


@dispatcher.callback_query_handler(text="delete_message")
async def process_cancel_command(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer()


async def advertise(user_id):
    await asyncio.sleep(1)
    value = random.randint(1, 6)
    if value == 1:
        ad_num = random.randint(1, len(ads)) - 1
        await data.bot.send_message(user_id, text=ads[ad_num], parse_mode="HTML",
                                    reply_markup=keyboards[ad_num], disable_web_page_preview=True)
