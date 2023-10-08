from pathlib import Path

import aiogram.types

import bot.commands.days
import config
from config import BASE_DIR

from bot import data, timetable

from aiogram import types
from bot.commands import buttoned
from bot.data import dispatcher
from aiogram.dispatcher import filters

from bot.states import GroupSettingState, ReportingState
from aiogram.dispatcher import FSMContext
from bot.ui.home.keyboards import home_keyboard
from bot.ui.weekdays.keyboards import weekdays_keyboard
import time

from bot.ui.start.keyboards import start_keyboard, back_keyboard, next_keyboard, again_keyboard


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    data.increment("start", message.from_user.id)

    data.users_and_groups[str(message.from_user.id)] = "undefined"

    chat_id = str(message.chat.id)
    if message.from_user.id not in data.waiting_for_group_num:
        data.waiting_for_group_num.append(message.from_user.id)

    # msg = "*Какие группы обслуживаются?*"
    # msg += "\n  •  ФИТР - группы всех 4-х курсов"
    # msg += "\n  •  Остальные факультеты - только 1 и 2 курсы"
    #
    # await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=next_keyboard)

    msg = "👋* Ещё раз здравствуйте!* \n\n_Перед тем, как продолжить, вам необходимо указать группу, студентом которой вы являетесь._ \n\n"

    await data.bot.send_message(chat_id, text=msg, parse_mode="Markdown", reply_markup=start_keyboard)


@dispatcher.callback_query_handler(text="input_group")
async def process_next_command(call: types.CallbackQuery):
    msg = "*Какие группы обслуживаются?*"
    msg += "\n  •  ФИТР - группы всех 4-х курсов"
    msg += "\n  •  Остальные факультеты - только 1 и 2 курсы"

    await call.message.edit_text(msg, parse_mode="Markdown", reply_markup=next_keyboard)


@dispatcher.message_handler(state=GroupSettingState.awaiting)
async def process_group_input(message: types.Message, state: FSMContext):
    reply_text = ""

    group = message.text.split()[0]

    user_id = str(message.from_user.id)

    if timetable.is_there_such_a_group(group):
        reply_text += "*Отлично! 🥳*"
        reply_text += "\n\n_Теперь вам доступен полный функционал бота._"
        await message.answer(reply_text, reply_markup=home_keyboard, parse_mode="Markdown")
        data.users_and_groups[user_id] = group

    else:
        reply_text = "🥲 Кажется, вы что-то не так ввели. Либо у меня пока нету расписания для вашей группы..."
        await message.answer(reply_text, reply_markup=again_keyboard, parse_mode="Markdown")

    await state.finish()
