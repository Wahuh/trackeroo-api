from .models import User


def add_user(username):
    return User.add_one(username)


def get_user(username):
    return User.get_user(username)


def get_users(start_username):
    return User.scan_users(start_username)


def add_follower(username, follower):
    return User.add_follower(username, follower)


def add_subscription(username, subscription):
    return User.add_subscription(username, subscription)
