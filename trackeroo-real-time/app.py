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
import os

region_name = os.environ.get("REGION_NAME")
ws_id = os.environ.get("WS_ID")
stage = os.environ.get("STAGE")

app = Chalice(app_name="trackeroo-real-time")
app.experimental_feature_flags.update(["WEBSOCKETS"])
app.websocket_api.session = Session()

# endpoint_url = (
#   f"https://{api_id}.execute-api.{region_name}.amazonaws.com/api/{stage}"
# )

endpoint_url = f"https://{ws_id}.execute-api.{region_name}.amazonaws.com/api/"

print(endpoint_url)

client = boto3.client(
    "apigatewaymanagementapi",
    region_name=region_name,
    endpoint_url=endpoint_url,
)


@app.lambda_function(name="runs_stream_handler")
def push_runs(event, context):
    app.websocket_api.configure("acmxvpvx98", "dev")
    if "Records" in event:
        records = event["Records"]
        for record in records:
            event_name = record["eventName"]
            if event_name == "INSERT":
                print(record)
                raw_run = record["dynamodb"]["NewImage"]
                run = json_util.loads(raw_run)
                username = run["username"]
                json_run = json.dumps({"run": run})
                connection_id = get_connection_id(username)
                print(connection_id)
                if connection_id:
                    try:
                        client.post_to_connection(
                            Data=json_run, ConnectionId=connection_id
                        )
                        # app.websocket_api.send(connection_id, json_run)
                    except Exception as e:
                        print(e)
                        pass
                connection_ids = get_all_followers_connection_ids(username)
                if connection_ids:
                    print(connection_ids)
                    for cid in connection_ids:
                        try:
                            res = client.get_connection(ConnectionId=cid)
                            print(res)
                            print(cid, json_run)
                            client.post_to_connection(
                                Data=json_run, ConnectionId=cid
                            )
                            app.websocket_api.send(cid, json_run)
                        except Exception as e:
                            print(e)
                            pass


# policy dev is used by default
