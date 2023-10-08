from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


website_button = InlineKeyboardButton("Расписание 1-2 курсов 🏛", url="bntu.by/raspisanie")
faculties_button = InlineKeyboardButton("Расписание 3-4 курсов 🗓", callback_data="goto_faculties")
origin_button = InlineKeyboardButton("А где оригинал ❓", callback_data="show_origin")
back_to_options_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_options")


website_keyboard = InlineKeyboardMarkup()
website_keyboard.insert(website_button)
website_keyboard.row(faculties_button)
website_keyboard.row(back_to_options_button)
website_keyboard.insert(origin_button)
