from aiogram.dispatcher.filters.state import StatesGroup, State


class UiStates(StatesGroup):
    home = State()
    week = State()

