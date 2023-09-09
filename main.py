import threading

from datetime import datetime
from bot import timetable, in_out, data
from bot.data import interactions_count, users_and_groups, dp

from aiogram.utils import executor
from bot import commands


async def start(dp):
    now = datetime.now()
    interactions_count["time"] = now.strftime("%d/%m/%Y %H:%M:%S")

    auto_saving_thread = threading.Thread(target=in_out.launch_autosaving)
    auto_saving_thread.daemon = True
    auto_saving_thread.start()

    print("Launching bot...")
    print(data.users_and_groups)


async def finish(dp):
    print(data.users_and_groups)
    in_out.save_userlist(data.users_and_groups)
    print("Data saved.")


if __name__ == '__main__':
    data.schedule = timetable.init()
    data.users_and_groups = in_out.read_userlist()

    executor.start_polling(dp, skip_updates=True, on_startup=start, on_shutdown=finish)


