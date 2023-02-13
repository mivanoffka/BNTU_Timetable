from bot import data
import codecs
import json
import random

from pathlib import Path
from config import BASE_DIR

bot = data.bot
dr = data.dp


def read_userlist(dump=False):
    users_and_groups = {}

    with open(Path(BASE_DIR / "users.json"), 'r', encoding='UTF-8') as f:
        users_and_groups = json.load(f)

    for user in users_and_groups:
        print("{} - {}".format(user, users_and_groups[user]))

    if not users_and_groups:
        with open(Path(BASE_DIR / "users_dump.json"), 'r', encoding='UTF-8') as f:
            users_and_groups = json.load(f)

        for user in users_and_groups:
            print("{} - {}".format(user, users_and_groups[user]))

    return users_and_groups


def save_userlist(users_and_groups):
    with open(Path(BASE_DIR / 'users.json'), 'w', encoding='UTF-8') as f:
        json.dump(users_and_groups, f, ensure_ascii=False, indent=3)

    #print("Список пользователей сохранён")


async def save_copy(users_and_groups):
    rand = random.randint(0, 15)
    if rand == 14:
        with open(Path(BASE_DIR / 'users_dump.json'), 'w', encoding='UTF-8') as f:
            json.dump(users_and_groups, f, ensure_ascii=False, indent=3)
        print("DUMP SAVED")
