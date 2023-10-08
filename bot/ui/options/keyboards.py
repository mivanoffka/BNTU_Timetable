from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


new_group_button = InlineKeyboardButton("Указать группу ✏️", callback_data="input_group")
mivanoffka_button = InlineKeyboardButton("Познакомиться с разработчиком 🥰", callback_data="show_mivanoffka")
help_button = InlineKeyboardButton("Справка 💡", callback_data="show_help")
bntu_button_3 = InlineKeyboardButton("Сайт БНТУ 🏛️", callback_data="show_bntu")
report_button = InlineKeyboardButton("Отзыв 📬️", callback_data="input_report")
back_home_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_home")
back_to_options_button = InlineKeyboardButton("Назад ↩️", callback_data="goto_options")
donate_button = InlineKeyboardButton("Поддержать нас денюжкой 🏦", callback_data="goto_donations")

options_keyboard = InlineKeyboardMarkup()
options_keyboard.row(bntu_button_3)
options_keyboard.insert(new_group_button)
options_keyboard.row(donate_button)
options_keyboard.row(back_home_button)
options_keyboard.insert(report_button)
options_keyboard.insert(help_button)

back_keybord = InlineKeyboardMarkup()
back_keybord.insert(back_home_button)


links_keyboard = InlineKeyboardMarkup()
bank_button = InlineKeyboardButton("Отправить пожертвование 💸", url="https://pay.netmonet.alfabank.by/42308250")
vk_button = InlineKeyboardButton("VK", url='https://vk.com/maksimka_ivanoffka')
inst_button = InlineKeyboardButton("Instagram", url="https://www.instagram.com/maksimka_ivanoffka")
links_keyboard.insert(vk_button)
links_keyboard.insert(inst_button)
links_keyboard.row(back_to_options_button)