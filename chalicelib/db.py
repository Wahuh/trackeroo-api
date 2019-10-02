import boto3
import os

database_url = os.environ.get("DATABASE_URL")

connection = boto3.resource("dynamodb", endpoint_url=database_url)
