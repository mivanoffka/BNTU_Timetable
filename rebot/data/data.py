from rebot.data.source import Source
from rebot.data.timetable import Timetable
from rebot.data.tracker.tracker import Tracker
from rebot.singleton import Singleton
from rebot.data.users import Users


class Data(metaclass=Singleton):
    __source = Source()
    __users: Users = Users(__source)
    __timetable: Timetable = Timetable(__source)
    __tracker: Tracker = Tracker()

    @property
    def users(self):
        return self.__users

    @property
    def timetable(self):
        return self.__timetable

    @property
    def tracker(self):
        return self.__tracker

    def __init__(self):
        pass



