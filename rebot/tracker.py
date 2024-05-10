import asyncio

from singleton import Singleton
from datetime import datetime
from data.types import User


class Tracker(metaclass=Singleton):
    __statistics: dict[str, int] = {}
    __recent_users_list: list[User] = []
    __muted_users_list: list[User] = []
    __last_reset_time: datetime = None

    def __init__(self):
        asyncio.get_event_loop().create_task(self.__unmuting_loop())

    def increment_key(self, key: str):
        pass

    def reset_all_keys(self):
        pass

    def get_report(self) -> str:
        pass

    def is_user_muted(self, user: User) -> bool:
        pass

    def mute_user(self, user: User) -> bool:
        pass

    async def __unmuting_loop(self):
        pass

