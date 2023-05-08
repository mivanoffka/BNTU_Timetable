import copy
import random
import urllib.request
import config
import requests
from config import BASE_DIR
from pathlib import Path
from parsing import parser as p
import _thread
import time

html_flag = False
html_buffer = None
url_buffer = "a"

def get_hmtl_code(url: str):
    global html_buffer
    html_buffer = None

    global  url_buffer
    url_buffer = url
    start_time = time.time()
    print("Connecting to " + url)
    i = 0
    while (html_buffer is None) and (i < 4):
        print("Attempt {}".format(i))

        _thread.start_new_thread(html_loop, tuple())
        while html_buffer is None:
            current_time = time.time()

            if current_time - start_time > 4:
                break
        i += 1

    if html_buffer is None:
        print("Cannot connect!")
        raise "Cannot connect!"
    else:
        print("Connected succesfully!")
        url_buffer = None
        return copy.copy(html_buffer)

def html_loop():
    html = requests.get(url_buffer)

    global html_buffer
    html_buffer = html

    pass

def find_lines_with_urld_fitr():
    # Ищем на страничке фитра

    ref = 'https://bntu.by/faculties/fitr/pages/raspisanie-zanyatij-i-ekzamenov'
    html = get_hmtl_code(ref)
    html = html.text
    html = html.splitlines()

    ref_1 = ""
    ref_2 = ""
    ref_3 = ""
    ref_4 = ""

    key_1 = 'Расписание занятий студентов 4-го курса специальности <strong>1-40 01 01, 1-40 05 01</strong> дневной формы получения образования с <strong>26.01.2023 по 15.03.2023</strong>&nbsp;года</a></p>'
    key_2 = '<span style="font-weight: 400;">Расписание занятий&nbsp; студентов 3-го курсов специальности </span><b>1-40 01 01, 1-40 05 01</b> дневной формы получения образования с 09.02.2023 по 31.05.2023&nbsp;&nbsp;</a></p>'
    key_3 = '<span style="font-weight: 400;">Расписание занятий&nbsp; студентов 3 и 4-го курсов специальности </span><b>1-53 01 05</b>&nbsp;дневной формы получения образования с 09.02.2023 по 31.05.2023&nbsp;&nbsp;</a></p>'
    key_4 = '<span style="font-weight: 400;">Расписание занятий&nbsp; студентов 3 и 4-го курсов специальности </span><b>1-53 01 01, 1-53 01 06</b> дневной формы получения образования с 09.02.2023 по 31.05.2023&nbsp;&nbsp;</a></p>'

    for line in html:
        if key_1 in line:
            ref_1 = line
            break

    for line in html:
        if key_2 in line:
            ref_2 = line
            break

    for line in html:
        if key_3 in line:
            ref_3 = line
            break

    for line in html:
        if key_4 in line:
            ref_4 = line
            break

    return [ref_1, ref_2, ref_3, ref_4]


def find_lines_with_urls():
    result = []
    # Ищем на страничке общего расписания

    ref = 'https://bntu.by/raspisanie'
    html = get_hmtl_code(ref)
    html = html.text
    html = html.splitlines()

    ref_1 = ""
    ref_2 = ""

    key_1 = "Расписание занятий студентов 1 курса дневной формы получения образования 2022-2023 учебного года"
    key_2 = "Расписание занятий студентов 2 курса дневной формы получения образования 2022-2023 учебного года"

    for line in html:
        if key_1 in line:
            ref_1 = line
            break

    for line in html:
        if key_2 in line:
            ref_2 = line
            break

    result.append(ref_1)
    result.append(ref_2)


    return result


def get_url_from_line(stroke: str):
    start = stroke.find("https")
    end = stroke.find("download")
    end = end + len("download")

    return stroke[start:end]


def get_url_from_line_fitr(stroke: str):
    start = stroke.find("https")
    end = stroke.find(".xls")
    end = end + len(".xls")

    return stroke[start:end]



async def download_and_parse():

    download_result = False
    try:
        urls = find_lines_with_urls()

        ref_1 = get_url_from_line(urls[0])
        ref_2 = get_url_from_line(urls[1])

        print(ref_1)
        print(ref_2)

        print(ref_1)
        destination = Path(BASE_DIR / "parsing/sheets/1kurs.xls")
        urllib.request.urlretrieve(ref_1, destination)
        print("0K")

        print(ref_2)
        destination = Path(BASE_DIR / "parsing/sheets/2kurs.xls")
        urllib.request.urlretrieve(ref_2, destination)
        print("0K")

        urls = find_lines_with_urld_fitr()
        ref_1 = get_url_from_line_fitr(urls[0])
        ref_2 = get_url_from_line_fitr(urls[1])
        ref_3 = get_url_from_line_fitr(urls[2])
        ref_4 = get_url_from_line_fitr(urls[3])

        print(ref_1)
        destination = Path(BASE_DIR / "parsing/sheets/4kurs_fitr.xls")
        urllib.request.urlretrieve(ref_1, destination)
        print("0K")

        print(ref_2)
        destination = Path(BASE_DIR / "parsing/sheets/3kurs_fitr.xls")
        urllib.request.urlretrieve(ref_2, destination)
        print("0K")

        print(ref_3)
        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_1.xls")
        urllib.request.urlretrieve(ref_3, destination)
        print("0K")

        print(ref_4)
        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_2.xls")
        urllib.request.urlretrieve(ref_4, destination)
        print("0K")

        print("Books are downloaded.")
        download_result = True

    except:
        print("Cannot download the books.")
        raise

    if download_result:
        try:
            p.main()
        except:
            print("An exception occured while parsing the sheets.")
            raise


        