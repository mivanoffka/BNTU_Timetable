from config import BASE_DIR, TABLE_NAME
from pathlib import Path

import sqlite3


class UserInfo:
    id: str
    group: str
    name: str
    message: str
    time: str

    def __init__(self, id, group, name, message, time):
        self.id = id
        self.group = group
        self.name = name
        self.message = message

        self.time = time

    def __str__(self):
        return "{}-{}-{}-{}-{}".format(self.id, self.group, self.name, self.message, self.time)


class UsersDB:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor
    times: tuple

    def __init__(self):
        self.connection = sqlite3.connect(BASE_DIR / "bot/databases/users.db")
        self.cursor = self.connection.cursor()

        self.times = self.execute("SELECT time FROM times")

    def insert(self, uid, group, name):
        if name is None:
            name = "NULL"

        exists = self.execute("SELECT EXISTS(SELECT * FROM {} where id = {})".format(TABLE_NAME, uid))[0][0]

        if not exists:
            self.execute("INSERT INTO {} (id, ugroup, uname) VALUES ('{}', '{}', '{}')"
                         .format(TABLE_NAME, uid, group, name))
        else:
            self.execute("UPDATE {} SET ugroup = '{}' WHERE id = '{}'".format(TABLE_NAME, group, uid))
            pass

    def update_message(self, uid, message):
        exists = self.execute("SELECT EXISTS(SELECT * FROM {} where id = {})".format(TABLE_NAME, uid))[0][0]

        if not exists:
            raise "DB ERROR"
        else:
            self.execute("UPDATE {} SET display_id = '{}' WHERE id = '{}'".format(TABLE_NAME, message, uid))
            pass

    def update_time(self, uid, time):
        exists = self.execute("SELECT EXISTS(SELECT * FROM {} where id = {})".format(TABLE_NAME, uid))[0][0]

        if not exists:
            raise "DB ERROR"

        else:
            if time == "morning":
                time = 1
                pass
            elif time == "evening":
                time = 2
            else:
                time = "NULL"
            self.execute("UPDATE {} SET mailing_time = {} WHERE id = '{}'".format(TABLE_NAME, time, uid))
            pass

    def delete(self, uid):
        self.execute("DELETE FROM {} WHERE id='{}'".format(TABLE_NAME, uid))

    def execute(self, query_text: str):
        result = None

        while "'NULL'" in query_text:
            query_text = query_text.replace("'NULL'", "NULL")

        try:
            result = self.cursor.execute(query_text)
            self.connection.commit()
        except:
            pass

        return self.cursor.fetchall()

    def get_group(self, uid: str):
        result = None
        try:
            query = "SELECT ugroup FROM {} WHERE id = {}".format(TABLE_NAME, uid)
            result = self.execute(query)[0][0]
        except:
            pass

        return result

    def get_info(self, uid: str):
        query_result = None
        info = None
        try:
            query = "SELECT * FROM {} WHERE id = {}".format(TABLE_NAME, uid)
            query_result = self.execute(query)[0]
            time_index = query_result[4]
            query = "SELECT time FROM times WHERE id = {}".format(time_index)
            t = None
            try:
                t = self.execute(query)[0][0]
            except:
                pass

            info = UserInfo(query_result[0], query_result[1], query_result[2], query_result[3], t)
        except:
            pass

        return info

    def get_list(self):
        result = None
        lst = []

        try:
            query = "SELECT * FROM {}".format(TABLE_NAME)
            result = self.execute(query)
        except:
            pass

        for obj in result:
            uinfo = UserInfo(obj[0], obj[1], obj[2], obj[3], obj[4])
            lst.append(uinfo)

        return lst

    def in_list(self, id: str):
        lst = self.get_list()
        result = False
        for uinfo in lst:
            if uinfo.id == id:
                result = True
                break

        return result

    def is_authorized(self, id: str):
        uinfo = self.get_info(id)
        if uinfo is not None:
            if uinfo.group == "NULL" or uinfo.group is None:
                return False
            else:
                return True
        else:
            return False

    # def __del__(self):
    #     self.cursor.close()
    #     self.connection.close()






