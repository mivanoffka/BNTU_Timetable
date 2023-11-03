import asyncio
import threading

from datetime import datetime

import bot.ui.dailymail.handlers
from bot import procedures, in_out, data
from bot.data import interactions_count, dispatcher

from aiogram.utils import executor
from bot import commands
from bot.ui import handlers, advertisement
from bot.ui.home import handlers as home_handlers
from bot.ui.weekdays import handlers as weekdays_handlers
from bot.ui.options import handlers as options_handlers
from bot.ui.start import handlers as start_handlers
from bot.ui.dailymail import handlers as dailymail_handlers
from bot.users import UsersDB


async def start(dp):
    data.schedule = procedures.load_schedule()
    #data.users_and_groups = in_out.read_userlist()
    data.users_db = UsersDB()

    now = datetime.now()
    interactions_count["time"] = now.strftime("%d/%m/%Y %H:%M:%S")

    # auto_saving_thread = threading.Thread(target=in_out.launch_autosaving)
    # auto_saving_thread.daemon = True
    # auto_saving_thread.start()

    loop = asyncio.get_event_loop()

    #loop.create_task()
    loop.create_task(bot.ui.dailymail.handlers.mailing_loop())

    print("Launching bot...")


async def finish(dp):
    # in_out.save_userlist(data.users_and_groups)
    # print("Data saved.")
    pass


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=start, on_shutdown=finish)


