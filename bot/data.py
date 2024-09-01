from aiogram.dispatcher import Dispatcher
from queue import Queue
from aiogram import Bot, types
from config import TOKEN
from bot.datacollector import DataCollector
from bot.users import UsersDB
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot, storage=storage)

datacollector: DataCollector

schedule = {}
users_and_groups = {}
waiting_for_group_num = []
waiting_for_sending_report = []
recently_sended_report = []

is_updating = False
exit_event = False

users_db = None
global_animations = False

mailing = True
