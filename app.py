from chalice import Chalice, Response, BadRequestError, ChaliceViewError
from chalicelib.auth import signup, authorizer

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
