from .models import Run


def add_run(username, start_time):
    return Run.add_one(username, start_time)


def update_run(**kwargs):
    run_id = kwargs["run_id"]
    username = kwargs["username"]
    finish_time = kwargs.get("finish_time")
    print(username, run_id, finish_time)
    if finish_time:
        return Run.update_finish_time(
            run_id=run_id, username=username, finish_time=finish_time
        )
    else:
        longitude = kwargs["longitude"]
        latitude = kwargs["latitude"]
        average_speed = kwargs["average_speed"]
        total_distance = kwargs["total_distance"]
        return Run.update_stats(
            username=username,
            run_id=run_id,
            longitude=longitude,
            latitude=latitude,
            average_speed=average_speed,
            total_distance=total_distance,
        )


def get_runs_by_subscriptions(subscriptions):
    return Run.get_runs_by_subscriptions(subscriptions)
