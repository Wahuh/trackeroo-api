# Trackeroo Api

## Running the project locally

### Prerequisites

* Python 3.6 installed. Run `python3 -v` to check.
* Java 6.0+ installed. Run `java -version` to check.
  1. `sudo apt install default-jre` (linux)
* DynamoDB installed locally
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

* AWS Access Key ID [None]: *your_access_key* 
* AWS Secret Access Key [None]: *your_secret_key*
* Default region name [None]: *eu-west-1*
* Default output format [None]: *json*

### Configuring VSCode

Install the Python extension for VSCode: https://marketplace.visualstudio.com/items?itemName=ms-python.python

> MAKE SURE YOUR VIRTUAL ENVIRONMENT IS ACTIVATED FIRST

* Press `cmd + shift + p` and search for 'Python: Select Interpreter'. Select the Python 3.6 which is inside your `venv` folder.
* Press `cmd + shift + p` and search for 'Python: Select Linter'. Select `flake8` and you'll be prompted to install it.
* Press `cmd + shift + i` and you should be prompted to choose a formatter for Python files. Install `black` as your formatter.

### Running DynamoDB

Make sure you are in the same directory as the DynamoDBLocal.jar file.

`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 7000`
