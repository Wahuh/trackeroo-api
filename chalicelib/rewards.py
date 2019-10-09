from .models import Rewards


def add_reward(challenge, reward):
    return Rewards.add_one(challenge, reward)
