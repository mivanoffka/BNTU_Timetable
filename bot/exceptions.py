from bot import data, keyboards


async def handle_schedule_sending_exception(message):
    msg_text = ""

    user_id = str(message.from_user.id)

    if user_id in data.users_and_groups:
        user_group = data.users_and_groups[user_id]

        if user_group in data.schedule:
            msg_text = "Неизвестная ошибка."
        else:
            msg_text = "Мы не обслуживаем группу, номер которой вы указывали ранее, либо он был указан с ошибкой."

    else:
        msg_text = "Кажется, ранее не указывали номер группы... Либо я его забыл 🫣"

    if msg_text != "":
        await data.bot.send_message(user_id, text=msg_text, parse_mode="Markdown", reply_markup=keyboards.new_group_button)
