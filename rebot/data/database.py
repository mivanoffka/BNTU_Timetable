import sqlalchemy
from rebot.singleton import Singleton
from sqlalchemy.orm import declarative_base
from sqlalchemy import Engine
from rebot.data.types import *


class Database(metaclass=Singleton):
    __engine: Engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:pass@localhost/bntu_timetable")
    __base: declarative_base = base

    def __init__(self):
        pass

    def get_users_list(self) -> list[User]:
        pass

    def get_user_by_telegram_id(self, telegram_id: int) -> User:
        pass

    def reset(self):
        base.metadata.drop_all(self.__engine)
        base.metadata.create_all(self.__engine)

database: Database = Database()


if __name__ == "__main__":
    print("Do you wish to reset the database? All data will be lost! (Y/n)")
    answer: str = input().lower()
    if answer == "y":
        Database().reset()

