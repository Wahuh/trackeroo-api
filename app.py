from chalice import Chalice, Response, BadRequestError, ChaliceViewError
from chalicelib.auth import signup, authorizer, login
from chalicelib.runs import add_run
from chalicelib.users import add_user
from chalicelib.followers import add_follower
from chalicelib.subscriptions import add_subscription

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
        raise BadRequestError("Username or start_time is missing")
    except Exception as e:
        raise ChaliceViewError(e)


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
        raise BadRequestError("Required input is missing")
    except Exception as e:
        raise ChaliceViewError(e)
