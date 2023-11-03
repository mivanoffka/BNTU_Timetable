from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# today_button = InlineKeyboardButton("Сегодня 📓", callback_data="show_today")
# tomorrow_button = InlineKeyboardButton("Завтра 📔", callback_data="show_tomorrow")
# weekdays_button = InlineKeyboardButton("Выбрать день недели 🔍", callback_data="goto_weekdays")
# week_button = InlineKeyboardButton("Рассылка 📣", callback_data="goto_dailymail")
# options_button = InlineKeyboardButton("Прочее ⚙️️", callback_data="goto_options")

# today_button = InlineKeyboardButton("Сегодня 📓", callback_data="show_today")
# tomorrow_button = InlineKeyboardButton("Завтра 📕", callback_data="show_tomorrow")
# weekdays_button = InlineKeyboardButton("Выбрать день недели 🔍", callback_data="goto_weekdays")
# week_button = InlineKeyboardButton("Рассылка 📮", callback_data="goto_dailymail")
# options_button = InlineKeyboardButton("Прочее ⚙️️", callback_data="goto_options")

today_button = InlineKeyboardButton("Сегодня 📓", callback_data="show_today")
tomorrow_button = InlineKeyboardButton("Завтра 📔", callback_data="show_tomorrow")
weekdays_button = InlineKeyboardButton("Выбрать день недели 🔍", callback_data="goto_weekdays")
week_button = InlineKeyboardButton("Рассылка 📩", callback_data="goto_dailymail")
options_button = InlineKeyboardButton("Прочее ⚙️️", callback_data="goto_options")


home_keyboard = InlineKeyboardMarkup()
home_keyboard.insert(today_button)
home_keyboard.insert(tomorrow_button)
home_keyboard.row(weekdays_button)
home_keyboard.row(week_button)
home_keyboard.insert(options_button)

