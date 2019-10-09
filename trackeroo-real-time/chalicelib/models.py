import boto3
from .db import connection
import uuid
import json
from decimal import Decimal

_users_table = connection.Table("users")
_runs_table = connection.Table("runs")
_followers_table = connection.Table("followers")
_subscriptions_table = connection.Table("subscriptions")
_connections_table = connection.Table("connections")


class User:
    @staticmethod
    def add_one(username):
        new_user_item = {
            "username": username,
            "cumulative_distance": 0,
            "followers": [],
            "subscriptions": [],
        }
        try:
            _users_table.put_item(Item=new_user_item)
            return new_user_item
        except Exception as e:
            raise e

    @staticmethod
    def add_follower(username, follower):
        try:
            patch_user_response = _users_table.update_item(
                TableName="users",
                Key={"username": username},
                UpdateExpression="SET followers = list_append(followers, :followers)",
                ExpressionAttributeValues={":followers": [follower]},
                ReturnValues="ALL_NEW",
            )
            return patch_user_response
        except Exception as e:
            raise e

    @staticmethod
    def add_subscription(username, subscription):
        try:
            patch_user_response = _users_table.update_item(
                TableName="users",
                Key={"username": username},
                UpdateExpression="SET subscriptions = list_append(subscriptions, :subscriptions)",
                ExpressionAttributeValues={":subscriptions": [subscription]},
                ReturnValues="ALL_NEW",
            )
            return patch_user_response
        except Exception as e:
            raise e

    @staticmethod
    def scan_users(start_username=None):
        try:
            scan_response = None
            if start_username:
                scan_response = _users_table.scan(
                    TableName="users",
                    Limit=10,
                    ExclusiveStartKey={"username": start_username},
                )
            else:
                scan_response = _users_table.scan(TableName="users", Limit=10)
            users = scan_response["Items"]
            last_username = None
            if "LastEvaluatedKey" in scan_response:
                if "username" in scan_response["LastEvaluatedKey"]:
                    last_username = scan_response["LastEvaluatedKey"][
                        "username"
                    ]
            new_response = {"users": users, "last_username": last_username}
            return new_response
        except Exception as e:
            raise e

    @staticmethod
    def get_user(username):
        try:
            get_response = _users_table.get_item(Key={"username": username})
            return get_response["Item"]
        except Exception as e:
            raise e

    # @staticmethod
    # def update_one(username, first_name, last_name, age, height, weight):
    #         'first_name': first_name,
    #         'last_name': last_name,
    #         'age': age,
    #         'height': height,
    #         'weight': weight,


class Run:
    @staticmethod
    def add_one(username, start_time):
        new_run_id = str(uuid.uuid4())
        new_run_item = {
            "run_id": new_run_id,
            "username": username,
            "start_time": start_time,
        }
        try:
            _runs_table.put_item(Item=new_run_item)
            return new_run_item
        except Exception as e:
            raise e

    @staticmethod
    def update_one(
        run_id, username, finish_time, average_speed, total_distance
    ):
        try:
            patch_run_response = _runs_table.update_item(
                TableName="runs",
                Key={"username": username, "run_id": run_id},
                UpdateExpression="SET finish_time=:finish, average_speed=:average, total_distance=:distance",
                ExpressionAttributeValues={
                    ":finish": {"S": finish_time},
                    ":average": {"N": average_speed},
                    ":distance": {"N": total_distance},
                },
                ReturnValues="ALL_NEW",
            )
            return patch_run_response
        except Exception as e:
            raise e

    @staticmethod
    def get_runs_by_subscriptions(subscriptions):
        try:
            scan_response = _runs_table.scan(
                IndexName="username-start_time-index",
                ScanFilter={
                    "username": {
                        "AttributeValueList": subscriptions,
                        "ComparisonOperator": "IN",
                    }
                },
            )
            runs = scan_response["Items"]
            sorted_runs = sorted(runs, key=lambda run: run["start_time"])
            return sorted_runs
        except Exception as e:
            raise e


class Followers:
    @staticmethod
    def get_one(username):
        try:
            response = _followers_table.get_item(Key={"username": username})
            return response["Item"]
        except Exception as e:
            raise e

    @staticmethod
    def add_one(username, follower):
        new_follower_item = {"username": username, "followers": [follower]}
        try:
            _followers_table.put_item(Item=new_follower_item)
            return new_follower_item
        except Exception as e:
            raise e

    @staticmethod
    def update_one(username, follower):
        try:
            patch_follower_response = _followers_table.update_item(
                TableName="followers",
                Key={"username": username},
                UpdateExpression="SET followers = list_append(followers, :followers)",
                ExpressionAttributeValues={
                    ":followers": {"L": [{"S": follower}]}
                },
                ReturnValues="ALL_NEW",
            )
            return patch_follower_response
        except Exception as e:
            raise e


class Subscriptions:
    @staticmethod
    def add_one(username, subscription):
        new_subscription_item = {
            "username": username,
            "subscriptions": [subscription],
        }
        try:
            _subscriptions_table.put_item(Item=new_subscription_item)
            return new_subscription_item
        except Exception as e:
            raise e

    @staticmethod
    def update_one(username, subscription):
        try:
            patch_subscription_response = _subscriptions_table.update_item(
                TableName="subscriptions",
                Key={"username": {"S": username}},
                UpdateExpression="SET subscriptions = list_append(subscriptions, :subscriptions)",
                ExpressionAttributeValues={
                    ":subscriptions": {"L": [{"S": subscription}]}
                },
                ReturnValues="ALL_NEW",
            )
            return patch_subscription_response
        except Exception as e:
            raise e


class Connection:
    @staticmethod
    def add_one(username):
        try:
            new_connection_item = {"username": username}
            put_connection_response = _connections_table.put_item(
                Item=new_connection_item
            )
            return put_connection_response
        except Exception as e:
            raise e

    @staticmethod
    def get_connection_id(username):
        try:
            get_response = _connections_table.get_item(
                Key={"username": username}
            )
            print(get_response)
            print(
                get_response,
                get_response["Item"],
                get_response["Item"].get("connection_id"),
            )
            return get_response["Item"].get("connection_id")
        except Exception as e:
            raise e

    @staticmethod
    def add_connection_id(username, connection_id):
        try:
            updated_connection_response = _connections_table.update_item(
                TableName="connections",
                Key={"username": username},
                UpdateExpression="SET connection_id=:connection",
                ExpressionAttributeValues={":connection": connection_id},
                ReturnValues="ALL_NEW",
            )
            return updated_connection_response
        except Exception as e:
            raise e

    @staticmethod
    def remove_connection_id(username):
        try:
            updated_connection_response = _connections_table.update_item(
                TableName="connections",
                Key={"username": username},
                UpdateExpression="REMOVE connection_id",
                ReturnValues="ALL_NEW",
            )
            return updated_connection_response
        except Exception as e:
            raise e
