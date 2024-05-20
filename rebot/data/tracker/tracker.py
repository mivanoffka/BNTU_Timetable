import asyncio

from rebot.singleton import Singleton
from datetime import datetime
from rebot.data.types.enums import TrackerKeys


class Tracker(metaclass=Singleton):
    __statistics: dict[TrackerKeys, int] = {}
    __recent_users_id_list: list[int] = []
    __muted_users_id_list: list[int] = []
    __last_reset_time: datetime = None

    def __init__(self):
        #asyncio.get_event_loop().create_task(self.__unmuting_loop())
        ...

    def increment_key(self, key: TrackerKeys, user_id: int):
        pass

    def reset_all_keys(self):
        pass

    def get_report(self) -> str:
        pass

    def is_user_muted(self, user_id: int) -> bool:
        pass

    def mute_user(self, user_id: int) -> bool:
        pass

    async def __unmuting_loop(self):
        pass