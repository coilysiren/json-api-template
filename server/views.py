"""
view.py is a thin layer used to mapping our routes to our controller logic
"""

import json

import flask

import server.errors as errors
from server.controller import Controller


class Views:
    controller: Controller

    def __init__(self, controller: Controller):
        self.controller = controller

    def create_user(self):
        # parse inputs
        data = flask.request.get_json()

        # initalize outputs
        output = {}
        status_code = 200

        # do business logic
        try:
            output = self.controller.create_user(data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            status_code = err.status_code

        return json.dumps(output), status_code

    def get_users(self):
        # parse inputs
        data = dict(flask.request.args)

        # initalize outputs
        output = {}
        status_code = 200

        # do business logic
        try:
            output = self.controller.get_users(data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            status_code = err.status_code

        return json.dumps(output), status_code

    def get_user(self, user_id):
        # initalize outputs
        output = {}
        status_code = 200

        # do business logic
        try:
            output = self.controller.get_user({"user_id": user_id})

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            status_code = err.status_code

        return json.dumps(output), status_code

    def update_user(self, user_id):
        # parse inputs
        data = flask.request.get_json()

        # initalize outputs
        output = {}
        status_code = 200

        # do business logic
        try:
            output = self.controller.update_user({"user_id": user_id}, data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            status_code = err.status_code

        return json.dumps(output), status_code
