import bot.ui.start.keyboards
from bot import data, procedures
from datetime import datetime
import time
schedule = data.schedule
import aiogram2
import logging


async def try_delete(message):
    try:
        await message.delete()
    except:
        pass


async def send_emoji_delay(id):
    delay = 0.15

    await data.bot.send_message(id, "✨", reply_markup=aiogram2.types.ReplyKeyboardRemove())
    time.sleep(delay)
    await data.bot.send_message(id, "✨")
    time.sleep(delay)
    await data.bot.send_message(id, "✨")
    time.sleep(delay)
    await data.bot.send_message(id, "✨")
    time.sleep(delay)
    await data.bot.send_message(id, "✨")
    time.sleep(delay)


async def send_symbol_delay(chat_id, message_id, keyboard):
    if not data.global_animations:
        return

    keyboard=None
    delay = 0.15
    count = 3

    text = ""
    for i in range(0, count):
        text += "."
        try:
            await data.bot.edit_message_text(chat_id=chat_id,
                                             message_id=message_id,
                                             text=text,
                                             reply_markup=keyboard)

        except:
            pass
        time.sleep(delay)


async def update_display(id, text, keyboard, animation=True, no_menu=False):
    user_info = data.users_db.get_info(id)

    if user_info.message is None:
        await send_display(id, text, keyboard, animation)
    else:
        try:
            if animation:
                if no_menu:
                    await send_symbol_delay(id, user_info.message, None)
                else:
                    await send_symbol_delay(id, user_info.message, keyboard)

            await data.bot.edit_message_text(chat_id=id,
                                             message_id=user_info.message,
                                             text=text,
                                             parse_mode="HTML",
                                             reply_markup=keyboard,
                                             disable_web_page_preview=True)

        except aiogram2.exceptions.MessageNotModified:
            logging.info("same")
            pass
        except:
            await send_display(id, text, keyboard, animation)


async def send_display(id, text, keyboard, animation=True):
    if animation:
        await send_emoji_delay(id)
    message = await data.bot.send_message(id, text, parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)
    data.users_db.update_message(id, message.message_id)


async def renew_display(id, text, keyboard):
    uinfo = data.users_db.get_info(id)

    try:
        await data.bot.delete_message(id, uinfo.message)
    except:
        pass

    data.users_db.update_message(id, "NULL")
    await update_display(id, text, keyboard, animation=False)