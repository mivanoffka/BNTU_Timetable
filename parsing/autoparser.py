import copy
import os
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
import re


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
    if "/download" not in url:
        if "google" not in url and "static" not in url and "bntu" in url:
            url += "/download"
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


def find_lines_with_url_ef():
    ref = "https://bntu.by/faculties/ef/pages/raspisanie-zanyatij-dnevnoe-otdelenie"

    html = requests.get(ref, verify=False)
    html = html.text

    html = html.splitlines()

    keys = [">Скачать</a>", 'title="Скачать"']
    urls = []

    for key in keys:
        for line in html:
            if key in line:
                urls.append(line)
                break

    new_urls = []

    new_url_1 = urls[0]
    new_url_1 = new_url_1.replace(
        '<td style="width: 26.343%; height: 22px; text-align: center;"><strong><a href="',
        "",
    )
    new_url_1 = new_url_1.replace('">Скачать</a></strong></td>', "")
    new_urls.append(new_url_1)

    new_url_2 = urls[1]
    new_url_2 = new_url_2.replace(
        '<td style="width: 26.343%; height: 22px; text-align: center;"><strong><a href="',
        "",
    )
    new_url_2 = new_url_2.replace('" title="Скачать">Скачать</a></strong></td>', "")
    new_urls.append(new_url_2)

    return new_urls


def find_lines_with_urld_fitr():
    ref = "https://bntu.by/faculties/fitr/pages/raspisanie-zanyatij-i-ekzamenov"

    html = requests.get(ref, verify=False)
    html = html.text

    html = html.splitlines()

    keys = (
        "Расписание учебных занятий студентов 3-го курса специальности <strong>1-40 01 01</strong> дневной формы получения образования с 27 января по 17 мая 2024-2025 учебного года</span></a></p>",
        "Расписание учебных занятий студентов 3-го курса специальности <strong>1-40 05 01</strong> дневной формы получения образования с 27 января по 17 мая 2024-2025 учебного года</span></a></p>",
        "Расписание учебных занятий студентов 3 и 4-го курсов специальности <strong>1-53 01 01 и 1-53 01 06</strong> дневной формы получения образования&nbsp;</span></a></p>",
        "Расписание учебных занятий студентов 3 и 4-го курсов специальности <strong>1-53 01 05</strong> дневной формы получения образования с 10 февраля по 7 июня 2024-2025 учебного года</span></a></p>",
    )
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

    # html = get_html(ref)
    # html = html.decode("utf-8")
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
    res = requests.get(
        f"https://schedule.bntu.by:9443/api/schedule_files/?course={course_number}&format=json",
        verify=False,
    )

    if not res.text:
        return

    res_json = res.json()

    excel_links = [item["excel_files"] for item in res_json]

    logging.info(excel_links)

    return excel_links[file_index][0]


def clear_folder():
    folder_path = Path(BASE_DIR / "parsing/sheets")
    if not os.path.exists(folder_path):
        return

    for file_name in os.listdir(folder_path):
        try:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        except:
            ...


def download_and_parse():
    clear_folder()
    download_result = False
    try:
        ef = find_lines_with_url_ef()
        logging.info(ef[0])
        logging.info(ef[1])

        destination = Path(BASE_DIR / "parsing/sheets/ef_345_1.xls")
        download_unsafe(ef[0], destination)

        destination = Path(BASE_DIR / "parsing/sheets/ef_345_2.xls")
        download_unsafe(ef[1], destination)

        ref_1 = get_link_for_cource(1)
        ref_2 = get_link_for_cource(2)

        destination = Path(BASE_DIR / "parsing/sheets/1kurs.xls")
        download_unsafe(ref_1, destination)

        destination = Path(BASE_DIR / "parsing/sheets/2kurs.xls")
        download_unsafe(ref_2, destination)

        urls = find_lines_with_urld_fitr()

        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_1.xlsx")
        download_unsafe(get_url_from_line_fitr(urls[0]), destination)

        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_2.xlsx")
        download_unsafe(get_url_from_line_fitr(urls[1]), destination)

        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_3.xls")
        download_unsafe(get_url_from_line_fitr(urls[2]), destination)

        destination = Path(BASE_DIR / "parsing/sheets/34kurs_fitr_4.xls")
        download_unsafe(get_url_from_line_fitr(urls[3]), destination)

        download_unsafe(
            "https://drive.google.com/uc?export=download&id=1UwvtDysgPIVdNyNIDi-f_zkqASJrnZLz",
            Path(BASE_DIR / "parsing/sheets/3kurs_fmmp_1.xls"),
        )

        download_unsafe(
            "https://drive.google.com/uc?export=download&id=1RNrL10SO_0EOpOSPgipw2iqx3iCidcPC",
            Path(BASE_DIR / "parsing/sheets/3kurs_fmmp_2.xls"),
        )

        download_unsafe(
            "https://drive.google.com/uc?export=download&id=1OZblTd85WnWxi6KYHk9kx3aE4A-R5F2W",
            Path(BASE_DIR / "parsing/sheets/3kurs_fmmp_3.xls"),
        )

        download_unsafe(
            "https://drive.google.com/uc?export=download&id=1k3Ff4AZJP6PL3TH3ilEHrbav369n4WTj",
            Path(BASE_DIR / "parsing/sheets/4kurs_fmmp_1.xls"),
        )

        logging.info("Books are downloaded.")
        download_result = True

    except Exception as e:
        logging.info(f"Cannot download the books.\n {e}")
        download_result = False
        raise

    if download_result:
        try:
            p.main()
        except Exception as e:
            logging.info(f"An exception occured while parsing the sheets. \n\n{e}")
            raise


if __name__ == "__main__":
    download_and_parse()
