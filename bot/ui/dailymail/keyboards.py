from aiogram2.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

dailymail_keyboard = InlineKeyboardMarkup()
evening_button = InlineKeyboardButton("Вечером 🌃", callback_data="set_evening")
morning_button = InlineKeyboardButton("Утром 🌇", callback_data="set_morning")
return_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_home_clr")
disable_button = InlineKeyboardButton("Никогда 🔕", callback_data="set_none")


dailymail_keyboard.insert(morning_button)
dailymail_keyboard.insert(evening_button)
dailymail_keyboard.insert(disable_button)
dailymail_keyboard.row(return_button)
