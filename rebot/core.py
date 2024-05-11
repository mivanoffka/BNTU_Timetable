import asyncio

import aiogram
from aiogram import Dispatcher
from aiogram import types
from aiogram.fsm.storage.memory import MemoryStorage

from tracker import Tracker
from dialog import Dialog

from singleton import Singleton
from config import TOKEN

from logger import log_rotation_and_archiving
from data.database import Database


class Core(metaclass=Singleton):
    __bot: aiogram.Bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
    __dispatcher: Dispatcher = Dispatcher()

    __tracker: Tracker = Tracker()
    __dialog: Dialog = Dialog(__bot)
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
        pass

    async def launch(self):
        self.__dispatcher.startup.register(self.__on_startup)
        await self.__dispatcher.start_polling(self.__bot, skip_updates=True)

    async def __on_startup(self, dispatcher: Dispatcher):
        await asyncio.get_event_loop().create_task(self.__mailing_loop())
        await asyncio.get_event_loop().create_task(log_rotation_and_archiving())
        print("The bot is running...")

    async def __mailing_loop(self):
        print("Mailing loop is running...")

    def callback_query(self, *args, **kwargs):
        return self.__dispatcher.callback_query(*args, **kwargs)

    def message(self, *args, **kwargs):
        return self.__dispatcher.message(*args, **kwargs)
