from chalice import Chalice, Response, BadRequestError, ChaliceViewError
from chalicelib.auth import signup, authorizer, login
from chalicelib.runs import add_run, update_run
from chalicelib.users import add_user, get_users
from chalicelib.followers import add_first_follower, update_followers
from chalicelib.subscriptions import add_first_subscription, update_subscriptions

app = Chalice(app_name="trackeroo-api")


@app.route("/", cors=True, methods=["GET"], authorizer=authorizer)
def index():
    return {"hello": "world"}


@app.route("/signup", cors=True, methods=["POST"])
def post_signup():
    try:
        body = app.current_request.json_body
        password = body["password"]
        username = body["username"]
        jwt = signup(username=username, password=password)
        return Response(
            body={"message": "Registration success"},
            status_code=200,
            headers={"Authorization": jwt},
        )
    except KeyError:
        raise BadRequestError("Username or password is missing")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/login", cors=True, methods=["POST"])
def post_login():
    try:
        body = app.current_request.json_body
        password = body["password"]
        username = body["username"]
        jwt = login(username=username, password=password)
        return Response(
            body={"message": "Login success"},
            status_code=200,
            headers={"Authorization": jwt},
        )
    except KeyError:
        raise BadRequestError("Username or password is missing")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/runs", cors=True, methods=["POST"])
def post_run():
    try:
        body = app.current_request.json_body
        username = body["username"]
        start_time = body["start_time"]
        run = add_run(username, start_time)
        return Response(
            body={"run": run},
            status_code=201,
        )
    except KeyError:
        raise BadRequestError("Bad request body")
    except Exception as e:
        print(e, "<<<<< APP.PY ROUTE ERROR")
        raise ChaliceViewError(e)


@app.route("/runs", cors=True, methods=["PATCH"])
def patch_run():
    try:
        body = app.current_request.json_body
        run_id = body["run_id"]
        username = body["username"]
        finish_time = body["finish_time"]
        average_speed = body["average_speed"]
        altitude = body["altitude"]
        total_distance = body["total_distance"]
        time_taken = body["time_taken"]
        run = update_run(run_id, username, finish_time, average_speed, altitude, total_distance, time_taken)
        return Response(
            body={"run": run},
            status_code=200
        )
    except KeyError:
        raise BadRequestError("Bad request body")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users", cors=True, methods=["GET"])
def fetch_users():
    try:
        users = get_users()
        return Response(
            body={"users": users},
            status_code=200
        )
    except Exception as e:
        raise e


@app.route("/users", cors=True, methods=["POST"])
def post_user():
    try:
        body = app.current_request.json_body
        username = body["username"]
        first_name = body["first_name"]
        last_name = body["last_name"]
        age = body["age"]
        height = body["height"]
        weight = body["weight"]
        user = add_user(username, first_name, last_name, age, height, weight)
        return Response(
            body={"user": user},
            status_code=201
        )
    except KeyError:
        raise BadRequestError("Required key-value is missing")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/subscriptions", cors=True, methods=["PATCH"])
def patch_subscription(username):
    try:
        body = app.current_request.json_body
        subscription = body["subscription"]
        subscriptions = update_subscriptions(username, subscription)
        return {"subscriptions": subscriptions}
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/subscriptions", cors=True, methods=["POST"])
def post_subscription(username):
    try:
        body = app.current_request.json_body
        subscription = body["subscription"]
        subscription = add_first_subscription(username, subscription)
        return Response(
            body={"subscription": subscription},
            status_code=201,
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/followers", cors=True, methods=["POST"])
def follower(username):
    try:
        body = app.current_request.json_body
        follower = body["follower"]
        followers = add_first_follower(username, follower)
        return Response(
            body={"followers": followers},
            status_code=201,
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/followers", cors=True, methods=["PATCH"])
def follower(username):
    try:
        body = app.current_request.json_body
        follower = body["follower"]
        print(follower, username)
        followers = update_followers(username, follower)
        return Response(
            body={"followers": followers},
            status_code=200,
        )
    except Exception as e:
        raise ChaliceViewError(e)