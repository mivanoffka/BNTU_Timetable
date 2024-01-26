import xlrd
import copy
import json
from pathlib import Path
from config import BASE_DIR
from parsing.sheetmap import SheetMap
import openpyxl



parsing_mode = "default"

# СЛОВАРЬ ТЕРМИНОВ
#       Сектор - фрагмент экселевской таблицы (как правило матрица 4х4), представляющий одну пару
#       Timetable или table - раписание конкретной группы
#       Schedule - совокупность всех timetable'ов


def parce_workbook(out_schedule, filename, param="no"):
    workbook = None
    if ".xlsx" in str(filename):
        workbook = xlrd.open_workbook(filename)
    else:
        workbook = xlrd.open_workbook(filename, formatting_info=True)
    print("\n----------------------------------\nBook {}".format(filename))

    schedule = {}

    sheet_num = workbook.sheets()
    sheet_num = len(sheet_num)

    for s in range(0, sheet_num):
        #parce_worksheet(workbook, s, schedule)

        try:
            parce_worksheet(workbook, s, schedule)
        except:
            print("An error occured while parsing sheet #{}".format(s + 1))
            raise
            continue

    for key in schedule:
        out_schedule[key] = schedule[key]


def parce_worksheet(workbook, index, out_schedule):
    try:
        worksheet = workbook.sheet_by_index(index)

        mp = SheetMap(worksheet)
        local_schedule = mp.parse()
        for key in local_schedule:
            out_schedule[key] = local_schedule[key]

        print("Sheet #{} was successfully parsed".format(index + 1))
    except:
        print("An error occured while parsing sheet #{}".format(index + 1))


def binary_sector(sector):
    binary_sector = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    for i in range(0, 4):
        for j in range(0, 4):
            if sector[i][j] != '_':
                binary_sector[i][j] = 1
            else:
                binary_sector[i][j] = 0

    return binary_sector


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


def remove_spaces(txt):
    new_txt = ""
    for c in txt:
        if not c == " ":
            new_txt += c

    return new_txt


def save_json(schedule):
    with open(Path(BASE_DIR / 'datasource/schedule.json'), 'w', encoding='UTF-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=3)


def main():
    # schedule = {}
    #
    # f1 = Path(BASE_DIR/"parsing/sheets/1kurs.xls")
    #
    # f2 = Path(BASE_DIR/"parsing/sheets/2kurs.xls")
    #
    # parce_workbook(schedule, f1)
    # parce_workbook(schedule, f2)
    #
    # f1 = Path(BASE_DIR/"parsing/sheets/3kurs_fitr.xls")
    # f2 = Path(BASE_DIR/"parsing/sheets/4kurs_fitr.xls")
    # f3 = Path(BASE_DIR/"parsing/sheets/34kurs_fitr.xls")
    #
    # #f3 = Path(BASE_DIR/"parsing/sheets/34kurs_fitr_1.xls")
    # #f4 = Path(BASE_DIR/"parsing/sheets/34kurs_fitr_2.xls")
    #
    # parce_workbook(schedule, f1)
    #
    # parce_workbook(schedule, f2)
    #
    # parce_workbook(schedule, f3)
    #
    # #parce_workbook(schedule, f4)

    schedule = {}

    f1 = Path(BASE_DIR/"parsing/sheets/3kurs_fitr.xlsx")
    parce_workbook(schedule, f1)

    f2 = Path(BASE_DIR/"parsing/sheets/4kurs_fitr.xlsx")
    parce_workbook(schedule, f2)

    f3 = Path(BASE_DIR/"parsing/sheets/34kurs_fitr.xls")
    parce_workbook(schedule, f3)

    save_json(schedule)


if __name__ == '__main__':
    main()

