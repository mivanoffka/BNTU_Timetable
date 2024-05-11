from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


mon_button = InlineKeyboardButton("Пн. ⚫", callback_data="show_mon")
tue_button = InlineKeyboardButton("Вт. ⚪️", callback_data="show_tue")
wed_button = InlineKeyboardButton("Ср. ⚫", callback_data="show_wed")
thu_button = InlineKeyboardButton("Чт. ⚪", callback_data="show_thu")
fri_button = InlineKeyboardButton("Пт. ⚫", callback_data="show_fri")
sat_button = InlineKeyboardButton("Сб. ⚪", callback_data="show_sat")
back_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_home")

weekdays_keyboard = InlineKeyboardMarkup()

weekdays_keyboard.insert(mon_button)
weekdays_keyboard.insert(tue_button)
weekdays_keyboard.insert(wed_button)
weekdays_keyboard.row(thu_button)
weekdays_keyboard.insert(fri_button)
weekdays_keyboard.insert(sat_button)
weekdays_keyboard.row(back_button)


# mon_button = InlineKeyboardButton("Пн. ⚫", callback_data="show_mon")
# tue_button = InlineKeyboardButton("Вт. ⚪", callback_data="show_tue")
# wed_button = InlineKeyboardButton("Ср. ⚪", callback_data="show_wed")
# thu_button = InlineKeyboardButton("Чт. ⚫", callback_data="show_thu")
# fri_button = InlineKeyboardButton("Пт. ⚫", callback_data="show_fri")
# sat_button = InlineKeyboardButton("Сб. ⚪", callback_data="show_sat")
# back_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_home")
#
# weekdays_keyboard = InlineKeyboardMarkup()
#
# weekdays_keyboard.insert(mon_button)
# weekdays_keyboard.insert(wed_button)
# weekdays_keyboard.insert(fri_button)
# weekdays_keyboard.row(tue_button)
# weekdays_keyboard.insert(thu_button)
# weekdays_keyboard.insert(sat_button)
# weekdays_keyboard.row(back_button)
