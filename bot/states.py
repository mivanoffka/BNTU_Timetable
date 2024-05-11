from aiogram2.dispatcher.filters.state import StatesGroup, State


class GroupSettingState(StatesGroup):
    awaiting = State()


class ReportingState(StatesGroup):
    awaiting = State()