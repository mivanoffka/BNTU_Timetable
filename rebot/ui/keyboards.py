import aiogram
from aiogram.utils.keyboard import InlineKeyboardBuilder
from rebot.ui import text
from rebot.ui.text import ButtonKeys

home_button = aiogram.types.InlineKeyboardButton(text=text.get(ButtonKeys.HOME), callback_data="restart")
home_keyboard = InlineKeyboardBuilder()
home_keyboard.add(home_button)