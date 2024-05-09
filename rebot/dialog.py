import aiogram
from aiogram.types import InlineKeyboardMarkup, Message
from singleton import Singleton
from usersdb.user import User


class Dialog(metaclass=Singleton):
    __bot: aiogram.Bot

    def __init__(self, bot: aiogram.Bot):
        self.__bot = bot

    def send_independent_message(self, user: User, text: str,
                                 keyboard_to_attach: InlineKeyboardMarkup = None) -> Message:
        pass

    def send_new_ui_message(self, user: User, text: str,
                            keyboard_to_attach: InlineKeyboardMarkup = None) -> Message:
        pass

    def update_ui_message(self, user: User, text: str,
                          keyboard_to_attach: InlineKeyboardMarkup = None) -> Message:
        pass
