from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



# Начальная клавиатура
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
set_button = KeyboardButton("Указать номер группы ✏️")
start_keyboard.add(set_button)

# Главное меню
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
today_button = KeyboardButton("Сегодня 📓")
tomorrow_button = KeyboardButton("Завтра 📔")
another_day_button = KeyboardButton("По дням недели 🔍")
week_button = KeyboardButton("Какая сейчас неделя? 📅")
settings_button = KeyboardButton("Опции ⚙️")

menu_keyboard.insert(today_button)
menu_keyboard.insert(tomorrow_button)
menu_keyboard.row(another_day_button)
menu_keyboard.row(week_button)
menu_keyboard.insert(settings_button)

# Меню дней недели
weekdays_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
mon_button = KeyboardButton("Понедельник 🔴")
tue_button = KeyboardButton("Вторник 🟠")
wed_button = KeyboardButton("Среда 🟡")
thu_button = KeyboardButton("Четверг 🟢")
fri_button = KeyboardButton("Пятница 🔵")
sat_button = KeyboardButton("Суббота 🟣")
weekdays_buttons = [mon_button, tue_button, wed_button, thu_button, fri_button, sat_button]

weekdays_keyboard.row(mon_button)
weekdays_keyboard.insert(tue_button)
weekdays_keyboard.row(wed_button)
weekdays_keyboard.insert(thu_button)
weekdays_keyboard.row(fri_button)
weekdays_keyboard.insert(sat_button)

schedule_button = KeyboardButton("На всю неделю 🗓️")
ret_button = KeyboardButton("Назад ↩️")

weekdays_keyboard.add(ret_button)

#
short_keyborad = ReplyKeyboardMarkup(resize_keyboard=True)
open_menu_button = KeyboardButton("Открыть меню ⭐")
short_keyborad.add(open_menu_button)

short_keyborad_2 = ReplyKeyboardMarkup(resize_keyboard=True)
open_menu_button_2 = KeyboardButton("Открыть меню ✨")
short_keyborad_2.add(open_menu_button_2)

# Опции
options_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
new_group_button = KeyboardButton("Заново указать группу ✏️")
mivanoffka_button = KeyboardButton("Познакомиться с разработчиком 🥰")
help_button = KeyboardButton("Справка 💡")
bntu_button_3 = KeyboardButton("Сайт БНТУ🏛️")
report_button = KeyboardButton("Оставить отзыв 📬️")


options_keyboard.row(bntu_button_3)
options_keyboard.insert(new_group_button)
options_keyboard.row(mivanoffka_button)
options_keyboard.row(ret_button)
options_keyboard.insert(report_button)
options_keyboard.insert(help_button)



links_keyboard = InlineKeyboardMarkup()
vk_button = InlineKeyboardButton("VK", url='https://vk.com/maksimka_ivanoffka')
inst_button = InlineKeyboardButton("Instagram", url="https://www.instagram.com/maksimka_ivanoffka")
links_keyboard.insert(vk_button)
links_keyboard.insert(inst_button)

bntu_keyboard = InlineKeyboardMarkup()
bntu_button = InlineKeyboardButton("Свериться на сайте БНТУ 🏛️", url="https://bntu.by/raspisanie")
bntu_keyboard.add(bntu_button)

bntu_keyboard_2 = InlineKeyboardMarkup()
bntu_button_2 = InlineKeyboardButton("Сайт БНТУ 🏛️", url="https://bntu.by/")
bntu_keyboard_2.add(bntu_button_2)