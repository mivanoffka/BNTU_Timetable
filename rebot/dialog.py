import aiogram
from aiogram.types import InlineKeyboardMarkup, Message
from singleton import Singleton
from data.types import User


class Dialog(metaclass=Singleton):
    __bot: aiogram.Bot

    def __init__(self, bot: aiogram.Bot):
        self.__bot = bot

    async def send_independent_message(self, user: User | int, text: str,
                                       keyboard_to_attach: InlineKeyboardMarkup = None):
        user_id: int = int(user.telegram_id) if (isinstance(user, User)) else int(user)
        message: Message = await self.__bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard_to_attach)

    def send_new_ui_message(self, user: User, text: str,
                            keyboard_to_attach: InlineKeyboardMarkup = None, show_animation: bool = False) -> Message:
        pass

    def update_ui_message(self, user: User, text: str,
                          keyboard_to_attach: InlineKeyboardMarkup = None) -> Message:
        pass
