from aiogram import types

import bot.display
from bot.data import dispatcher
from bot.ui.options.keyboards import options_keyboard
from bot.ui.advertisement import advertise
from bot import data


@dispatcher.callback_query_handler(text="goto_donations")
async def process_devinfo_command(call: types.CallbackQuery):
    # txt = "<b>Вот он — <u>Максимка Иваноффка!</u></b> 🤗" \
    #       "\n\n<a href='vk.com/maksimka_ivanoffka'>ВКонтакте</a> | " \
    #       "<a href='instagram.com/maksimka_ivanoffka/'>Instagram</a>"\
    #       "<i>\n\nМой бесподобный создатель, заботливый администратор да и просто замечательный человек!</i>"
    data.increment("mivanoffka", call.from_user.id)

    txt = "<b>🤗 Вот он — Максимка Иваноффка!</b>" \
          "\n\n<i>Этот замечательный человек — мой единоличный создатель," \
          " который разрабатывает меня на голом энтузиазме... И он тоже хочет кушать!</i>"\
    "<a href='https://pay.netmonet.alfabank.by/42308250'>\n\n<b>💸 Если вы хотите поддержать проект, то можете отправить нам копеечку на чай!</b></a>"\
            "\n\n<i>Кроме того, Максимка будет очень рад, если вы подпишитесь на его соцсети и напишете ему что-нибудь приятное!</i>"\
    "\n\n<a href='vk.com/maksimka_ivanoffka'><b>ВКонтакте</b></a> | " \
    "<a href='instagram.com/maksimka_ivanoffka/'><b>Instagram</b></a>"
    try:
        #await call.message.edit_text(txt, reply_markup=options_keyboard, disable_web_page_preview=True)
        await bot.display.update_display(call.from_user.id, txt, options_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_bntu")
async def process_bntu_command(call: types.CallbackQuery):
    txt = "🙅‍♂️ Этот бот не имеет отношения " \
        "к руководству БНТУ, не финансируется им и существует на общественных началах."\
        "\n\n<b>❗ За всей официальной информацией стоит"\
        " обращаться к сайту Университета.</b>" \
        "\n\n<i>🌐 Рекомендуем вам регулярно сверять представленное здесь расписание с его оригиналом на сайте.</i>"\
        "\n\n<a href='https://bntu.by/raspisanie'><b>1-2 курс</b></a> | " \
        "<a href='https://bntu.by/faculties'><b>3-4 курс</b></a>"

    try:
        #await call.message.edit_text(txt, reply_markup=options_keyboard, disable_web_page_preview=True)
        await bot.display.update_display(call.from_user.id, txt, options_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


@dispatcher.callback_query_handler(text="show_help")
async def process_help_command(call: types.CallbackQuery):
    data.increment("help", call.from_user.id)

    txt = "<u>Ответы на вопросы, которые могли у вас возникнуть.</u>" \
          "<b>\n\n❓ Почему расписание 3-го курса и старше доступно студентам лишь некоторых факультетов?</b>" \
          "<i>\n\nК сожалению, расписания занятий сведены в одну таблицу Excel только для младших курсов." \
          " У старших же курсов оно разбросано по десятку таблиц, форматирование которых может заметно отличаться" \
          " друг от друга и не может быть обработано одинаковой программой. " \
          "\n\nПо возможности, будет реализовываться полноценная поддержка и для других факультетов," \
          " но полного покрытия ждать, скорее всего, не стоит... 😔</i>" \
          "<b>\n\n❓ Почему деление расписания по подгруппам и неделям не соответствует тому, " \
          "как моя группа в действительности ходит на пары?</b>" \
          "<i>\n\nРасписание взято в «сыром» виде прямо с сайта БНТУ. В рамках" \
          " каждой группы студенты, как правило, договариваются о чередовании пар несколько иначе," \
          " чем там отражено. Но об этом знаете только вы сами.</i>" \
          "<b>\n\n❓ Почему некоторые занятия отображаются нечитаемым образом?</b>" \
          "<i>\n\nПри составлении оригинальных табличек часто допускаются ошибки и" \
          " случаются расхождения в форматировании одной и той же по смыслу информации. " \
          "Предусмотреть такое заранее не всегда возможно, но стараюсь над этим работать и исправлять.</i>"

    try:
        #await call.message.edit_text(txt, reply_markup=options_keyboard, disable_web_page_preview=True)
        await bot.display.update_display(call.from_user.id, txt, options_keyboard)
    except:
        pass

    await call.answer()
    await advertise(call.from_user.id)


