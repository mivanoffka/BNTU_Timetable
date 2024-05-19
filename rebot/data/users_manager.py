from rebot.data.database import database, Database
from rebot.singleton import Singleton
from sqlalchemy import select
from rebot.data.types import User


class UsersManager(metaclass=Singleton):
    __database: Database = database

    def __init__(self):
        pass

    def get_user_by_id(self, telegram_user_id) -> User:
        pass

    def register_user(self, telegram_user_id) -> User:
        pass

    def ban_user(self, telegram_user_id):
        pass

    def unban_user(self, telegram_user_id):
        pass


