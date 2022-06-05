
from db import conn
from sqlobject import *

class Notes(SQLObject):
    """
    Notes Model
    """
    _connection = conn
    title = StringCol(length=100, notNone=True)
    description = StringCol()
    user = ForeignKey('Users', cascade=True)
    created_at = DateTimeCol().now()

    def get_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user": self.user.username,
            "created_at": str(self.created_at)
        }

Notes.createTable(ifNotExists=True)