from aiogram2.dispatcher.filters.state import StatesGroup, State


class UiStates(StatesGroup):
    home = State()
    week = State()

