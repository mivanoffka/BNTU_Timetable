import data
import codecs
import json


bot = data.bot
dr = data.dp


def read_userlist():
    users_and_groups = {}

    with codecs.open('users.json', 'r', encoding='utf-8') as f:
        users_and_groups = json.load(f)

    print("Список пользователей открыт.\n")

    for user in users_and_groups:
        print("{} - {}".format(user, users_and_groups[user]))

    return users_and_groups


def save_userlist(users_and_groups):
    with codecs.open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_and_groups, f, ensure_ascii=False, indent=3)

    print("Список пользователей сохранён")