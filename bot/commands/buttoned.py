from bot import data, keyboards, in_out
from aiogram import types
import copy

from bot.commands import days, general, weekdays
from bot.data import dispatcher

from aiogram.dispatcher import filters


# @dispatcher.message_handler(commands=['main_menu'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.open_menu_button.text))
# @dispatcher.message_handler(filters.Text(equals=keyboards.ret_button.text))
# async def process_main_menu_comand(msg: types.Message):
#     await data.bot.send_message(msg.from_user.id, text="_Открываем меню..._",
#                                 reply_markup=keyboards.menu_keyboard, parse_mode="Markdown")
#     await general.advertise(msg.from_user.id)
#
#
# @dispatcher.message_handler(commands=['week_menu'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.another_day_button.text))
# @dispatcher.message_handler(filters.Text(equals=keyboards.open_menu_button_2.text))
# async def process_week_menu_comand(msg: types.Message):
#     await data.bot.send_message(msg.from_user.id, text="_Открываем меню..._",
#                                 reply_markup=keyboards.weekdays_keyboard, parse_mode="Markdown")
#     await general.advertise(msg.from_user.id)
#
#
# @dispatcher.message_handler(commands=['options', 'settings'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.settings_button.text))
# async def process_options_command(msg: types.Message):
#     data.increment("settings", msg.from_user.id)
#
#     await data.bot.send_message(msg.from_user.id, text="_Открываем опции..._",
#                                 reply_markup=keyboards.options_keyboard, parse_mode="Markdown")
#     await general.advertise(msg.from_user.id)
#
#
# @dispatcher.message_handler(commands=['dev'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.mivanoffka_button.text))
# async def mivanoffka(message: types.Message):
#     data.increment("mivanoffka", message.from_user.id)
#
#     msg = "<b>Вот он — <u>Максимка Иваноффка!</u></b> 🤗 \n"\
#           "<i>\nМой бесподобный создатель, заботливый администратор да и просто замечательный человек!</i>"
#
#     await data.bot.send_message(message.from_user.id, text=msg, parse_mode="HTML", reply_markup=keyboards.links_keyboard)
#
#
# @dispatcher.message_handler(commands=['help'])
# @dispatcher.message_handler(filters.Text(equals=keyboards.help_button.text))
# async def process_help_command(message: types.Message):
#     data.increment("help", message.from_user.id)
#
#     txt = "<u>Ответы на вопросы, которые могли у вас возникнуть.</u>" \
#           "<b>\n\n❓ Почему расписание 3-го курса и старше доступно только студентам ФИТР?</b>" \
#           "<i>\n\nК сожалению, расписания занятий сведены в одну таблицу Excel только для младших курсов." \
#           " У старших же курсов оно разбросано по десятку таблиц, форматирование которых может заметно отличаться" \
#           " друг от друга и не может быть обработано одинаковой программой. " \
#           "\n\nПо возможности, будет реализовываться полноценная поддержка и для других факультетов," \
#           " но полного покрытия ждать, скорее всего, не стоит... 😔</i>" \
#           "<b>\n\n❓ Почему деление расписания по подгруппам и неделям не соответствует тому, " \
#           "как моя группа в действительности ходит на пары?</b>" \
#           "<i>\n\nРасписание взято в «сыром» виде прямо с сайта БНТУ. В рамках" \
#           " каждой группы студенты, как правило, договариваются о чередовании пар несколько иначе," \
#           " чем там отражено. Но об этом знаете только вы сами. Если вам очень хочется исправить " \
#           "чередование для своей группы, напишите мне – может быть, мы что-нибудь придумаем.</i>" \
#           "<b>\n\n❓ Почему некоторые занятия отображаются нечитаемым образом?</b>" \
#           "<i>\n\nПри составлении оригинальных табличек часто допускаются ошибки и" \
#           " случаются расхождения в форматировании одной и той же по смыслу информации. " \
#           "Предусмотреть такое заранее не всегда возможно, но стараюсь над этим работать и исправлять.</i>" \
#           "\n\n<b>Если есть ещё вопросы - пишите мне!</b>"
#
#     await data.bot.send_message(message.from_user.id, text=txt,
#                                 reply_markup=keyboards.links_keyboard, parse_mode="HTML", )
#     await general.advertise(message.from_user.id)
#
#
# @dispatcher.message_handler(filters.Text(equals=keyboards.bntu_button_3.text))
# async def process_site_command(message: types.Message):
#     await data.bot.send_message(message.from_user.id, text="✖️ Этот бот не имеет непосредственного отношения"
#                                                        " к руководству Белорусского Национального Технического"
#                                                        " Университета и создан на общественных началах."
#                                                        "\n\n*❗ За всей официальной информацией стоит"
#                                                        " обращаться к сайту Университета.*\n\n_🌐 Рекомендуем"
#                                                        " вам регулярно сверять представленное здесь расписание"
#                                                        " с его оригиналом на сайте._",
#                                 reply_markup=keyboards.bntu_keyboard_2, parse_mode="Markdown")
#     await general.advertise(message.from_user.id)
#
#
# @dispatcher.message_handler(filters.Text(equals=keyboards.another_day_button.text))
# async def process_weekdays_command(msg: types.Message):
#     await data.bot.send_message(msg.from_user.id, text="_Смотрим дни недели..._",
#                                 reply_markup=keyboards.weekdays_keyboard, parse_mode="Markdown")

