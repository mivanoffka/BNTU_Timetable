from bot import data, keyboards, in_out
from aiogram import types
import copy

from bot.commands import days, general, weekdays


async def handle(msg: types.Message):
    if msg.from_user.id in data.waiting_for_group_num:
        await continue_setting(msg)

        return True

    if msg.from_user.id in data.waiting_for_sending_report:
        data.waiting_for_sending_report.remove(msg.from_user.id)
        msg.text = "/report " + msg.text
        await general.process_report_command(msg)

        return True

    if msg.from_user.id not in data.recent_users:
        data.recent_users.append(msg.from_user.id)

    if msg.text == keyboards.today_button.text:
        if data.interactions_count["today"] < 9999999:
            data.interactions_count["today"] += 1
        await days.process_today_command(msg)

    elif msg.text == keyboards.tomorrow_button.text:
        if data.interactions_count["tomorrow"] < 9999999:
            data.interactions_count["tomorrow"] += 1
        await days.process_tomorrow_command(msg)

    elif msg.text == keyboards.set_button.text or msg.text == keyboards.new_group_button.text:
        await start_setting(msg.from_user.id)

    elif msg.text == keyboards.another_day_button.text:
        await another_days(msg)

    elif msg.text == keyboards.week_button.text:
        await general.process_week_command(msg)

    elif msg.text == keyboards.mon_button.text:
        await weekdays.process_mon_command(msg)

    elif msg.text == keyboards.tue_button.text:
        await weekdays.process_tue_command(msg)

    elif msg.text == keyboards.wed_button.text:
        await weekdays.process_wed_command(msg)

    elif msg.text == keyboards.thu_button.text:
        await weekdays.process_thu_command(msg)

    elif msg.text == keyboards.fri_button.text:
        await weekdays.process_fri_command(msg)

    elif msg.text == keyboards.sat_button.text:
        await weekdays.process_sat_command(msg)

    elif msg.text == keyboards.report_button.text:
        if msg.from_user.id not in data.recently_sended_report:
            await start_report(msg.from_user.id)
        else:
            m = "⏳ _Вы совсем недавно отправляли нам сообщение..." \
                " Подождите пару минуточек, прежде чем делать это снова!_"
            await data.bot.send_message(msg.from_user.id, text=m, parse_mode="Markdown",
                                        reply_markup=keyboards.short_keyborad)

    elif msg.text == keyboards.bntu_button_3.text:
        await data.bot.send_message(msg.from_user.id, text="✖️ Этот бот не имеет непосредственного отношения"
                                                           " к руководству Белорусского Национального Технического"
                                                           " Университета и создан на общественных началах."
                                                           "\n\n*❗ За всей официальной информацией стоит"
                                                           " обращаться к сайту Университета.*\n\n_🌐 Рекомендуем"
                                                           " вам регулярно сверять представленное здесь расписание"
                                                           " с его оригиналом на сайте._",
                                    reply_markup=keyboards.bntu_keyboard_2, parse_mode="Markdown")
        await general.advertise(msg.from_user.id)

    elif msg.text == keyboards.help_button.text:
        if data.interactions_count["help"] < 9999999:
            data.interactions_count["help"] += 1

        txt = "<u>Ответы на вопросы, которые могли у вас возникнуть.</u>" \
              "<b>\n\n❓ Почему расписание 3-го курса и старше доступно только студентам ФИТР?</b>" \
              "<i>\n\nК сожалению, расписания занятий сведены в одну таблицу Excel только для младших курсов." \
              " У старших же курсов оно разбросано по десятку таблиц, форматирование которых может заметно отличаться" \
              " друг от друга и не может быть обработано одинаковой программой. " \
              "\n\nПо возможности, будет реализовываться полноценная поддержка и для других факультетов," \
              " но полного покрытия ждать, скорее всего, не стоит... 😔</i>" \
              "<b>\n\n❓ Почему деление расписания по подгруппам и неделям не соответствует тому, " \
              "как моя группа в действительности ходит на пары?</b>" \
              "<i>\n\nРасписание взято в «сыром» виде прямо с сайта БНТУ. В рамках" \
              " каждой группы студенты, как правило, договариваются о чередовании пар несколько иначе," \
              " чем там отражено. Но об этом знаете только вы сами. Если вам очень хочется исправить " \
              "чередование для своей группы, напишите мне – может быть, мы что-нибудь придумаем.</i>" \
              "<b>\n\n❓ Почему некоторые занятия отображаются нечитаемым образом?</b>" \
              "<i>\n\nПри составлении оригинальных табличек часто допускаются ошибки и" \
              " случаются расхождения в форматировании одной и той же по смыслу информации. " \
              "Предусмотреть такое заранее не всегда возможно, но стараюсь над этим работать и исправлять.</i>" \
              "\n\n<b>Если есть ещё вопросы - пишите мне!</b>"

        await data.bot.send_message(msg.from_user.id, text=txt,
                                    reply_markup=keyboards.links_keyboard, parse_mode="HTML", )
        await general.advertise(msg.from_user.id)

    elif msg.text == keyboards.ret_button.text:
        await data.bot.send_message(msg.from_user.id, text="_Возвращаемся..._",
                                    reply_markup=keyboards.menu_keyboard, parse_mode="Markdown")
        await general.advertise(msg.from_user.id)

    elif msg.text == keyboards.settings_button.text:
        if data.interactions_count["settings"] < 9999999:
            data.interactions_count["settings"] += 1

        await data.bot.send_message(msg.from_user.id, text="_Открываем опции..._",
                                    reply_markup=keyboards.options_keyboard, parse_mode="Markdown")
        await general.advertise(msg.from_user.id)

    elif msg.text == keyboards.mivanoffka_button.text:
        await mivanoffka(msg)
        await general.advertise(msg.from_user.id)

    elif msg.text == keyboards.open_menu_button.text:
        await data.bot.send_message(msg.from_user.id, text="_Открываем меню..._",
                                    reply_markup=keyboards.menu_keyboard, parse_mode="Markdown")
        await general.advertise(msg.from_user.id)

    elif msg.text == keyboards.open_menu_button_2.text:
        await data.bot.send_message(msg.from_user.id, text="_Открываем меню..._",
                                    reply_markup=keyboards.weekdays_keyboard, parse_mode="Markdown")
        await general.advertise(msg.from_user.id)

    else:
        return False

    return True


async def mivanoffka(message: types.Message):
    if data.interactions_count["mivanoffka"] < 9999999:
        data.interactions_count["mivanoffka"] += 1

    msg = "<b>Вот он — <u>Максимка Иваноффка!</u></b> 🤗 \n"\
          "<i>\nМой бесподобный создатель, заботливый администратор да и просто замечательный человек!</i>"

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

    await general.process_set_command(new_message)


async def start_report(user_id):
    msg_text = "_Хотите указать на ошибку, предложить идею по улучшению бота или просто написать гадостей?_\n"
    msg_text += "\n*Тогда отправьте своё послание как обычное сообщение!*"

    if user_id not in data.waiting_for_sending_report:
        data.waiting_for_sending_report.append(user_id)

    await data.bot.send_message(user_id, text=msg_text, reply_markup=keyboards.ReplyKeyboardRemove(), parse_mode="Markdown")
