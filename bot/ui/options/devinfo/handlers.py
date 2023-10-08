from pathlib import Path

import bot.commands.days
import config
from config import BASE_DIR

from bot import data, timetable

from aiogram import types
from bot.commands import buttoned
from bot.data import dispatcher
from aiogram.dispatcher import filters

from bot.states import GroupSettingState, ReportingState
from aiogram.dispatcher import FSMContext
from bot.ui.home.keyboards import home_keyboard
from bot.ui.weekdays.keyboards import weekdays_keyboard
from bot.ui.options.keyboards import options_keyboard
from bot.ui.options.website.keyboards import website_keyboard
import time




