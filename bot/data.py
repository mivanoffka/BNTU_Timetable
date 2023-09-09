from aiogram.dispatcher import Dispatcher
from queue import Queue
from aiogram import Bot, types
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

schedule = {}
users_and_groups = {}
waiting_for_group_num = []
waiting_for_sending_report = []
recently_sended_report = []

recent_users = []
interactions_count = {"today": 0, "tomorrow": 0, "weekdays": 0, "week": 0, "settings": 0, "mivanoffka": 0, "help": 0}

is_updating = False
exit_event = False
