import boto3
from boto3.session import Session
from chalice import (
    Chalice,
    Response,
    BadRequestError,
    ChaliceViewError,
    WebsocketDisconnectedError,
)
from chalicelib.auth import signup, authorizer, login
from chalicelib.runs import add_run, update_run, get_runs_by_subscriptions
from chalicelib.users import (
    add_user,
    get_users,
    add_follower,
    add_subscription,
    get_user,
    get_all_followers_connection_ids,
)
import json
from chalicelib.models import Connection
from chalicelib.connections import (
    handle_connection,
    handle_disconnection,
    get_connection_id,
)
import jwt
from dynamodb_json import json_util

app = Chalice(app_name="trackeroo-api")
app.experimental_feature_flags.update(["WEBSOCKETS"])
app.websocket_api.session = Session()


@app.route("/", cors=True, methods=["GET"], authorizer=authorizer)
def index():
    return {"hello": "world"}


@app.route("/me", cors=True, methods=["GET"])
def get_me():
    try:
        token = app.current_request.headers["Authorization"]
        print(token)
        details = jwt.decode(token, algorithms=["RS256"])
        user = get_user(details["username"])
        return Response(body={"user": user}, status_code=200)
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/signup", cors=True, methods=["POST"])
def post_signup():
    try:
        body = app.current_request.json_body
        password = body["password"]
        username = body["username"]
        jwt = signup(username=username, password=password)
        return Response(
            body={"user": {"username": username}},
            status_code=200,
            headers={"Authorization": jwt},
        )
    except KeyError:
        raise BadRequestError("Username or password is missing")
    except Exception as e:
        print(e)
        raise ChaliceViewError(e)


@app.route("/login", cors=True, methods=["POST"])
def post_login():
    try:
        body = app.current_request.json_body
        password = body["password"]
        username = body["username"]
        jwt = login(username=username, password=password)
        return Response(
            body={"user": {"username": username}},
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
        return Response(body={"run": run}, status_code=201)
    except KeyError:
        raise BadRequestError("Bad request body")
    except Exception as e:
        print(e)
        raise ChaliceViewError(e)


@app.route("/runs/{run_id}", cors=True, methods=["PATCH"])
def patch_run(run_id):
    try:
        body = app.current_request.json_body
        # username = body["username"]
        # finish_time = body["finish_time"]
        # average_speed = body["average_speed"]
        # total_distance = body["total_distance"]
        run = update_run(**body, run_id=run_id)
        print(run)
        return Response(body={"run": run}, status_code=200)
    except KeyError:
        raise BadRequestError("Bad request body")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/runs", cors=True, methods=["GET"])
def get_runs():
    try:
        query = app.current_request.query_params
        if query:
            if "username" in query:
                username = query["username"]
                user = get_user(username)
                if user["subscriptions"]:
                    runs = get_runs_by_subscriptions(user["subscriptions"])
                    return Response(body={"runs": runs}, status_code=200)
                else:
                    return Response(body={"runs": []}, status_code=200)
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users", cors=True, methods=["GET"])
def fetch_users():
    try:
        query = app.current_request.query_params
        start_username = None

        if query:
            if "start_username" in query:
                start_username = query["start_username"]

        users = get_users(start_username)
        return Response(body=users, status_code=200)
    except Exception as e:
        raise e


@app.route("/users", cors=True, methods=["POST"])
def post_user():
    try:
        body = app.current_request.json_body
        username = body["username"]
        user = add_user(username)
        return Response(body={"user": user}, status_code=201)
    except KeyError:
        raise BadRequestError("username must be valid")
    except Exception as e:
        raise ChaliceViewError(e)


@app.route("/users/{username}/followers", cors=True, methods=["PATCH"])
def patch_user_followers(username):
    try:
        body = app.current_request.json_body
        follower = body["follower"]
        add_follower(username, follower)
        return Response(body={}, status_code=204)
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
        return Response(body={}, status_code=204)
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


@app.route("/users/{username}/followers", cors=True, methods=["POST"])
def follower(username):
    try:
        body = app.current_request.json_body
        follower = body["follower"]
        followers = add_follower(username, follower)
        return Response(body={"user": followers}, status_code=201)
    except Exception as e:
        raise ChaliceViewError(e)


# @app.on_ws_disconnect()
# def disconnect(event):
#     connection_id = event.connection_id
#     try:
#         handle_disconnection()
#     except Exception:
#         pass


@app.on_ws_message()
def handle_message(event):
    connection_id = event.connection_id
    try:
        message_type = event.json_body["type"]
        if message_type == "connect":
            username = event.json_body["username"]
            handle_connection(username, connection_id)
        # app.websocket_api.send(
        # event.connection_id, json.dumps({"username": username})
        # )
    except WebsocketDisconnectedError:
        pass


# @app.on_ws_disconnect()
# def handle_disconnect():
#     print(5)
# region_name = os.environ.get("REGION_NAME")
# client = boto3.client("apigatewaymanagementapi", region_name=region_name, endpoint_url=)


# @app.route('/connections', methods=["POST", "PATCH"])
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

# wait 5 mins between deletes and deploys because CloudFront caches 500 errors
