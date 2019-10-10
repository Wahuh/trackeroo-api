from .models import User, Followers, Connection


def add_user(username):
    return User.add_one(username)


def get_user(username):
    return User.get_user(username)


def update_user_rewards(username):
    return User.update_rewards(username)


def update_user_distance(username, distance):
    return User.update_distance(username, distance)
    # return User.update_distance(username, distance)


def get_all_followers_connection_ids(username):
    user = User.get_user(username)
    followers = user["followers"]
    print("followers", followers)
    connection_ids = []
    if followers:
        for follower in followers:
            connection_id = Connection.get_connection_id(follower)
            print("conn_id", connection_id)
            connection_ids.append(connection_id)
    return connection_ids


def get_users(start_username):
    return User.scan_users(start_username)


def add_follower(username, follower):
    return User.add_follower(username, follower)


def add_subscription(username, subscription):
    return User.add_subscription(username, subscription)
