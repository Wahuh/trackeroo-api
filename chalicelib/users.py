from .models import User


def add_user(username, first_name, last_name, age, height, weight):
    return User.add_one(username, first_name, last_name, age, height, weight)