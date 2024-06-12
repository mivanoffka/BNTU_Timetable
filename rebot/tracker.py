import asyncio

from rebot.singleton import Singleton
from datetime import datetime
from rebot.data.types.enums import TrackerKeys
from rebot.data.users import Users
import enum


class Tracker(metaclass=Singleton):
    __statistics: dict[str, int] = {}
    __recent_users_id_list: list[int] = []
    __muted_users_id_list: list[int] = []
    __last_reset_time: datetime = None

    __users: Users = None

    def __init__(self, users: Users):
        self.__users = users
        self.reset_all_keys()

    async def start(self):
        await asyncio.get_event_loop().create_task(self.__unmuting_loop())

    def increment_key(self, key: str, user_id: int):
        if key in self.__statistics:
            self.__statistics[key] += 1
        else:
            self.__statistics[key] = 1

        if user_id not in self.__recent_users_id_list:
            self.__recent_users_id_list.append(user_id)

    def reset_all_keys(self):
        self.__statistics.clear()
        self.__last_reset_time = datetime.now()

    async def get_report(self) -> str:
        template: str = "Действия пользователей, начиная с {}:{}\n\nПроявили активность {} из {} пользователей"
        row_template: str = '\n   "{}": {} раз(а)'
        rows: str = "\n"

        for key in self.__statistics.keys():
            row = row_template.format(key, self.__statistics[key])
            rows += row

        rows += "\n"

        formatted_time = (str(self.__last_reset_time.date()) +
                          " " + str(self.__last_reset_time.time().hour) +
                          ":" + str(self.__last_reset_time.time().minute))

        active_users_count = len(self.__recent_users_id_list)
        all_users_count = len(await self.__users.get_all())

        report = template.format(formatted_time, rows, active_users_count, all_users_count)

        return report

    def is_user_muted(self, user_id: int) -> bool:
        return user_id in self.__muted_users_id_list

    def mute_user(self, user_id: int):
        if user_id not in self.__muted_users_id_list:
            self.__muted_users_id_list.append(user_id)

    def unmute_user(self, user_id: int):
        if user_id in self.__muted_users_id_list:
            self.__muted_users_id_list.remove(user_id)

    async def __unmuting_loop(self):
        while True:
            self.__muted_users_id_list.clear()
            await asyncio.sleep(300000)

    def track(self, key: str):
        def decorator(function):
            async def wrapper(*args, **kwargs):

                user_id: int = args[1]
                self.increment_key(key, user_id)

                return await function(*args, **kwargs)

            return wrapper

        return decorator


