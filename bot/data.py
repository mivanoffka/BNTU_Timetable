from aiogram.dispatcher import Dispatcher
from queue import Queue
from aiogram import Bot, types
from config import TOKEN

from bot.users import UsersDB
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode = "HTML")
dispatcher = Dispatcher(bot, storage=storage)

schedule = {}
users_and_groups = {}
waiting_for_group_num = []
waiting_for_sending_report = []
recently_sended_report = []

recent_users = []
interactions_count = {"today": 0, "tomorrow": 0, "weekdays": 0, "week": 0, "settings": 0, "mivanoffka": 0, "help": 0,
                      "start": 0, "cancel": 0}

is_updating = False
exit_event = False

users_db = None
global_animations = False


def increment(action, id):
    if action in interactions_count.keys():
        if interactions_count[action] < 9999999:
            interactions_count[action] += 1

    if id not in recent_users:
        recent_users.append(id)
