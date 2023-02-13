from bot import data, main_commands, weekdays_commands, exceptions, keyboards, days_commands, in_out
from aiogram import types
import copy


async def handle_emul_commands(msg: types.message):
    if msg.from_user.id in data.waiting_for_group_num:
        await continue_setting(msg)

    else:
        await in_out.save_copy(data.users_and_groups)

        if msg.text == keyboards.today_button.text:
            await days_commands.process_today_command(msg)

        elif msg.text == keyboards.tomorrow_button.text:
            await days_commands.process_tomorrow_command(msg)

        elif msg.text == keyboards.set_button.text or msg.text == keyboards.new_group_button.text:
            await start_setting(msg.from_user.id)

        elif msg.text == keyboards.another_day_button.text:
            await another_days(msg)

        elif msg.text == keyboards.week_button.text:
            await main_commands.process_week_command(msg)

        elif msg.text == keyboards.mon_button.text:
            await weekdays_commands.process_mon_command(msg)

        elif msg.text == keyboards.tue_button.text:
            await weekdays_commands.process_tue_command(msg)

        elif msg.text == keyboards.wed_button.text:
            await weekdays_commands.process_wed_command(msg)

        elif msg.text == keyboards.thu_button.text:
            await weekdays_commands.process_thu_command(msg)

        elif msg.text == keyboards.fri_button.text:
            await weekdays_commands.process_fri_command(msg)

        elif msg.text == keyboards.sat_button.text:
            await weekdays_commands.process_sat_command(msg)

        elif msg.text == keyboards.schedule_button.text:
            await days_commands.process_schedule_command(msg)

        elif msg.text == keyboards.help_button.text:
            await data.bot.send_message(msg.from_user.id, text="_Этот раздел пока не готов..._",
                                        reply_markup=keyboards.options_keyboard, parse_mode="Markdown")

        elif msg.text == keyboards.ret_button.text:
            await data.bot.send_message(msg.from_user.id, text="_Возвращаемся..._",
                                        reply_markup=keyboards.menu_keyboard, parse_mode="Markdown")

        elif msg.text == keyboards.settings_button.text:
            await data.bot.send_message(msg.from_user.id, text="_Открываем опции..._",
                                        reply_markup=keyboards.options_keyboard, parse_mode="Markdown")

        elif msg.text == keyboards.mivanoffka_button.text:
            await mivanoffka(msg)

        elif msg.text == keyboards.open_menu_button.text:
            await data.bot.send_message(msg.from_user.id, text="_Открываем меню..._",
                                        reply_markup=keyboards.menu_keyboard, parse_mode="Markdown")

        elif msg.text == keyboards.open_menu_button_2.text:
            await data.bot.send_message(msg.from_user.id, text="_Открываем меню..._",
                                        reply_markup=keyboards.weekdays_keyboard, parse_mode="Markdown")

        else:
            return False

    return True


async def mivanoffka(message: types.Message):
    msg = "<b>Вот он — <u>Максимка Иваноффка!</u></b> ☺️ \n"\
          "<i>\nМой бесподобный создатель, заботливый администратор, да и просто замечательный человек!</i>"

    await data.bot.send_message(message.from_user.id, text=msg, parse_mode="HTML", reply_markup=keyboards.links_keyboard)


async def another_days(msg: types.Message):
    await data.bot.send_message(msg.from_user.id, text="_Смотрим дни недели..._",
                                reply_markup=keyboards.weekdays_keyboard, parse_mode="Markdown")


async def start_setting(user_id):
    if user_id not in data.waiting_for_group_num:
        data.waiting_for_group_num.append(user_id)

    msg_text = " 📲 _Просто введите номер группы и отправьте как сообщение._"

    await data.bot.send_message(user_id, text=msg_text, reply_markup=keyboards.ReplyKeyboardRemove(), parse_mode="Markdown")


async def continue_setting(message: types.Message):
    data.waiting_for_group_num.remove(message.from_user.id)

    new_message = types.Message()
    new_message = copy.copy(message)
    new_message.text = "/set {}".format(message.text)

    await main_commands.process_set_command(new_message)
