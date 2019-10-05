from .models import Run


def add_run(username, start_time):
    return Run.add_one(username, start_time)
