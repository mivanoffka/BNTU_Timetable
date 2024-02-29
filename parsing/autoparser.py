import copy
import random
import urllib.request
from urllib.request import urlopen
import config
import requests
from config import BASE_DIR
from pathlib import Path
from parsing import parser as p
import _thread
import time
import logging

def get_html(url):
    counter = 0
    f = None
    max_attemps = 16

    logging.info("Connecting to {}".format(url))
    while counter < max_attemps and f is None:
        logging.info("Attempt {}...".format(counter))
        try:
            f = urllib.request.urlopen(url, timeout=2).read()
            counter = max_attemps + 1
        except:
            f = None
            counter += 1

    if f is not None:
        logging.info("Connected succesfully!")
        return f
    else:
        logging.info("Cannot connect!")
        return None


def download_unsafe(url, dest):
    response = requests.get(url, verify=False)
    open(dest, "wb").write(response.content)



def download(url, dest):
    counter = 0
    f = None
    max_attemps = 16

    while counter < max_attemps and f is None:
        logging.info("Attempt {}...".format(counter))
        try:
            f = urllib.request.urlopen(url, timeout=2).read()
            counter = max_attemps + 1
        except:
            f = None
            counter += 1

    if f is not None:
        file = open(dest, "wb")
        file.write(f)
        logging.info("Succesfully downloaded!")
    else:
        logging.info("Cannot download!")


def find_lines_with_urld_fitr():
    # Ищем на страничке фитра

    ref = 'https://bntu.by/faculties/fitr/pages/raspisanie-zanyatij-i-ekzamenov'
    #html = requests.get(ref)
    #html = get_html(ref).decode("utf-8")
    #html = html.text

    html = requests.get(ref, verify=False)
    html = html.text
    html = html.splitlines()

    ref_1 = ""
    ref_2 = ""
    ref_3 = ""

    '''
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
            '''

    key_1 = "Расписание занятий студентов 3-го курса специальности <strong>1-40 01 01</strong>"
    key_2 = "Расписание занятий&nbsp; студентов 4-го курса специальности"
    key_3 = "Расписание занятий студентов 3-го курса <strong>(с 26 января по 17 мая)</strong> и 4-го курса"

    prev = ""

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

    arr = [ref_1, ref_2, ref_3]

    logging.info("\n\n\n")
    logging.info(arr)
    logging.info("\n\n\n")

    return arr


def find_lines_with_urls():
    result = []
    # Ищем на страничке общего расписания

    ref = "https://bntu.by/raspisanie"
    html = requests.get(ref, verify=False)

    #html = get_html(ref)
    #html = html.decode("utf-8")
    html = html.text
    html = html.splitlines()

    ref_1 = ""
    ref_2 = ""

    key_1 = "Расписание занятий студентов 1 курса дневной формы получения образования 2023-2024 учебного года"
    key_2 = "Расписание занятий студентов 2 курса дневной формы получения образования 2023-2024 учебного года"

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
    is_x = False
    if ".xlsx" in stroke:
        is_x = True
        stroke = stroke.replace(".xlsx", ".xls")

    start = stroke.find("https")
    end = stroke.find(".xls")
    end = end + len(".xls")

    result = stroke[start:end]
    if is_x:
        result = result + "x"

    return result


def get_link_for_cource(course_number):
    res = requests.get(f'https://schedule.bntu.by:9443/api/schedule_files/?course={course_number}&format=json', verify=False)

    if not res.text:
        return

    res_json = res.json()

    excel_links = [item['excel_files'] for item in res_json]

    return excel_links[0][0]


def download_and_parse():
    download_result = False
    try:
        # urls = find_lines_with_urls()
        #
        # ref_1 = get_url_from_line(urls[0])
        # ref_2 = get_url_from_line(urls[1])

        ref_1 = get_link_for_cource(1)
        ref_2 = get_link_for_cource(2)

        logging.info(ref_1)
        logging.info(ref_2)

        destination = Path(BASE_DIR / "parsing/sheets/1kurs.xls")
        download_unsafe(ref_1, destination)

        destination = Path(BASE_DIR / "parsing/sheets/2kurs.xls")
        download_unsafe(ref_2, destination)

        urls = find_lines_with_urld_fitr()
        ref_1 = get_url_from_line_fitr(urls[0])
        ref_2 = get_url_from_line_fitr(urls[1])
        ref_3 = get_url_from_line_fitr(urls[2])

        destination = Path(BASE_DIR / "parsing/sheets/3kurs_fitr.xlsx")
        download_unsafe(ref_1, destination)

        destination = Path(BASE_DIR / "parsing/sheets/4kurs_fitr.xlsx")
        download_unsafe(ref_2, destination)

        destination = Path(BASE_DIR/"parsing/sheets/34kurs_fitr.xls")
        download_unsafe(ref_3, destination)

#        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_2.xls")
#        download(ref_4, destination)

        logging.info("Books are downloaded.")
        download_result = True

    except:
        logging.info("Cannot download the books.")
        download_result = False
        raise

    if download_result:
        try:
            p.main()
        except:
            logging.info("An exception occured while parsing the sheets.")
            raise

        