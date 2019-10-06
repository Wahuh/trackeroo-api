from .models import Subscriptions


def add_first_subscription(username, subscription):
    return Subscriptions.add_one(username, subscription)


def update_subscriptions(username, subscription):
    return Subscriptions.update_one(username, subscription)
