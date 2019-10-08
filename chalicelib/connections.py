from .models import Connection


def get_connection_id(username):
    Connection.get_connection_id(username)


def handle_connection(username, connection_id):
    Connection.add_connection_id(username, connection_id)


def handle_disconnection(username):
    Connection.remove_connection_id(username)
