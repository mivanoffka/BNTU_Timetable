from excel import convert_keys
import json
import codecs

WEEK_DAYS = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресение")

schedule = None


def is_there_such_a_group(group):
    return group in schedule


def read_json(filename):
    schedule = {}

    with codecs.open('schedule.json', 'r', encoding='utf-8') as f:
        schedule = json.load(f)

    print("Расписание открыто.\n")

    return schedule

def get_day_message(user_group, weekday):
    msg = ""
    if weekday != 6:
        weekday = WEEK_DAYS[weekday]

        msg = "*Группа {}, {}*".format(user_group.upper(), weekday.upper())

        msg += print_lesson(user_group, weekday)

    else:
        msg = "Сегодня воскресенье. Отдыхаем!"

    return msg

def print_lesson(group, weekday):
    output = ""

    global schedule

    timetable = schedule[group]
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
    global schedule
    schedule = {}

    schedule1 = read_json("schedule.json")
    schedule2 = read_json("schedule2.json")

    for key in schedule1:
        schedule[key] = schedule1[key]


if __name__ == '__main__':
    init()
