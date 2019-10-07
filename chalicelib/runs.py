from .models import Run


def add_run(username, start_time):
    return Run.add_one(username, start_time)


def update_run(username, run_id, finish_time, average_speed, total_distance):
    return Run.update_one(username, run_id, finish_time, average_speed, total_distance)


def get_runs_by_subscriptions(subscriptions):
    return Run.get_runs_by_subscriptions(subscriptions)
