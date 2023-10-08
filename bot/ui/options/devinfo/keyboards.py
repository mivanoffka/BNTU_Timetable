from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


links_keyboard = InlineKeyboardMarkup()
vk_button = InlineKeyboardButton("VK", url='https://vk.com/maksimka_ivanoffka')
inst_button = InlineKeyboardButton("Instagram", url="https://www.instagram.com/maksimka_ivanoffka")
back_to_options_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_options")
links_keyboard.insert(vk_button)
links_keyboard.insert(inst_button)
links_keyboard.row(back_to_options_button)
