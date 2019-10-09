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


def update_user_distance(username, distance):
    return User.update_distance(username, distance)


def update_user_rewards(username):
    return User.update_rewards(username)
