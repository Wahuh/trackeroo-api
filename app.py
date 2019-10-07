from boto3.session import Session
from chalice import (
    Chalice,
    Response,
    BadRequestError,
    ChaliceViewError,
    WebsocketDisconnectedError,
)
from chalicelib.auth import signup, authorizer, login
import json

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
        add_run(username=username, start_time=start_time)
    except KeyError:
        raise BadRequestError("username and start_time must be valid")
    except Exception as e:
        raise ChaliceViewError(e)


# @app.on_ws_connect()
# def handle_connect(event):
#     event.connection_id
#     # get username


@app.on_ws_message()
def handle_message(event):
    try:
        # message_type = event.json_body["type"]
        username = event.json_body["username"]
        app.websocket_api.send(
            event.connection_id, json.dumps({"username": username})
        )
    except WebsocketDisconnectedError as e:
        pass


# @app.on_ws_disconnect()
# def handle_disconnect():
#     print(5)


# @app.lambda_function(name="runs_stream_handler")
# def push_runs(event, context):
#     print(event)
