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

    @staticmethod
    def update_distance(username, distance):
        try:
            distance_decimal = Decimal(str(distance))
            update_response = _users_table.update_item(
                Key={"username": username},
                UpdateExpression="SET cumulative_distance = cumulative_distance + :distance",
                ExpressionAttributeValues={":distance": distance_decimal},
                ReturnValues="ALL_NEW",
            )
            return update_response["Attributes"]
        except Exception as e:
            raise e


    @staticmethod
    def update_rewards(username):
        try:
            update_response = _users_table.update_item(
                Key={
                    'username': username
                },
                UpdateExpression="SET rewards_earned = rewards_earned + :rewards",
                ExpressionAttributeValues={
                    ":rewards": 1
                },
                ReturnValues="ALL_NEW"
            )
            print(update_response)
            return update_response
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
    def get_users_runs(username):
        try:
            scan_response = _runs_table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr("username").eq(
                    username
                )
            )
            return scan_response["Items"]
        except Exception as e:
            raise e

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
    def update_finish_time(
        username,
        run_id,
        average_speed,
        total_distance,
        finish_time,
        coordinates,
    ):
        try:
            response = _runs_table.update_item(
                TableName="runs",
                Key={"username": username, "run_id": run_id},
                UpdateExpression="SET average_speed=:speed, total_distance=:distance, coordinates=:coordinates, finish_time=:finish",
                ExpressionAttributeValues={
                    ":finish": finish_time,
                    ":speed": Decimal(str(average_speed)),
                    ":distance": Decimal(str(total_distance)),
                    ":coordinates": coordinates,
                },
                ReturnValues="ALL_NEW",
            )
            return response["Attributes"]
        except Exception as e:
            raise e

    @staticmethod
    def update_stats(
        username,
        run_id,
        latitude,
        longitude,
        average_speed,
        total_distance,
        coordinates,
    ):
        try:
            response = _runs_table.update_item(
                TableName="runs",
                Key={"username": username, "run_id": run_id},
                UpdateExpression="SET average_speed=:speed, total_distance=:distance, latitude=:latitude, longitude=:longitude, coordinates=:coordinates",
                ExpressionAttributeValues={
                    ":speed": Decimal(str(average_speed)),
                    ":distance": Decimal(str(total_distance)),
                    ":latitude": Decimal(str(latitude)),
                    ":longitude": Decimal(str(longitude)),
                    ":coordinates": coordinates,
                },
                ReturnValues="ALL_NEW",
            )
            print(response)
            return response["Attributes"]
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def update_one(**kwargs):
        print(kwargs)
        # try:
        #     patch_run_response = _runs_table.update_item(
        #         TableName="runs",
        #         Key={"username": username, "run_id": run_id},
        #         UpdateExpression="SET finish_time=:finish, average_speed=:average, total_distance=:distance",
        #         ExpressionAttributeValues={
        #             ":finish": {"S": finish_time},
        #             ":average": {"N": average_speed},
        #             ":distance": {"N": total_distance},
        #         },
        #         ReturnValues="ALL_NEW",
        #     )
        #     return patch_run_response
        # except Exception as e:
        #     raise e

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

class Rewards:
    @staticmethod
    def add_one(challenge, reward):
        try:
            new_reward_id = str(uuid.uuid4())
            decimal_challenge = Decimal(challenge)
            reward_item = {
                "reward_id": new_reward_id,
                "challenge": decimal_challenge,
                "reward": reward,
                "completed": False
            }
            _rewards_table.put_item(Item=reward_item)
            return reward_item
        except Exception as e:
            raise e

    @staticmethod
    def update_reward(reward_id, winner):
        try:
            patch_response = _rewards_table.update_item(
                Key={
                    'reward_id': reward_id
                },
                UpdateExpression='SET winner=:winner, completed=:completed',
                ExpressionAttributeValues={
                    ':winner': {"S": winner},
                    ':completed': True
                },
                ReturnValues="ALL_NEW"
            )
            return patch_response
        except Exception as e:
            raise e

    @staticmethod
    def get_rewards(completed):
        try:
            if completed == "yes":
                scan_response = _rewards_table.scan(
                    FilterExpression=boto3.dynamodb.conditions.Attr("completed").eq(True)
                )
            else:
                scan_response = _rewards_table.scan(
                    FilterExpression=boto3.dynamodb.conditions.Attr("completed").eq(False)
                )
            return scan_response["Items"]
        except Exception as e:
            raise e
