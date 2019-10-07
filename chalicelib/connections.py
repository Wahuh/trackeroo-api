from .models import Connection


def handle_connection(username, connection_id):
    Connection.add_connection_id(username, connection_id)


def handle_disconnection(username):
    Connection.remove_connection_id(username)
