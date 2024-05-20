import aiogram
from aiogram2.types import InlineKeyboardMarkup, Message
from singleton import Singleton
import asyncio


class Messenger(metaclass=Singleton):
    __bot: aiogram.Bot

    def __init__(self, bot: aiogram.Bot):
        self.__bot = bot

    async def send_independent_message(self, user_id: int, text: str,
                                       keyboard_to_attach: InlineKeyboardMarkup = None):
        message: Message = await self.__bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard_to_attach)

    async def send_emoji_delay(self, id):
        delay = 0.15
        for i in range(0, 5):
            await self.__bot.send_message(id, "✨")
            await asyncio.sleep(delay)
        pass

    def send_new_ui_message(self, user_id : int, text: str,
                            keyboard_to_attach: InlineKeyboardMarkup = None, show_animation: bool = False) -> Message:
        pass

    def update_ui_message(self, user_id: int, text: str,
                          keyboard_to_attach: InlineKeyboardMarkup = None) -> Message:
        pass

    async def try_edit_message_text(self, message: Message, new_text: str) -> None:
        print(message.message_id)
        await self.__bot.edit_message_text(text=new_text, chat_id=message.from_user.id, message_id=message.message_id)
