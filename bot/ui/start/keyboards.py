from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup()
again_keyboard = InlineKeyboardMarkup()
back_keyboard = InlineKeyboardMarkup()

set_button = InlineKeyboardButton("Указать группу ✏️", callback_data="input_group")
question_button = InlineKeyboardButton("Справка ❓", callback_data="goto_question")
menu_button = InlineKeyboardButton("Не указывать 🙅‍♂️", callback_data="goto_home_clr")
back_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_start")

start_keyboard.add(set_button)
#start_keyboard.insert(menu_button)

again_keyboard.add(set_button)
again_keyboard.add(menu_button)

back_keyboard.add(back_button)

next_keyboard = InlineKeyboardMarkup()
next_button = InlineKeyboardButton("Далее ➡️", callback_data="goto_next")
next_keyboard.insert(next_button)


