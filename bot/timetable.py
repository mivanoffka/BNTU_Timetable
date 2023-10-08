from pathlib import Path
from config import BASE_DIR

from bot import data
import json
from datetime import datetime



WEEK_DAYS = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресение")

def is_there_such_a_group(group):
    return group in data.schedule


def read_json(filename):
    schedule = {}

    with open(Path(BASE_DIR / filename), 'r', encoding='UTF-8') as f:
        schedule = json.load(f)

    return schedule


def get_current_week():
    week_number = datetime.today().isocalendar()[1] % 2

    if week_number == 0:
        week_number = 2

    return week_number


def get_day_message(id, weekday):
    id = str(id)

    data.increment("weekdays", id)

    user_group = data.users_and_groups[id]

    msg = ""
    if weekday != 6:
        weekday = WEEK_DAYS[weekday]

        msg = "*{}, группа {}.*".format(weekday, user_group)

        msg_buf = day_to_str(user_group, weekday)

        if msg_buf != "":
            msg += msg_buf
        else:
            msg += "\n\n_Пар нет. Отдыхаем!_"

        #msg += day_to_str(user_group, weekday)

    else:
        msg = "*Воскресенье – выходной.*_ Отдыхаем! 🥳_"

    return msg


def day_to_str(group, weekday):
    output = ""

    timetable = data.schedule[group]
    day = timetable[weekday]

    for time in day:

        info = day[time]

        if info != "<Пусто>" and info != "\nПусто" and info is not None:
            output += "\n\n⏰ *{}* ".format(time)
            output += "_{}_".format(day[time])

    return output


def init():
    schedule = {}

    schedule1 = read_json("datasource/schedule.json")

    for key in schedule1:
        schedule[key] = schedule1[key]

    return schedule


if __name__ == '__main__':
    init()
