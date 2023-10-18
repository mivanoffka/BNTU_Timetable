from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


delete_keyboard = InlineKeyboardMarkup()
delete_button = InlineKeyboardButton("Закрыть ✖️", callback_data="delete_message")
delete_keyboard.insert(delete_button)

donations_and_delete_keyboard = InlineKeyboardMarkup()
donations_button = InlineKeyboardButton("Пожертвовать 💸", url="https://pay.netmonet.alfabank.by/42308250")
donations_and_delete_keyboard.insert(delete_button)
donations_and_delete_keyboard.insert(donations_button)

cancel_button = InlineKeyboardButton("Отмена ✖️", callback_data="input_cancel")
cancel_keyboard = InlineKeyboardMarkup()
cancel_keyboard.insert(cancel_button)

open_menu_keyboard = InlineKeyboardMarkup()
open_menu_button = InlineKeyboardButton("⬅️ В меню ", callback_data="goto_home_clr")
open_menu_keyboard.add(open_menu_button)

