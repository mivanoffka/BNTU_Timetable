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


def get_num_of_week(weekday=1):
    week_number = datetime.today().isocalendar()[1] % 2

    if week_number == 0:
        week_number = 2

    if weekday > 6:
        if week_number == 1:
            week_number = 2
        else:
            week_number = 1

    return week_number


def get_day_message(id, weekday):
    id = str(id)

    #user_group = data.users_and_groups[id]
    #user_group = data.users_db.get_group(id)
    uinfo = data.users_db.get_info(id)

    num_of_week = get_num_of_week(weekday)
    week_appendix = ""

    if weekday < 6:
        week_appendix = "\n\nТекущая неделя — {}-я по счёту.".format(num_of_week)
    else:
        num_of_week = 1 if num_of_week == 2 else 2
        week_appendix = "\n\nСледующая неделя — {}-я по счёту.".format(num_of_week)

    msg = ""
    if weekday != 6:
        weekday = WEEK_DAYS[weekday]

        msg = "<b>{}, группа {}.</b>".format(weekday, uinfo.group)

        try:
            msg_buf = day_to_str(uinfo.group, weekday)
        except:
            return "❌ <b>В данный момент у нас нет расписания для группы {}</b>\n\n😔 <i>Приносим свои извинения... Возможно, оно появится позже.</i>".format(uinfo.group)


        if msg_buf != "":
            msg += msg_buf
        else:
            msg += "\n\n<i>Пар нет. Отдыхаем!</i>"

        #msg += day_to_str(user_group, weekday)

        msg += "<b>" + week_appendix + "</b>"

    else:
        msg = "<b>Воскресенье – выходной.</b><i> Отдыхаем! 🥳</i>"

    return msg


def day_to_str(group, weekday):
    output = ""

    timetable = data.schedule[group]
    day = timetable[weekday]

    for time in day:

        info = day[time]

        if info != "<Пусто>" and info != "\nПусто" and info is not None:
            output += "\n\n⏰ <b>{}</b> ".format(time)
            output += "<i>{}</i>".format(day[time])

    return output


async def process_day(id, delta=0):
    id = str(id)

    try:
        date = datetime.today()
        weekday = datetime.weekday(date) + delta

        weekday = weekday % 7

        msg = get_day_message(id, weekday)

        return msg

    except:
        pass


def load_schedule():
    schedule = {}

    schedule1 = read_json("datasource/schedule.json")

    for key in schedule1:
        schedule[key] = schedule1[key]

    return schedule


if __name__ == '__main__':
    load_schedule()
