from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    START = State()
    GROUP_INPUT = State()
    HOME = State()
    WEEKDAYS = State()
    DISTRIBUTION = State()
    OPTIONS = State()
    WEBSITE = State()
    HELP = State()
    TIMETABLE = State()
    DONATIONS = State()
    MESSAGE = State()
    REPORT_INPUT = State()
    ALTERNATIVE_MESSAGE = State()

