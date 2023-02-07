from excel import convert_keys
import json
import codecs

WEEK_DAYS = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресение")

schedule = None


def is_there_such_a_group(group):
    return group in schedule


def read_json(filename):
    global schedule
    schedule = {}

    with codecs.open('schedule.json', 'r', encoding='utf-8') as f:
        schedule = json.load(f)

    print("Расписание открыто.\n")


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
            output += "\n\n⏰ Пара в {}".format(time)
            output += "\n_{}_".format(day[time])

    return output


def init():
    global schedule
    read_json("schedule.json")


if __name__ == '__main__':
    init()
