from .models import User, Followers, Connection


def add_user(username):
    return User.add_one(username)


def get_user(username):
    return User.get_user(username)


def get_all_followers_connection_ids(username):
    user = User.get_user(username)
    followers = user["followers"]
    connection_ids = []
    if followers:
        for follower in followers:
            connection_id = Connection.get_connection_id(follower)
            connection_ids.append(connection_id)
    return connection_ids


def get_users(start_username):
    return User.scan_users(start_username)


def add_follower(username, follower):
    return User.add_follower(username, follower)


def add_subscription(username, subscription):
    return User.add_subscription(username, subscription)
