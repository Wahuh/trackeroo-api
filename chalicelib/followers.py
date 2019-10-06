from .models import Followers


def add_first_follower(username, follower):
    return Followers.add_one(username, follower)


def update_followers(username, follower):
    return Followers.update_one(username, follower)