import boto3
from .db import connection
import uuid

_users_table = connection.Table("users")
_runs_table = connection.Table('runs')

dynamodb_client = boto3.client("dynamodb")
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
        new_run_id = uuid.uuid1()
        put_run_response = _runs_table.put_item(
            Item={
                'run_id': new_run_id,
                'username': username,
                'start_time': start_time
            }
        )
        print(put_run_response, f'run inserted {new_run_id}')
        return put_run_response
