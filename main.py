import threading

from bot import data, timetable, in_out, keyboards
import bot.commands
from bot.commands import general, days, weekdays, admin, buttoned

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


def setup_handlers():
    general.setup()
    days.setup()
    weekdays.setup()
    admin.setup()

    data.dp.register_message_handler(unknown_handler, content_types=['text'], state='*')


async def unknown_handler(msg: types.Message):

    if not await buttoned.handle(msg):
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

