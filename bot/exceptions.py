import data

async def handle_schedule_sending_exception(message):
    msg_text = ""

    user_id = str(message.from_user.id)

    if user_id in data.users_and_groups:
        user_group = data.users_and_groups[user_id]

        if user_group in data.schedule:
            msg_text = "Неизвестная ошибка."
        else:
            msg_text = "К сожалению, в данный момент у нас нет расписания для группы {}".format(user_group)

    else:
        msg_text = "Вы ранее не указывали номер группы. Это можно сделать командой /set"

    if msg_text != "":
        await data.bot.send_message(user_id, text=msg_text, parse_mode="Markdown")
