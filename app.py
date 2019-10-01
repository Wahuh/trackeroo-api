from chalice import Chalice

app = Chalice(app_name="trackeroo-api")


@app.route("/")
def index():
    return {"hello": "world"}
