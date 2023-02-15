import urllib.request
import config
import requests
from config import BASE_DIR
from pathlib import Path
from parsing import parser as p


def find_lines_with_urls():
    ref = 'https://bntu.by/raspisanie'
    html = requests.get(ref)
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

    return [ref_1, ref_2]


def get_url_from_line(stroke: str):
    start = stroke.find("https")
    end = stroke.find("download")
    end = end + len("download")

    return stroke[start:end]


def download_and_parse():

    download_result = False
    try:
        urls = find_lines_with_urls()
        ref_1 = get_url_from_line(urls[0])
        ref_2 = get_url_from_line(urls[1])

        destination = Path(BASE_DIR / "parsing/sheets/1kurs.xls")
        urllib.request.urlretrieve(ref_1, destination)

        destination = Path(BASE_DIR / "parsing/sheets/2kurs.xls")
        urllib.request.urlretrieve(ref_2, destination)

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


if __name__ == "__main__":
    download_and_parse()

        