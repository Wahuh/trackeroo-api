from chalice import CognitoUserPoolAuthorizer
import boto3
import os
from .models import User

cognito = boto3.client("cognito-idp", region_name="eu-west-1")

user_pool_id = os.environ.get("USER_POOL_ID")
app_client_id = os.environ.get("APP_CLIENT_ID")
user_pool_arn = os.environ.get("USER_POOL_ARN")

authorizer = CognitoUserPoolAuthorizer(
    app_client_id, header="Authorization", provider_arns=[user_pool_arn]
)


def login(username, password):
    initiate_auth_response = cognito.admin_initiate_auth(
        AuthFlow="ADMIN_NO_SRP_AUTH",
        ClientId=app_client_id,
        UserPoolId=user_pool_id,
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )
    id_token = initiate_auth_response["AuthenticationResult"]["IdToken"]
    return id_token


def signup(username, password):
    # TODO check if username is already registered
    cognito.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        MessageAction="SUPPRESS",
        TemporaryPassword=password,
    )
    initiate_auth_response = cognito.admin_initiate_auth(
        AuthFlow="ADMIN_NO_SRP_AUTH",
        ClientId=app_client_id,
        UserPoolId=user_pool_id,
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )
    respond_to_auth_challenge_response = cognito.respond_to_auth_challenge(
        ClientId=app_client_id,
        ChallengeName="NEW_PASSWORD_REQUIRED",
        ChallengeResponses={"USERNAME": username, "NEW_PASSWORD": password},
        Session=initiate_auth_response["Session"],
    )
    id_token = respond_to_auth_challenge_response["AuthenticationResult"][
        "IdToken"
    ]
    # User.add_one(username=username)
    return id_token
