import asyncio
from singleton import Singleton


class Distributor(metaclass=Singleton):
    async def __timer_loop(self):
        pass

    def __init__(self):
        asyncio.get_event_loop().create_task(self.__timer_loop())
        pass
