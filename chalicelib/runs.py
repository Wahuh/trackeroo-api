from .models import Run


def add_run(username, start_time):
    return Run.add_one(username, start_time)


def update_run(username, run_id, finish_time, average_speed, total_distance, coordinates):
    return Run.update_one(username, run_id, finish_time, average_speed, total_distance, coordinates)


def get_runs_by_subscriptions(subscriptions):
    return Run.get_runs_by_subscriptions(subscriptions)


def get_users_runs(username):
    return Run.get_users_runs(username)

