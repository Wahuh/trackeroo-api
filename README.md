# Trackeroo Api

## Running the project locally

### Prerequisites

- Python 3.6 installed. Run `python3 -v` to check.
- Java 6.0+ installed. Run `java -version` to check.
  1. `sudo apt install default-jre` (linux)
- DynamoDB installed locally
  1. https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

### Cloning

`git clone https://github.com/Wahuh/trackeroo-api.git`

`cd trackeroo-api`

### Setting up your virtual environment

`python3 -m venv venv`

Activate your virtual environment

`source venv/bin/activate`

### Installing dependencies

`pip install -r requirements.txt`

Setup git hooks, linting and formatting on pre-commit.

`pre-commit install`

### Setting up AWS Credentials

`pip install awscli`
`aws configure`

- AWS Access Key ID [None]: _your_access_key_
- AWS Secret Access Key [None]: _your_secret_key_
- Default region name [None]: _eu-west-1_
- Default output format [None]: _json_

### Configuring VSCode

Install the Python extension for VSCode: https://marketplace.visualstudio.com/items?itemName=ms-python.python

> MAKE SURE YOUR VIRTUAL ENVIRONMENT IS ACTIVATED FIRST

- Press `cmd + shift + p` and search for 'Python: Select Interpreter'. Select the Python 3.6 which is inside your `venv` folder.
- Press `cmd + shift + p` and search for 'Python: Select Linter'. Select `flake8` and you'll be prompted to install it.
- Press `cmd + shift + i` and you should be prompted to choose a formatter for Python files. Install `black` as your formatter.

### Running DynamoDB

Make sure you are in the same directory as the DynamoDBLocal.jar file.

`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 7000`

### Setting up Environment Variables

Create a directory called `.chalice` then inside of it create a `config.json` file which looks like:

```
{
  "version": "2.0",
  "app_name": "trackeroo-api",
  "environment_variables": {
    "USER_POOL_ID": user_pool_id # from cognito dashboard
    "APP_CLIENT_ID": app_client_id # from cognito dashboard
    "REGION_NAME": "eu-west-1",
    "USER_POOL_ARN": user_pool_arn # from cognito dashboard
  },
  "stages": {
    "dev": {
      "autogen_policy": false,
      "api_gateway_stage": "api",
      "environment_variables": {
        "DATABASE_URL": "http://localhost:7000"
      }
    }
  }
}

```

In the same directory, create a `policy-dev.json` file which looks like:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cognito-identity:*",
        "cognito-idp:*",
        "cognito-sync:*",
        "iam:ListRoles",
        "iam:ListOpenIdConnectProviders",
        "sns:ListPlatformApplications"
      ],
      "Resource": "*"
    }
  ]
}
```

### Starting the Server finally!

`chalice local`
