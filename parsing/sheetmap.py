import xlrd
import copy
from parsing.sector import Sector

DAYS_LIST = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']


def unmerged_value(rowx, colx, thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo, clo)
    return thesheet.cell_value(rowx, colx)


def is_group_num(txt):
    txt = txt.replace("гр. ", "")
    group_num = txt[0:8]
    if str.isdigit(group_num):
        return True
    else:
        return False


def fix_str(txt):
    txt = str(txt)
    num = 0
    new_txt = ''
    prev = '   '

    for c in txt:
        will_do = not (c == ' ' and prev == ' ')
        if will_do:
            new_txt += c
        prev = c

    return new_txt


def fix_sheet_value(value):
    if type(value) == float:
        return str(value)[:-2]
    else:
        return str(value)


class SheetMap:
    width: int
    height: int

    start_y: int
    begin_y: int
    end_y: int

    start_x: int

    group_nums = {}
    times = {}

    raw_sheet = None

    def __init__(self, raw_sheet, format='excel'):
        if format == 'excel':
            self.get = self.get_excel_value

        self.raw_sheet = raw_sheet
        self.reformat()

    def get_excel_value(self, y, x, appendix):
        return unmerged_value(y, x, self.raw_sheet)

    def get(self, y, x, appendix=None):
        pass

    def reformat(self):
        self.explore_horizontal()
        self.explore_times()
        self.get_group_names()

        # print("\nY: from {}-{} to {}; {}".format(self.start_y, self.begin_y, self.end_y, self.start_x))
        # print(self.group_nums)
        # print(self.times)

    def explore_horizontal(self):
        raw_sheet = self.raw_sheet

        start = -1
        begin = -1
        end = -1
        h = -1

        y_pos = 0


        txt: str
        txt = "undefined"
        while start < 40:
            txt: str
            txt = self.get(start, 1, raw_sheet)
            txt = txt.upper()

            if txt in ("ЧАСЫ", "ВРЕМЯ"):
                break

            start += 1

        begin = start + 1
        while begin < 30:
            txt: str
            txt = self.get(begin, 1, raw_sheet)

            txt = txt.upper()

            if txt not in ("ЧАСЫ", "ВРЕМЯ"):
                break


            begin += 1

        end = start
        while end < 200:
            txt: str
            txt1 = self.get(end, 0, raw_sheet).upper()
            txt2 = self.get(end, 1, raw_sheet).upper()

            if (txt1 == "" and txt2 == "") or ("НАЧАЛЬНИК УМУ" in txt1 and "НАЧАЛЬНИК УМУ" in txt2) or (txt1 == "" and "НАЧАЛЬНИК УМУ" in txt2):
                break

            end += 1

        self.start_y = start
        self.begin_y = begin
        self.end_y = end

    def explore_times(self):
        raw_sheet = self.raw_sheet

        y = self.begin_y
        x = 1

        txt: str
        txt = self.get(y, x, raw_sheet)

        dy = 0
        if self.get(y, x, raw_sheet) != self.get(y + 2, x, raw_sheet):
            dy = 2
        elif self.get(y, x, raw_sheet) != self.get(y + 4, x, raw_sheet):
            dy = 4

        y = self.begin_y
        dy = 0
        while self.get(y, x, raw_sheet) == self.get(y + dy, x, raw_sheet):
            dy += 1

            if dy > 20:
                break

        weekdays = [0, 1, 2, 3, 4, 5]

        times = dict.fromkeys(weekdays, None)
        previous_day = "undefined"

        index = -1
        while y < self.end_y:
            dy = 0
            while self.get(y, x, raw_sheet) == self.get(y + dy, x, raw_sheet):
                dy += 1

                if dy > 20:
                    break

            time: str
            day: str
            time = self.get(y, x, raw_sheet)

            day = self.get(y, x - 1, raw_sheet)

            if previous_day != day:
                index += 1
                if index > 5:
                    self.end_y = y
                    break
                times[weekdays[index]] = {}

            previous_day = day
            times[weekdays[index]][time] = dy

            y += dy
        self.times = times

    def get_group_names(self):
        worksheet = self.raw_sheet

        group_y = 0
        group_x = 0

        xs = []

        for x in range(2, 10):
            for y in range(self.start_y, self.begin_y):
                txt = str(self.get(y, x, None))
                txt = txt.replace("гр. ", "")
                if txt != "":
                    xs.append(x)
                    break

        for x in xs:
            if x != 0:
                group_x = x
                break


        self.start_x = group_x

        for y in range(self.start_y, self.begin_y):
            txt = str(self.get(y, group_x, worksheet))
            txt = txt.replace("гр. ", "")
            if is_group_num(txt):
                group_y = y
                break

        groups = {}
        x = copy.copy(group_x)
        y = copy.copy(group_y)

        dx = 0
        while is_group_num(str(self.get(group_y, x, worksheet))):
            txt = str(self.get(group_y, x, worksheet))
            txt = txt.replace("гр. ", "")
            group_num = txt[0:8]

            dx = self.groups_distance(x, group_y)
            # print(dx)
            # print(group_num, ": ", dx)

            groups[group_num] = dx
            x += dx

        self.group_nums = groups

    def groups_distance(self, x, y):
        group = str(self.get(y, x, self.raw_sheet))
        distance = 1

        while str(self.get(y, x + distance, self.raw_sheet)) == group:
            distance += 1

        return distance

    def parse(self):
        timetables = dict.fromkeys(self.group_nums, [])

        dx = 0
        pos_x = self.start_x
        for group_name in self.group_nums:
            dx = self.group_nums[group_name]

            timetables[group_name] = self.get_group_table(pos_x, dx)

            pos_x += dx

        schedule = self.convert_table_to_dict(timetables)

        return schedule

    def get_group_table(self, pos_x, dx):
        matrix = []

        breaker = False

        for i in range(self.begin_y, self.end_y):

            if breaker:
                break

            line = []
            for j in range(pos_x, pos_x + dx):

                value = fix_str(fix_sheet_value(self.get(i, j, self.raw_sheet)))
                if value != '':
                    if "Начальник УМУ" not in value:
                        value = value.replace('\n', ' ')
                        line.append(value)
                    else:
                        breaker = True
                        break

                else:
                    line.append('_')
            matrix.append(line)
            #print(line)
        table = []

        index = -1
        for day_num in range(0, 6):
            times = self.times[day_num]
            day = []
            if times is None:
                continue
            for time in times:
                lesson = []
                for j in range(0, times[time]):

                    index += 1

                    if index >= self.end_y - self.begin_y:
                        break

                    lesson.append(matrix[index])


                day.append(lesson)
            table.append(day)

        return table

    def convert_table_to_dict(self, tb):
        group_names = self.group_nums

        schedule = dict.fromkeys(group_names)

        for key in group_names:
            raw_group_table = tb[key]

            group_schedule = dict.fromkeys(DAYS_LIST)

            tb_len = len(raw_group_table)

            for i in range(0, tb_len):
                raw_day = raw_group_table[i]

                times = self.times[i]
                times_list = []
                for time in times:
                    times_list.append(time)

                day = dict.fromkeys(times_list)

                day_len = len(raw_day)
                for j in range(0, day_len):
                    raw_lesson = raw_day[j]

                    sec = Sector(raw_lesson)
                    info = sec.process()
                    info = self.fix_info(info)

                    day[times_list[j]] = info

                group_schedule[DAYS_LIST[i]] = day
            schedule[key] = group_schedule

        return schedule

    def fix_info(self, info):
        if info == "<Пусто>" or info is None or info == "":
            return info

        info = info.replace("ф и з и ч е с к а я к у л ь т у р а", "Физическая культура")
        info = info.replace("физическая культура", "Физическая культура")
        info = info.replace(" к ", ", корп. ")
        info = info.replace(" 8.30 ", " ❗ 8.30 ❗ ")
        info = info.replace(" 9.55 ", " ❗ 9.55 ❗ ")
        info = info.replace(" 10.25 ", " ❗ 10.25 ❗ ")
        info = info.replace(" 12.10 ", " ❗ 12.10 ❗ ")
        info = info.replace(" 13.55 ", " ❗ 13.55 ❗ ")
        info = info.replace(" 14.15 ", " ❗ 14.15 ❗ ")
        info = info.replace(" 8.00-13.15 ", " ❗ 8.00-13.15 ❗ ")
        info = info.replace(" 13.55-17.15 ", " ❗ 13.55-17.15 ❗ ")

        for i in range(0, 5):
            info = info.replace("СГМ {}".format(i), "СГМ-{}".format(i))

        for i in range(0, 5):
            info = info.replace("{} П ".format(i), "{}П ".format(i))

        return info