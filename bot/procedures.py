from bot import data, timetable
from datetime import datetime

schedule = data.schedule


async def process_day(id, delta=0):
    id = str(id)

    try:
        date = datetime.today()
        weekday = datetime.weekday(date) + delta

        weekday = weekday % 7

        msg = timetable.get_day_message(id, weekday)

        return msg

    except:
        pass

async def get_week(id):
    data.increment("week", id)
    week_num = timetable.get_current_week()
    data.interactions_count["week"] += 1
    date = datetime.today()
    weekday = datetime.weekday(date)
    if weekday == 6:
        if week_num == 1:
            weekday = 2
        else:
            weekday = 1
        msg_text = "_С понедельника начнётся {}-я неделя!_ 👌".format(weekday)
    else:
        msg_text = "_Сейчас {}-я неделя!_ 👌".format(week_num)

    return msg_text