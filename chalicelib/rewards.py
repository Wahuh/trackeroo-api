from .models import Rewards


def add_reward(challenge, reward):
    return Rewards.add_one(challenge, reward)


def update_reward(reward_id, winner):
    return Rewards.update_reward(reward_id, winner)


def get_rewards(completed):
    return Rewards.get_rewards(completed)