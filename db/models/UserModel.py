from sqlobject import *
from db import conn

class Users(SQLObject):
    """
    User Model
    """
    _connection = conn
    username = StringCol(length=18, notNone=True, unique=True)
    password = StringCol()

    def get_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }

Users.createTable(ifNotExists=True)