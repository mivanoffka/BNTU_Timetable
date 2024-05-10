import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Engine
from rebot.data.types import base


class Database:
    __engine: Engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:pass@localhost:3306/bntu_timetable")
    __base: declarative_base = base

    def __init__(self):
        pass

    def reset(self):
        base.metadata.drop_all(self.__engine)
        base.metadata.create_all(self.__engine)


if __name__ == "__main__":
    print("Do you wish to reset the database? All data will be lost! (Y/n)")
    answer: str = input().lower()
    if answer == "y":
        Database().reset()

