from .models import Run


def add_run(username, start_time):
    return Run.add_one(username, start_time)


def get_users_runs(username):
    return Run.get_users_runs(username)


def update_run(**kwargs):
    run_id = kwargs["run_id"]
    username = kwargs["username"]
    finish_time = kwargs.get("finish_time")
    coordinates = kwargs.get("coordinates")

    average_speed = kwargs["average_speed"]
    total_distance = kwargs["total_distance"]

    print(username, run_id, finish_time)
    if finish_time:
        return Run.update_finish_time(
            username=username,
            run_id=run_id,
            average_speed=average_speed,
            total_distance=total_distance,
            coordinates=coordinates,
            finish_time=finish_time,
        )
    else:
        longitude = kwargs["longitude"]
        latitude = kwargs["latitude"]
        return Run.update_stats(
            username=username,
            run_id=run_id,
            longitude=longitude,
            latitude=latitude,
            average_speed=average_speed,
            total_distance=total_distance,
            coordinates=coordinates,
        )


def get_runs_by_subscriptions(subscriptions):
    return Run.get_runs_by_subscriptions(subscriptions)
