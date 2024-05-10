import asyncio

import aiogram
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from distributor import Distributor
from tracker import Tracker
from dialog import Dialog

from singleton import Singleton
from config import TOKEN

from logger import log_rotation_and_archiving
from data.database import Database


class Core(metaclass=Singleton):
    __bot: aiogram.Bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
    __dispatcher: Dispatcher = Dispatcher(__bot, storage=MemoryStorage())

    __tracker: Tracker = Tracker()
    __dialog: Dialog = Dialog(__bot)
    __distributor: Distributor = Distributor()
    __database: Database = Database()

    @property
    def tracker(self) -> Tracker:
        return self.__tracker

    @property
    def dialog(self) -> Dialog:
        return self.__dialog

    @property
    def database(self) -> Database:
        return self.__database

    def __init__(self):
        #asyncio.get_event_loop().create_task(log_rotation_and_archiving())
        executor.start_polling(self.__dispatcher, skip_updates=True)

    def callback_query_handler(self, *args, **kwargs):
        return self.__dispatcher.callback_query_handler(*args, **kwargs)


if __name__ == '__main__':
    Core()

