from .db import connection

_table = connection.Table("users")


class User:
    @staticmethod
    def add_one(username):
        _table.put_item(Item={"username": username})
