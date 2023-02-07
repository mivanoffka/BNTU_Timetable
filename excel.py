import xlrd
import copy
import codecs
import json

TIMES = [['8.00- 9.35', "9.55-11.30", "11.40-13.15", "13.55-15.30", "15.40-17.15"], ['12.00- 13.35', "13.55-15.30", "15.40-17.15", "17.45-19.20", "19.30-21.05"]]
DAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

show_matrix = False

start_pos = 0
shift = 1

# СЛОВАРЬ ТЕРМИНОВ
#       Сектор - фрагмент экселевской таблицы (как правило матрица 4х4), представляющий одну пару
#       Timetable или table - раписание конкретной группы
#       Schedule - совокупность всех timetable'ов


# -------------------------------------------------------
# ПАРСИНГ РАСПИСАНИЯ ИЗ ТАБЛИЦЫ
# (Функции расположены в порядке возрастания "вложенности")

# Начало парсинга всей книги
def parce_workbook(filename):
    # Открытие файла
    workbook = xlrd.open_workbook(filename, formatting_info=True)

    # Будущее расписание
    schedule = {}

    # Число страничек
    sheet_num = workbook.sheets()
    sheet_num = len(sheet_num)

    # Парсинг каждой странички
    for s in range(0, sheet_num):
        try:
            parce_worksheet_start(workbook, s, schedule)
        except:
            print("Исключение при обработке {}-й таблицы".format(s + 1))
            continue

    return schedule


# Парсинг конкретной странички
def parce_worksheet_start(workbook, index, out_schedule):
    worksheet = workbook.sheet_by_index(index)

    global start_pos
    global shift
    start_pos = find_start(worksheet)

    keys = get_group_names(worksheet)

    local_schedule = parce_worksheet_end(worksheet)

    for key in keys:
        out_schedule[key] = local_schedule[key]

    print("Таблица {} успешно обработана".format(index + 1))


def parce_worksheet_end(worksheet):
    # Получение списка групп и их количества
    group_names = get_group_names(worksheet)
    num_of_groups = len(group_names)

    # Определение смены, в которую учится фалькультет
    shift = what_shift(worksheet)

    # Получение двух "сырых" табличек. В одной из них не учитываются объединённые ячейк, в другой - учитываются
    timetables_min = dict.fromkeys(group_names, [])
    timetables_max = dict.fromkeys(group_names, [])
    for i in range(0, num_of_groups):
        timetables_min[group_names[i]] = get_timetable(worksheet, i, max=False)
        timetables_max[group_names[i]] = get_timetable(worksheet, i, max=True)

    # Новая табличка, правильно (надеюсь) отражающая расписание каждой группы
    shift_tab = TIMES[shift - 1]
    timetable = mix_tables(group_names, timetables_min, timetables_max, shift_tab)

    return timetable


# Расписание одной группы
def get_timetable(worksheet, num, max=False):
    q = num + 1
    # получение элемента K в столбце Q

    matrix = []

    start_column = 2 + (q - 1) * 4
    end_column = 2 + q * 4

    start_row = start_pos
    end_row = 132 - 14 + start_pos

    for i in range(start_row, end_row):
        line = []
        for j in range(start_column, end_column):
            if max:
                value = fix_str(unmerged_value(i, j, worksheet))
            else:
                value = fix_str(worksheet.cell_value(i, j))
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
def mix_tables(group_names, tb_min, tb_max, shift_tab):
    schedule = dict.fromkeys(group_names)

    for key in group_names:
        group_table_min = tb_min[key]
        group_table_max = tb_max[key]

        group_schedule = dict.fromkeys(DAYS)

        tb_len = len(group_table_min)

        for i in range(0, tb_len):
            day_min = group_table_min[i]
            day_max = group_table_max[i]

            day = dict.fromkeys(shift_tab)

            day_len = len(day_min)
            for j in range(0, day_len):

                lesson_min = day_min[j]
                lesson_max = day_max[j]

                lesson = []

                lesson_min_top = []
                lesson_min_top.append(lesson_min[0])
                lesson_min_top.append(lesson_min[1])

                lesson_min_bottom = []
                lesson_min_bottom.append(lesson_min[2])
                lesson_min_bottom.append(lesson_min[3])

                if lesson_min == [['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_']]\
                        or lesson_min_top == [['_', '_', '_', '_'], ['_', '_', '_', '_']]\
                        or lesson_min_bottom == [['_', '_', '_', '_'], ['_', '_', '_', '_']]:
                    lsn = copy.copy(lesson_max)
                    lesson = lsn
                    #lesson = copy.copy(lesson_max)
                else:
                    lesson = copy.copy(lesson_min)

                info = process_sector(lesson)

                day[shift_tab[j]] = info
            group_schedule[DAYS[i]] = day
        schedule[key] = group_schedule

    print(schedule)

    return schedule


# -------------------------------------------------------
# ПОЛУЧЕНИЕ ВСПОМОГАТЕЛЬНЫХ СВЕДЕНИЙ ИЗ ТАБЛИЦЫ

# Поиск точки отсчёта
def find_start(worksheet):
    for i in range(0, 20):
        if worksheet.cell_value(i, 0) == 'Дни':
            return i + 5


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


# Оформление строчки о конкретной паре на основе бинарного шаблона
def process_sector(sector):
    info = ""
    type = binary_sector(sector)
    info = "Ошибка!"

    #print_sector(sector)

    if type == None:
        pass

    elif type == [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]:
        if sector[0][0] == sector[2][0]:
            info = "  • {}".format(sector[0][0])
        else:
            info_1 = "  * {}".format(sector[0][0])
            info_2 = "  * {}".format(sector[2][0])
            info = info_1 + "\n" + info_2

    elif type == [[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]:
        info = "  * {}, {}".format(sector[0][0], sector[2][0])

        info = info.replace("2 нед.", "\n  * 2 нед.")

    elif type == [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1]]:
        info = "  * {},{}".format(sector[2][0], sector[3][0])


    elif type == [[1, 0, 1, 0], [1, 0, 1, 0], [1, 1, 1, 1], [1, 0, 1, 0]] \
        or type == [[1, 0, 1, 0], [0, 0, 1, 0], [1, 1, 1, 1], [1, 0, 1, 0]]\
        or type == [[1, 0, 1, 0], [1, 0, 1, 0], [1, 1, 1, 0], [1, 0, 1, 0]]\
        or type == [[1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 1], [1, 0, 1, 0]]:
        info_1 = "1-я подгруппа:\n  *  {} {}, {} {}, {}".format(sector[0][0], sector[1][0],
                                                                sector[2][0], sector[2][1], sector[3][0])
        info_2 = "2-я подгруппа:\n  *  {} {}, {} {}, {}".format(sector[0][2], sector[1][2],
                                                                sector[2][2], sector[2][3], sector[3][2])
        info = info_1 + "\n" + info_2

    elif type == [[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]:
        info = "  * {}, {}".format(sector[0][0], sector[1][0])

    elif type == [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]:
        info_1 = "  * {}, {}".format(sector[0][0], sector[1][0])
        info_2 = "  * {}, {}".format(sector[2][0], sector[3][0])

        info = info_1 + "\n" + info_2

    elif type == [[1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0]]:
        info = "1-я подгруппа:\n  *  {} {}, {} {}, {}".format(sector[0][0], sector[1][0],
                                                                sector[2][0], sector[2][1], sector[3][0])

    elif type == [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 1, 0]]:
        info = "2-я подгруппа:\n  *  {} {}, {} {}, {}".format(sector[0][2], sector[1][2],
                                                              sector[2][2], sector[2][3], sector[3][2])

    elif type == [[1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]]:
        info = "  * {}{} \n{}, {}\n{}, {}".format(sector[0][0], sector[1][0], sector[2][0], sector[2][1], sector[3][0], sector[3][1])

    elif type == [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 0, 0, 0]]:
        info = "  * {}, {}".format(sector[0][0], sector[3][0])

    elif type == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
        info = "<Пусто>"

    else:
        #info = "Ошибка! Неизвестный шаблон"
        info = "(!)    "
        '''for line in sector:
            for txt in line:
                info += txt + " "'''
        for line in sector:
            for i in range(0, 2):
                info += line[i] + " "
        for line in sector:
            for i in range(0, 2):
                info += line[i+2] + " "

        #info += "\n" + str(type)

    info = fix_info(info)

    return info + "\n" + str(type)


# Получение списка групп (ключей для словаря)
def get_group_names(worksheet):
    groups = []
    x = 2
    y = start_pos - 3


    while worksheet.cell_value(y, x) != '':
        groups.append(unmerged_value(y, x, worksheet))
        x += 4

    n_groups = []
    for item in groups:
        n_groups.append(str(item)[:-2])

    groups = n_groups
    return groups


# Определение смены, в которую учится факультет (ключи для словаря)
def what_shift(worksheet):
    global shift
    if worksheet.cell_value(14, 1) == "8.00- 9.35":
        shift = 1
    else:
        shift = 2

    return shift


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


# Удаление лишних '_'
def fix_info(info):
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

    return info


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
    with codecs.open('schedule.json', 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=3)

    print("Расписание сохранено.")


# -------------------------------------------------------


if __name__ == '__main__':
    schedule = parce_workbook("2.xls")
    save_json(schedule)

