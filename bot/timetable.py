from pathlib import Path

from bot import data
import json
from datetime import datetime

from config import BASE_DIR

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


def get_day_message(user_group, weekday):
    msg = ""
    if weekday != 6:
        weekday = WEEK_DAYS[weekday]

        msg = "*{}, группа {}.*".format(weekday, user_group)

        msg += print_lesson(user_group, weekday)

    else:
        msg = "Выходной. Отдыхаем!"

    return msg


def print_lesson(group, weekday):
    output = ""

    timetable = data.schedule[group]
    day = timetable[weekday]

    for time in day:

        info = day[time]

        if info != "<Пусто>" and info is not None:
            #print("Пара в {}".format(time))
            #print("{}".format(day[time]))
            output += "\n\n⏰ *{}* ".format(time)
            output += "\n_{}_".format(day[time])

    return output


def init():
    schedule = {}

    schedule1 = read_json("datasource/schedule.json")

    for key in schedule1:
        schedule[key] = schedule1[key]

    return schedule

if __name__ == '__main__':
    init()
