import threading

from bot import in_out
from bot import data
from bot import timetable
from bot import main_commands
from bot import admin_commands
from bot import weekdays_commands, emulations
from bot import days_commands
from bot import keyboards

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


def setup_handlers():
    main_commands.setup()
    days_commands.setup()
    weekdays_commands.setup()
    admin_commands.setup()


    data.dp.register_message_handler(unknown_handler, content_types=['text'], state='*')


async def unknown_handler(msg: types.Message):

    if not await emulations.handle_emul_commands(msg):
        msg_text = "Кажется, вы что-то не то ввели... 🫠"
        await data.bot.send_message(msg.from_user.id, msg_text, reply_markup=keyboards.short_keyborad)

if __name__ == '__main__':

    data.schedule = timetable.init()
    data.bot = Bot(token=TOKEN)
    data.dp = Dispatcher(data.bot)

    data.users_and_groups = in_out.read_userlist()

    auto_saving_thread = threading.Thread(target=in_out.launch_autosaving)
    auto_saving_thread.daemon = True
    auto_saving_thread.start()

    setup_handlers()

    print("Launching bot...")

    executor.start_polling(data.dp, skip_updates=True)

    in_out.save_userlist(data.users_and_groups)

