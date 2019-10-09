from boto3.session import Session
from chalice import (
    Chalice,
    Response,
    BadRequestError,
    ChaliceViewError,
    WebsocketDisconnectedError,
)
from chalicelib.auth import signup, authorizer, login
from chalicelib.runs import add_run, update_run, get_runs_by_subscriptions, get_users_runs
from chalicelib.users import add_user, get_users, add_follower, add_subscription, get_user, update_user_distance, update_user_rewards
from chalicelib.rewards import add_reward, update_reward, get_rewards
import json
from chalicelib.models import Connection

app = Chalice(app_name="trackeroo-api")
app.experimental_feature_flags.update(["WEBSOCKETS"])
app.websocket_api.session = Session()


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
        raise ChaliceViewError(e)


@app.route("/runs", cors=True, methods=["PATCH"])
def patch_run():
    try:
        body = app.current_request.json_body
        run_id = body["run_id"]
        username = body["username"]
        finish_time = body["finish_time"]
        average_speed = body["average_speed"]
        total_distance = body["total_distance"]
        coordinates = body["coordinates"]
        update_run(run_id, username, finish_time, average_speed, total_distance, coordinates)
        return Response(
            body={},
            status_code=204
        )
    except KeyError:
        raise BadRequestError("Bad request body")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/runs", methods=["GET"])
def get_runs():
    try:
        query = app.current_request.query_params
        if "username" in query:
            username = query["username"]
            user = get_user(username)
            print(user)
            runs = get_runs_by_subscriptions(user["subscriptions"])
            return Response(
                body={"runs": runs},
                status_code=200
            )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/runs", methods=["GET"])
def get_runs_by_username(username):
    try:
        runs = get_users_runs(username)
        return Response(
            body={"runs": runs},
            status_code=200
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users", cors=True, methods=["GET"])
def fetch_users():
    try:
        query = app.current_request.query_params
        print(query, )
        start_username = None
        if query is None:
            users = get_users(None)
        elif "start_username" in query:
            start_username = query["start_username"]
            users = get_users(start_username)
        print(users)
        return Response(
            body=users,
            status_code=200
        )
    except Exception as e:
        raise e


@app.route("/users", cors=True, methods=["POST"])
def post_user():
    try:
        body = app.current_request.json_body
        username = body["username"]
        user = add_user(username)
        return Response(
            body={"user": user},
            status_code=201
        )
    except KeyError:
        raise BadRequestError("username must be valid")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route('/users/{username}', cors=True, methods=["PATCH"])
def update_user(username):
    try:
        body = app.current_request.json_body
        distance = body["distance"]
        user = update_user_distance(username, distance)
        return Response(
            body={'user': user["Attributes"]},
            status_code=200
        )
    except Exception as e:
        raise e


@app.route("/users/{username}/followers", cors=True, methods=["PATCH"])
def patch_user_followers(username):
    try:
        body = app.current_request.json_body
        follower = body["follower"]
        add_follower(username, follower)
        return Response(
            body={},
            status_code=204
        )
    except KeyError:
        raise BadRequestError("follower must be valid")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/subscriptions", cors=True, methods=["PATCH"])
def patch_subscription(username):
    try:
        body = app.current_request.json_body
        subscription = body["subscription"]
        add_subscription(username, subscription)
        return Response(
            body={},
            status_code=204
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/rewards", cors=True, methods=["POST"])
def post_reward():
    try:
        body = app.current_request.json_body
        challenge = body["challenge"]
        reward = body["reward"]
        new_reward = add_reward(challenge, reward)
        return Response(
            body={"reward": new_reward},
            status_code=201
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/rewards", cors=True, methods=["PATCH"])
def patch_reward():
    try:
        body = app.current_request.json_body
        reward_id = body["reward_id"]
        winner = body["winner"]
        update_reward(reward_id, winner)
        return Response(
            body={},
            status_code=204
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/rewards", cors=True, methods=["GET"])
def fetch_rewards():
    try:
        query = app.current_request.query_params
        completed = query["completed"]
        rewards = get_rewards(completed)
        return Response(
            body={"rewards": rewards},
            status_code=200
        )
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/rewards/{username}", cors=True, methods=["PATCH"])
def update_users_rewards(username):
    try:
        update_user_rewards(username)
        return Response(
            body={},
            status_code=204
        )
    except Exception as e:
        raise ChaliceViewError(e)


# @app.route("/users/{username}/subscriptions", cors=True, methods=["POST"])
# def post_subscription(username):
#     try:
#         body = app.current_request.json_body
#         subscription = body["subscription"]
#         subscription = add_first_subscription(username, subscription)
#         return Response(
#             body={"subscription": subscription},
#             status_code=201,
#         )
#     except Exception as e:
#         raise ChaliceViewError(e)


# @app.route("/users/{username}/followers", cors=True, methods=["POST"])
# def follower(username):
#     try:
#         body = app.current_request.json_body
#         follower = body["follower"]
#         followers = add_first_follower(username, follower)
#         return Response(
#             body={"user": followers},
#             status_code=201,
#         )
#     except Exception as e:
#         raise ChaliceViewError(e)

# @app.on_ws_connect()
# def handle_connect(event):
#     event.connection_id
#     # get username


# @app.on_ws_message()
# def handle_message(event):
#     try:
#         # message_type = event.json_body["type"]
#         username = event.json_body["username"]
#         app.websocket_api.send(
#             event.connection_id, json.dumps({"username": username})
#         )
#     except WebsocketDisconnectedError as e:
#         pass


# @app.on_ws_disconnect()
# def handle_disconnect():
#     print(5)


# @app.lambda_function(name="runs_stream_handler")
# def push_runs(event, context):
#     print(event)

# @app.route('/connections', methods=["POST", "PATCH", "GET"])
# def connections():
#     method = app.current_request.method
#     if method == "POST":
#         try:
#             body = app.current_request.json_body
#             username = body["username"]
#             Connection.add_one(username)
#         except Exception as e:
#             raise ChaliceViewError(e)
#     elif method == "PATCH":
#         try:
#             body = app.current_request.json_body
#             username = body["username"]
#             Connection.remove_connection_id(username)
#         except Exception as e:
#             raise ChaliceViewError(e)
#     elif method == "GET":
#         try:
#             query = app.current_request.query_params
#             subscriptions = query["subscriptions"]
#             Connection.get_connection_ids_for_subscriptions(subscriptions)
#         except Exception as e:
#             raise ChaliceViewError(e)


# @app.route('/connections/user', methods=["POST"])
# def user_by_connection():
#     method = app.current_request.method
#     if method == "POST":
#         try:
#             body = app.current_request.json_body
#             connection_id = body["connection_id"]
#             print(connection_id)
#             response = Connection.get_user_by_connection_id_and_remove_id(connection_id)
#             return Response(
#                 body={"response": response},
#                 status_code=200
#             )
#         except Exception as e:
#             raise ChaliceViewError(e)
