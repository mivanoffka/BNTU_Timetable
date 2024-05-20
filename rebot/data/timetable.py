from rebot.data.types.enums import DistributionMode
from rebot.data.source import Source
from rebot.singleton import Singleton


class Timetable(metaclass=Singleton):
    __source: Source

    def __init__(self, source: Source):
        self.__source = source

    async def get_timetable_message_text(self, user_id: int, weekday_number: int,
                                         distribution_mode: DistributionMode | None = None) -> str:
        return "Пока что здесь ничего нет..."
