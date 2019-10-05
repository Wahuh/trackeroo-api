from .models import Subscriptions


def add_subscription(username, subscription):
    return Subscriptions.add_one(username, subscription)
