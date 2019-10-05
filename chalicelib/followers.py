from .models import Followers


def add_follower(username, follower):
    return Followers.add_one(username, follower)