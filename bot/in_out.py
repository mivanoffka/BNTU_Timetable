import copy
import time

from bot import data
import json
import schedule

from pathlib import Path
from config import BASE_DIR

bot = data.bot
dr = data.dp


def read_userlist(filename="datasource/users.json"):
    users_and_groups = {}

    try:
        with open(Path(BASE_DIR / filename), 'r', encoding='UTF-8') as f:
            users_and_groups = json.load(f)

        save_userlist(users_and_groups, "datasource/dump.json")

        return users_and_groups
    except:
        return {}


def save_userlist(users_and_groups, filename="datasource/users.json"):
    with open(Path(BASE_DIR / filename), 'w', encoding='UTF-8') as f:
        json.dump(users_and_groups, f, ensure_ascii=False, indent=3)


def autosave():
    try:
        uag = copy.copy(data.users_and_groups)
        save_userlist(uag)
        print("Autosaving completed.")
    except:
        print("An error occured during autosaving...")


def clear_recent_reports():
    data.recently_sended_report.clear()


def launch_autosaving():
    schedule.every(15).minutes.do(autosave)
    schedule.every(5).minutes.do(clear_recent_reports)

    while not data.exit_event:
        schedule.run_pending()
        time.sleep(1)

