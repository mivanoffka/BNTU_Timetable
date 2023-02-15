import xlrd
import copy
import json
from pathlib import Path
from config import BASE_DIR

from parsing.sector import Sector

TIMES = [['8.00-9.35', "9.55-11.30", "11.40-13.15", "13.55-15.30", "15.40-17.15"], ['12.00-13.35', "13.55-15.30", "15.40-17.15", "17.45-19.20", "19.30-21.05"]]
DAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

save_binary_info = False
show_matrix = False

start_x = 0
delta_x = 0
from_start_to_names = 0
start_y = 0
shift = 1

# СЛОВАРЬ ТЕРМИНОВ
#       Сектор - фрагмент экселевской таблицы (как правило матрица 4х4), представляющий одну пару
#       Timetable или table - раписание конкретной группы
#       Schedule - совокупность всех timetable'ов


# -------------------------------------------------------
# ПАРСИНГ РАСПИСАНИЯ ИЗ ТАБЛИЦЫ
# (Функции расположены в порядке возрастания "вложенности")

# Начало парсинга всей книги

def parce_workbook(out_schedule, filename):
    workbook = xlrd.open_workbook(filename, formatting_info=True)
    print("\n----------------------------------\nBook {}".format(filename))

    schedule = {}

    # Число страничек
    sheet_num = workbook.sheets()
    sheet_num = len(sheet_num)

    # Парсинг каждой странички
    for s in range(0, sheet_num):
        try:
            parce_worksheet_start(workbook, s, schedule)
        except:
            print("An error occured while parsing sheet #{}".format(s + 1))
            continue

    for key in schedule:
        out_schedule[key] = schedule[key]


# Парсинг конкретной странички
def parce_worksheet_start(workbook, index, out_schedule):
    worksheet = workbook.sheet_by_index(index)

    global start_y
    global shift
    start_y = find_start(worksheet)

    keys = get_group_names(worksheet)

    local_schedule = parce_worksheet_end(worksheet)

    for key in keys:
        out_schedule[key] = local_schedule[key]

    print("Sheet #{} was successfully parsed".format(index + 1))


def parce_worksheet_end(worksheet):
    group_names = get_group_names(worksheet)
    num_of_groups = len(group_names)

    what_shift(worksheet)

    global shift

    timetables_max = dict.fromkeys(group_names, [])
    for i in range(0, num_of_groups):
        timetables_max[group_names[i]] = get_timetable(worksheet, i)

    shift_tab = TIMES[shift - 1]

    timetable = convert_table_to_dict(group_names, timetables_max, shift_tab)

    return timetable


# Расписание одной группы
def get_timetable(worksheet, num):
    q = num + 1
    # получение элемента K в столбце Q

    matrix = []

    start_column = 2 + (q - 1) * 4
    end_column = 2 + q * 4

    start_row = start_y
    end_row = 132 - 14 + start_y

    for i in range(start_row, end_row):
        line = []
        for j in range(start_column, end_column):
            value = fix_str(fix_sheet_value(unmerged_value(i, j, worksheet)))
            if value != '':
                line.append(value)
            else:
                line.append('_')
        matrix.append(line)

    table = []

    index = 0

    for j in range(0, 5):
        day = []
        for i in range(0, 5):
            lesson = []

            index = j * 5 * 4 + i * 4

            lesson.append(matrix[index])
            lesson.append(matrix[index + 1])
            lesson.append(matrix[index + 2])
            lesson.append(matrix[index + 3])

            day.append(lesson)
        table.append(day)

    index += 4

    day = []
    for i in range(0, 4):
        lesson = []

        lesson.append(matrix[index + i * 4])
        lesson.append(matrix[index + i * 4 + 1])
        lesson.append(matrix[index + i * 4 + 2])
        lesson.append(matrix[index + i * 4 + 3])


        day.append(lesson)
    table.append(day)

    return table


# Объединение недостаточной и избыточной таблиц в готовое распсиание
def convert_table_to_dict(group_names, tb, shift_tab):
    schedule = dict.fromkeys(group_names)

    for key in group_names:
        raw_group_table = tb[key]

        group_schedule = dict.fromkeys(DAYS)

        tb_len = len(raw_group_table)

        for i in range(0, tb_len):
            raw_day = raw_group_table[i]

            day = dict.fromkeys(shift_tab)

            day_len = len(raw_day)
            for j in range(0, day_len):
                raw_lesson = raw_day[j]

                sec = Sector(raw_lesson)
                info = sec.process()
                info = fix_info(info)

                day[shift_tab[j]] = info
            group_schedule[DAYS[i]] = day
        schedule[key] = group_schedule

    return schedule


# -------------------------------------------------------
# ПОЛУЧЕНИЕ ВСПОМОГАТЕЛЬНЫХ СВЕДЕНИЙ ИЗ ТАБЛИЦЫ

# Поиск точки отсчёта
def find_start(worksheet):
    for i in range(0, 20):
        value = worksheet.cell_value(i, 0)
        value = str(value)
        value = value.upper()
        value = remove_spaces(value)
        if value == 'ДНИ':
            return i + 5


# Поиск расстояния между расписаниями групп
def find_delta_x(worksheet, begin_x, begin_y):
    dx = 1
    value = str(worksheet.cell_value(begin_y, begin_x + dx))
    while value == "":
        dx += 1
        value = str(worksheet.cell_value(begin_y, begin_x + dx))

    global delta_x
    delta_x = dx


# Бинарное представления сектора: 1 - запись есть, 0 - записи нет
def binary_sector(sector):
    binary_sector = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    for i in range(0, 4):
        for j in range(0, 4):
            if sector[i][j] != '_':
                binary_sector[i][j] = 1
            else:
                binary_sector[i][j] = 0

    if show_matrix:
        print(binary_sector)

    return binary_sector


def is_group_num(txt):
    if txt == "":
        return False

    for char in txt:
        if not (char.isdigit() or char == '(' or char == ' ' or char == ')'):
            return False

    return True


# Получение списка групп (ключей для словаря)
def get_group_names(worksheet):
    groups = []
    x = 2
    y = copy.copy(start_y)


    value = ""
    #while not (len(value) == 8 and value.isdigit()):
    while not is_group_num(value):
        y -= 1
        value = str(worksheet.cell_value(y, x))
        value = value[:-2]

    find_delta_x(worksheet, x, y)


    global from_start_to_names
    from_start_to_names = start_y - y

    while worksheet.cell_value(y, x) != '':
        groups.append(unmerged_value(y, x, worksheet))
        x += delta_x

    n_groups = []
    for item in groups:
        n_groups.append(str(item)[:-2])

    groups = n_groups
    return groups


# Определение смены, в которую учится факультет (ключи для словаря)
def what_shift(worksheet):
    global shift
    if worksheet.cell_value(start_y, 1) == "8.00- 9.35":
        shift = 1
    else:
        shift = 2


# -------------------------------------------------------
# РАБОТА СО СТРОКАМИ


# Замена пустых строк на '_'
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

def mark_audience(info: str):
    if info[len(info) - 1] != " ":
        info += " "

    pos = info.find(", к. ")
    while pos != -1:
        pos = info.find(", к. ")
        start_pos = copy.copy(pos)
        while info[start_pos] != " ":
            start_pos -= 1

            if pos - start_pos > 5:
                break
        end_pos = copy.copy(pos) + 6
        while info[end_pos] != " ":
            end_pos += 1

            if end_pos - pos > 5:
                break

        aud_info = ""
        for i in range(start_pos, end_pos):
            aud_info += info[i]

        aud_info_new = "a." + aud_info

        aud_info_new = " [" + aud_info_new + "] "

        aud_info_new = aud_info_new.replace("к.", "корп.")
        aud_info_new = aud_info_new.replace("а.a", "a")
        aud_info_new = aud_info_new.replace("а.", "ауд. ")

        info = info.replace(aud_info, aud_info_new)

    return info


def fix_info(info):
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

    for i in range(0, 10):
        info = info.replace("{} П".format(i), "{}П".format(i))

    return info

# Удаление лишних '_'
def fix_info_old(info):
    info = info.replace("_", "")
    info = info.replace(" ,", ",")
    info = info.replace("ф и з и ч е с к а я к у л ь т у р а", "Физическая культура")
    info = info.replace("физическая культура", "Физическая культура")
    info = info.replace(" к ", ", корп. ")
    info = info.replace(".0", "")
    info = info.replace("*", "      •")
    info = info.replace("1-я", "   1-я")
    info = info.replace("2-я", "   2-я")
    info = info.replace("9.55", " ❗ 9.55  ❗ ")
    info = info.replace("80-", "8.00-")
    info = info.replace("80-", "8.00-")

    return info


def fix_sector(sector):
    print_sector(sector)

    s = copy.copy(sector[0][0])
    y_len = len(sector)
    x_len = len(sector[0])

    for i in range(0, y_len):
        for j in range(0, x_len):
            if not (i == 0 and j == 0):
                if sector[i][j] == s:
                    sector[i][j] = "_"

    print(sector)
    return sector


def remove_spaces(txt):
    new_txt = ""
    for c in txt:
        if not c == " ":
            new_txt += c

    return new_txt


# ---------------------------------------------------------
# ПРОЧЕЕ

# Вывод в консоль сектора в виде таблички (ДЛЯ ОТЛАДКИ)
def print_sector(sector, gap=30):
    for i in range(0, len(sector)):
        for j in range(0, len(sector[0])):
            value = str(sector[i][j])
            print(value.center(gap), end=" ")
        print()
    print()


def fix_sheet_value(value):
    if type(value) == float:
        return str(value)[:-2]
    else:
        return str(value)

# Значение в ячейке с учётом объединения ячеек
def unmerged_value(rowx, colx, thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo, clo)
    return thesheet.cell_value(rowx, colx)


# Список ключей словаря --> нормальный итерируемый список
def convert_keys(dict_keys):
    list_keys = []
    for key in dict_keys:
        list_keys.append(key)

    return list_keys


# Сохранение расписания
def save_json(schedule):
    with open(Path(BASE_DIR / 'datasource/schedule.json'), 'w', encoding='UTF-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=3)

    #print("Расписание сохранено.")


# -------------------------------------------------------

def main():
    schedule = {}

    f1 = Path(BASE_DIR/"parsing/sheets/1kurs.xls")
    f2 = Path(BASE_DIR/"parsing/sheets/2kurs.xls")

    parce_workbook(schedule, f1)
    parce_workbook(schedule, f2)

    save_json(schedule)


if __name__ == '__main__':
    main()

