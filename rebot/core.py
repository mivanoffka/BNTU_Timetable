import asyncio

import aiogram
from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs, Window, Dialog

from config import TOKEN
from data.data import Data
from messenger import Messenger
from singleton import Singleton


class Core(metaclass=Singleton):
    __bot: aiogram.Bot = aiogram.Bot(token=TOKEN, parse_mode="HTML")
    __dispatcher: Dispatcher = Dispatcher()

    __messenger: Messenger = Messenger(__bot)
    __data: Data = Data()

    __windows: list[Window] = []
    __dialog: Dialog

    @property
    def messenger(self) -> Messenger:
        return self.__messenger

    @property
    def data(self) -> Data:
        return self.__data

    def __init__(self):
        pass

    async def launch(self):
        self.__dispatcher.startup.register(self.__on_startup)
        self.__dialog = Dialog(*self.__windows)
        self.include_router(self.__dialog)
        setup_dialogs(self.__dispatcher)
        await self.__dispatcher.start_polling(self.__bot, skip_updates=True)

    async def __on_startup(self, dispatcher: Dispatcher):
        #await asyncio.get_event_loop().create_task(log_rotation_and_archiving())

        await asyncio.get_event_loop().create_task(self.__mailing_loop())
        print("The bot is running...")

    async def __mailing_loop(self):
        print("Mailing loop is running...")

    async def accept_report(self, user_id: int, report_text: str):
        pass

    # region Декораторы

    def callback_query(self, *args, **kwargs):
        return self.__dispatcher.callback_query(*args, **kwargs)

    def message(self, *args, **kwargs):
        return self.__dispatcher.message(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self.__dispatcher.error(*args, **kwargs)

    def include_router(self, router):
        self.__dispatcher.include_router(router)

    def include_window(self, window: Window):
        self.__windows.append(window)

    # endregion


core: Core = Core()
