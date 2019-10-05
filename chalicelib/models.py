import boto3
from .db import connection
import uuid

_users_table = connection.Table("users")
_runs_table = connection.Table("runs")
_followers_table = connection.Table("followers")
_subscriptions_table = connection.Table("subscriptions")

print('**************************************************')

# print(boto3.client('dynamodb').list_tables())
dynamodb_resource = boto3.resource("dynamodb")


class User:
    @staticmethod
    def add_one(username):
        _users_table.put_item(Item={"username": username})


class Run:
    @staticmethod
    def add_one(
        username,
        start_time
    ):
        new_run_id = str(uuid.uuid4())
        new_run_item = {
            'run_id': new_run_id,
            'username': username,
            'start_time': start_time
        }
        try:
            # put_run_response = _runs_table.put_item(Item=new_run_item)
            put_run_response = dynamodb_resource.Table("runs").put_item(Item=new_run_item)
            print(put_run_response, f'run inserted {new_run_id}')
            return new_run_item
        except Exception as e:
            raise e


class Followers:
    @staticmethod
    def add_one(
        username,
        follower
    ):
        new_follower_item = {
            'username': username,
            'followers': [follower]
        }
        try:
            put_followers_response = _followers_table.put_item(Item=new_follower_item)
            print(put_followers_response, f'inserted new follower: {follower}')
            return new_follower_item
        except Exception as e:
            raise e


class Subscriptions:
    @staticmethod
    def add_one(
        username,
        subscription
    ):
        new_subscription_item = {
            'username': username,
            'subscriptions': [subscription]
        }
        try:
            put_subscription_response = _subscriptions_table.put_item(Item=new_subscription_item)
            print(put_subscription_response, f'inserted new subscription')
            return new_subscription_item
        except Exception as e:
            raise e
