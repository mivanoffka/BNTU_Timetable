import asyncio
from datetime import datetime
import bot.ui.dailymail.handlers
from bot import procedures, in_out, data
from bot.data import dispatcher
from logger import log_rotation_and_archiving
from aiogram.utils import executor
from bot.users import UsersDB
from bot.datacollector import DataCollector

# ЭТИ ИМПОРТЫ НУЖНЫ, НЕСМОТРЯ НА ТО ЧТО IDE ТАК НЕ СЧИТАЕТ
import logging
from bot import commands
from bot.ui import handlers, advertisement
from bot.ui.home import handlers as home_handlers
from bot.ui.weekdays import handlers as weekdays_handlers
from bot.ui.options import handlers as options_handlers
from bot.ui.start import handlers as start_handlers
from bot.ui.dailymail import handlers as dailymail_handlers


async def start(dp):
    data.schedule = procedures.load_schedule()
    data.users_db = UsersDB()
    data.datacollector = DataCollector()

    now = datetime.now()

    loop = asyncio.get_event_loop()
    loop.create_task(log_rotation_and_archiving())
    loop.create_task(bot.ui.dailymail.handlers.mailing_loop())

    print("Launching bot...")


async def finish(dp):
    pass


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=start, on_shutdown=finish)


