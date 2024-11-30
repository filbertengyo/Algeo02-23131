# EDP445 Backend

Backend sourcecode for the EDP445 audio lookup web application.


## Pre-Requisites

The following pre-requisites are required to start developing the EDP445 backend:
- Python 3.12
- pip
- venv

To check if Python is installed (Make sure the correct version is installed):
```
python --version

```
To check if pip is installed:
```
pip --version
```
To check if venv is installed:
```
python -m venv --help
```

## Setup
The following are the setup steps required to develop and run the program:
1. Setup a python virtual environment in the env folder.
```
python -m venv .venv
```
2. Enter the python virtual environment.

Windows:
```
./.venv/Scripts/activate.bat
```
Linux:
```
./.venv/bin/activate
```
3. Install the project requirements listed in requirements.txt.
```
pip install -r requirements.txt
```

## How to Run
The following are instructions to run the backend server:
1. Open the python virtual environment

Windows:
```
./.venv/Scripts/activate.bat
```
Linux:
```
./.venv/bin/activate
```
2. Run the flask app
```
flask run --host=0.0.0.0
```