import aiogram
from aiogram.dispatcher.filters.state import StatesGroup, State


class GroupSettingState(StatesGroup):
    awaiting = State()


class ReportingState(StatesGroup):
    awaiting = State()