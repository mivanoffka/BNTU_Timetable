
from bot import data, procedures
from aiogram import types
from bot.data import dispatcher

from bot.states import GroupSettingState
from aiogram.dispatcher import FSMContext
from bot.ui.home.keyboards import home_keyboard

from bot.ui.start.keyboards import start_keyboard, back_keyboard, next_keyboard, again_keyboard, continue_reply_button
from aiogram.dispatcher import filters
from bot.ui.handlers import send_ui
import bot.display

@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.display.try_delete(message)
    await do_start(message.from_user.id)


@dispatcher.callback_query_handler(text="start")
async def process_restart_command(call: types.CallbackQuery):
    await do_start(call.from_user.id)


async def do_start(id):
    id = str(id)

    data.increment("start", id)

    #data.users_and_groups[id] = "NULL"
    data.users_db.insert(id, "NULL", "NULL")

    msg = ("👋<b> Ещё раз здравствуйте!</b> \n\n<i>Перед тем, как продолжить,"
           " вам необходимо указать группу, студентом которой вы являетесь.</i> \n\n")

    data.users_db.update_message(id, "NULL")
    await bot.display.update_display(id, msg, start_keyboard)

    #await data.bot.send_message(id, text=msg, parse_mode="Markdown", reply_markup=start_keyboard)


@dispatcher.message_handler(state=GroupSettingState.awaiting)
async def process_group_input(message: types.Message, state: FSMContext):
    await bot.display.try_delete(message)
    reply_text = ""

    group = message.text.split()[0]

    user_id = str(message.from_user.id)


    if procedures.is_there_such_a_group(group):
        reply_text += "<b>🥳 Вы указали группу {}!</b>".format(group)
        reply_text += "\n\n<i>Теперь вам доступен полный функционал бота.</i>"

        await bot.display.update_display(message.from_user.id, reply_text, home_keyboard, no_menu=True)
        #await message.answer(reply_text, reply_markup=home_keyboard, parse_mode="Markdown")
        #data.users_and_groups[user_id] = group
        data.users_db.insert(user_id, group, str(message.from_user.username))

    else:
        reply_text = "🥲 Кажется, вы что-то не так ввели. Либо у меня пока нету расписания для вашей группы..."
        await bot.display.update_display(message.from_user.id, reply_text, home_keyboard, no_menu=True)
        #await message.answer(reply_text, reply_markup=again_keyboard, parse_mode="Markdown")

    await state.finish()



@dispatcher.message_handler(filters.Text(equals=continue_reply_button.text))
async def process_continue_message(message: types.Message):
    await bot.display.try_delete(message)

    if data.users_db.is_authorized(message.from_user.id):
        await send_ui(message.from_user.id)
    else:
        await do_start(message.from_user.id)
