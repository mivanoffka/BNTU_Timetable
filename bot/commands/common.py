from datetime import datetime

from bot import data, procedures

from aiogram import types
from bot.data import dispatcher
from bot.ui.handlers import send_ui


# @dispatcher.message_handler(commands=['set'])
# async def process_set_command(message: types.Message):
#     group = message.get_args()
#     user_id = str(message.from_user.id)
#
#     reply_text = ""
#     if timetable.is_there_such_a_group(group):
#         reply_text = "Группа успешно измененена!"
#
#         data.users_and_groups[user_id] = group
#
#     else:
#         reply_text = "🥲 Кажется, вы что-то не так ввели. Либо у меня пока нету расписания для вашей группы..."
#
#     await send_ui(user_id, reply_text)
