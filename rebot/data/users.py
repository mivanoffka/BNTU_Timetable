from rebot.data.types.enums import GroupSettingResult, DistributionMode
from rebot.data.source import Source
from rebot.singleton import Singleton


class Users(metaclass=Singleton):
    __source: Source

    def __init__(self, source: Source):
        self.__source = source

    async def set_group(self, user_id: int, group_number: int) -> GroupSettingResult:
        return GroupSettingResult.SUCCESS

    async def get_group(self, user_id) -> int | None:
        return 0

    async def register(self, user_id: int):
        pass

    async def set_distribution_mode(self, user_id: int, distribution_mode: DistributionMode):
        pass

    async def is_admin(self, user_id: int) -> bool:
        return user_id in await self.get_admins()

    async def get_admins(self) -> tuple[int]:
        return (640091837,)


