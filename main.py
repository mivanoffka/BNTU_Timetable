import threading

from datetime import datetime
from bot import data, timetable, in_out, keyboards
import bot.commands
from bot.commands import general, days, weekdays, admin, buttoned

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

import random
from config import BASE_DIR
from pathlib import Path
import urllib.request


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


def random_download_spam():
    random_urls = ["https://files.bntu.by/s/qNjn1hCFhHatBiF/download",
                   "https://files.bntu.by/s/GiNiyutLywFOlX6/download",
                   "https://files.bntu.by/s/G8yIM958ClBY8ud/download",
                   "https://files.bntu.by/s/ORjI3tly33pwGZX/download",
                   "https://files.bntu.by/s/VSLosddrsj412o9/download",
                   "https://files.bntu.by/s/OHA27qBIAoLaqtN/download",
                   "https://files.bntu.by/s/sNYPkNMjKc7UCkZ/download",
                   "https://files.bntu.by/s/ORR7pxqXZ7ZmF0J/download",
                   "https://files.bntu.by/s/RiKOH8ddb1f0RgT/download"]

    number: int = random.randint(1, len(random_urls))

    for i in range(0, number):
        try:
            destination = Path(BASE_DIR / "parsing/sheets/tra.sh")
            urllib.request.urlretrieve(random_urls[i], destination)

        except:
            pass


if __name__ == '__main__':
    random_download_spam()

    data.interactions_count = dict.fromkeys(["today", "tomorrow", "weekdays", "week", "settings", "mivanoffka", "help"])
    for key in data.interactions_count:
        data.interactions_count[key] = 0

    now = datetime.now()
    data.interactions_count["time"] = now.strftime("%d/%m/%Y %H:%M:%S")


    data.schedule = timetable.init()
    data.bot = Bot(token=TOKEN)
    data.dp = Dispatcher(data.bot)

    data.users_and_groups = in_out.read_userlist()

    auto_saving_thread = threading.Thread(target=in_out.launch_autosaving)
    auto_saving_thread.daemon = True
    auto_saving_thread.start()


    setup_handlers()

    print("Launching bot...")
    print("Version 1.1.X")

    executor.start_polling(data.dp, skip_updates=True)

    in_out.save_userlist(data.users_and_groups)
    print("Data saved.")

