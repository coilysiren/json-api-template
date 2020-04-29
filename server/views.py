"""
view.py is a thin layer used to mapping our routes to our controller logic

The views have no tests primarily because I wanted to avoid writing a bunch of
integration tests that span across both flask and sqlalchemy. Ultimately I think
that is a good choice, since integration tests are harder to write when they span
across more systems.

Because of that fact though, any code inside of the view layer is "dangerous"
(eg. untested). That means that as much code should be pushed into the controller
as possible, including the `errors.ErrorWithStatus` logic. Assuming of course,
that making that change would be in line with how "controllers" are usually
thought of.
"""

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


def get_user(user_id):
    # initalize outputs
    output = {}
    status_code = 200

    # do business logic
    try:
        output = controller.get_user(user_id)

    # process errors
    except errors.ErrorWithStatus as e:
        output = {"error": str(e)}
        status_code = e.status_code

    return json.dumps(output), status_code


def update_user(user_id):
    # parse inputs
    data = flask.request.get_json()

    # initalize outputs
    output = {}
    status_code = 200

    # do business logic
    try:
        output = controller.update_user(user_id, data)

    # process errors
    except errors.ErrorWithStatus as e:
        output = {"error": str(e)}
        status_code = e.status_code

    return json.dumps(output), status_code
