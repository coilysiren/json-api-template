import json

import flask
import server.errors as errors
from server.controller import controller


def create_user():
    # parse inputs
    data = flask.request.get_json()

    # initalize outputs
    output = {}
    status_code = 200

    # do business logic
    try:
        output = controller.create_user(data)

    # process errors
    except errors.ErrorWithStatus as e:
        output = {"error": str(e)}
        status_code = e.status_code

    return json.dumps(output), status_code


def get_users():
    # parse inputs
    data = flask.request.args

    # initalize outputs
    output = {}
    status_code = 200

    # do business logic
    try:
        output = controller.get_users(data)

    # process errors
    except errors.ErrorWithStatus as e:
        output = {"error": str(e)}
        status_code = e.status_code

    return json.dumps(output), status_code
