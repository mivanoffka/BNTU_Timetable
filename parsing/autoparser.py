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


file_index = 0

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
    ref = 'https://bntu.by/faculties/fitr/pages/raspisanie-zanyatij-i-ekzamenov'

    html = requests.get(ref, verify=False)
    html = html.text

    html = html.splitlines()

    keys = ('Расписание учебных занятий студентов 3 и 4-го курсов специальности <strong>1-40 01 01</strong>',
            '>Расписание учебных занятий студентов 3 и 4-го курсов специальности <strong>1-53 01 01 и 1-53 01 06</strong>',
            'Расписание учебных занятий студентов 3 и 4-го курсов специальности <strong>1-53 01 05</strong>')
    urls = []

    for key in keys:
        for line in html:
            if key in line:
                urls.append(line)
                break

    logging.info("\n\n\n")
    logging.info(urls)
    logging.info("\n\n\n")

    return urls


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

    logging.info(excel_links)

    return excel_links[file_index][0]


def download_and_parse():
    download_result = False
    try:
        # ref_1 = get_link_for_cource(1)
        # ref_2 = get_link_for_cource(2)
        #
        # logging.info(ref_1)
        # logging.info(ref_2)
        #
        # destination = Path(BASE_DIR / "parsing/sheets/1kurs.xls")
        # download_unsafe(ref_1, destination)
        #
        # destination = Path(BASE_DIR / "parsing/sheets/2kurs.xls")
        # download_unsafe(ref_2, destination)

        urls = find_lines_with_urld_fitr()


        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_1.xls")
        download_unsafe(get_url_from_line_fitr(urls[0]), destination)

        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_2.xls")
        download_unsafe(get_url_from_line_fitr(urls[1]), destination)

        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_3.xls")
        download_unsafe(get_url_from_line_fitr(urls[2]), destination)

        # destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_1.xls")
        # download_unsafe(ref_2, destination)
        #
        # destination = Path(BASE_DIR/"parsing/sheets/34kurs_fitr_2.xls")
        # download_unsafe(ref_3, destination)
        #
        # destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_3.xls")
        # download_unsafe(ref_4, destination)

#        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_2.xls")
#        download(ref_4, destination)

        # ref_1 = "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1lnQTsDw2jFxx3087HYJtI_SLMwxnGOtX"
        # destination = Path(BASE_DIR/"parsing/sheets/3kurs_fmmp_1.xls")
        # download_unsafe(ref_1, destination)
        #
        # ref_2 = "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1FXrGeWdNaprjw59yDL8QkyCkQOiGHx6V"
        # destination = Path(BASE_DIR/"parsing/sheets/3kurs_fmmp_2.xls")
        # download_unsafe(ref_2, destination)
        #
        # ref_3 = "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1fWv8LFGiPmZROF0xin77xOnypHOIMsqP"
        # destination = Path(BASE_DIR/"parsing/sheets/3kurs_fmmp_3.xls")
        # download_unsafe(ref_3, destination)
        #
        # ref_4 = "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=14cLoLJAv5R8fF04yFGqfdqnzbKwE-prJ"
        # destination = Path(BASE_DIR/"parsing/sheets/3kurs_fmmp_4.xls")
        # download_unsafe(ref_4, destination)

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

        