import in_out
import data
import timetable
import main_commands
import weekdays_commands
import days_commands

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


def setup_handlers():
    main_commands.setup()
    days_commands.setup()
    weekdays_commands.setup()

    data.dp.register_message_handler(unknown_handler, content_types=['text'], state='*')


async def unknown_handler(msg: types.Message):
    msg_text = "Неизвестная команда. Используйте /help для получения списка команд"
    await data.bot.send_message(msg.from_user.id, msg_text)


if __name__ == '__main__':
    timetable.init()

    print(TOKEN)

    data.schedule = timetable.schedule
    data.bot = Bot(token=TOKEN)
    data.dp = Dispatcher(data.bot)
    data.users_and_groups = in_out.read_userlist()

    setup_handlers()
    executor.start_polling(data.dp)

    in_out.save_userlist(data.users_and_groups)
