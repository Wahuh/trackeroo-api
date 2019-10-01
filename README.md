# Trackeroo Api

## Running the project locally

### Prerequisites

* Python 3.6 installed. Run `python3 -v` to check.

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

### Configuring VSCode

Install the Python extension for VSCode: https://marketplace.visualstudio.com/items?itemName=ms-python.python

> MAKE SURE YOUR VIRTUAL ENVIRONMENT IS ACTIVATED FIRST

* Press `cmd + shift + p` and search for 'Python: Select Interpreter'. Select the Python 3.6 which is inside your `venv` folder.
* Press `cmd + shift + p` and search for 'Python: Select Linter'. Select `flake8` and you'll be prompted to install it.
* Press `cmd + shift + i` and you should be prompted to choose a formatter for Python files. Install `black` as your formatter.
