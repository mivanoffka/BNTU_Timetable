from bot import data, keyboards


async def handle_schedule_sending_exception(message):
    msg_text = ""

    user_id = str(message.from_user.id)

    if user_id in data.users_and_groups:
        user_group = data.users_and_groups[user_id]

        if user_group in data.schedule:
            msg_text = "Неизвестная ошибка."
        else:
            msg_text = "В данный момент у меня нет доступа к расписанию вашей группы. Прошу прощения..."
            await data.bot.send_message(user_id, text=msg_text, parse_mode="Markdown",
                                        reply_markup=keyboards.short_keyborad)

    else:
        msg_text = "_Кажется, вы ранее не указывали номер группы. Либо я его забыл... 🫣_"
        await data.bot.send_message(user_id, text=msg_text, parse_mode="Markdown", reply_markup=keyboards.start_keyboard)

