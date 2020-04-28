# isort: stdlib imports
import json

# isort: 3rd party imports
import flask
# isort: our imports
from server.controller import controller


def create_user():
    # parse inputs
    data = flask.request.get_json()
    if data == None:
        data = {}

    # initalize outputs
    output = {}
    status_code = 200

    # do business logic
    try:
        output = controller.create_user(data)

    # process errors
    except BaseException:
        status_code = 500

    # return
    return json.dumps(output), status_code


def get_users():
    # parse inputs
    data = flask.request.get_json()
    if data == None:
        data = {}

    # initalize outputs
    output = {}
    status_code = 200

    # do business logic
    try:
        output = controller.get_users(data)

    # process errors
    except BaseException:
        status_code = 500

    # return
    return json.dumps(output), status_code
