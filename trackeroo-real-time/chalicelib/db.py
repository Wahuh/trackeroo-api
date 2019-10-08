import boto3
import os

database_url = os.environ.get("DATABASE_URL")
region_name = os.environ.get("REGION_NAME")
connection = boto3.resource("dynamodb", region_name=region_name)
streams_connection = boto3.client("dynamodbstreams")
