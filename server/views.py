"""
view.py is a thin layer used to mapping our routes to our controller logic
"""

import json

import flask
import marshmallow

import server.errors as errors
import server.schema as schema
from server.controller import Controller


class Views:
    controller: Controller

    def __init__(self, controller: Controller):
        self.controller = controller

    def create_user(self):
        # parse inputs
        try:
            _input = flask.request.get_json()
            data = schema.UserSchema().load(_input)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

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

        # format and return output
        json_output = json.dumps(output)
        return json_output, status_code

    def get_users(self):
        # parse inputs
        try:
            _input = dict(flask.request.args)
            data = schema.UserQueryParamSchema().load(_input)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

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

        # format and return output
        json_output = json.dumps(output)
        return json_output, status_code

    def get_user(self, user_id):
        # parse inputs
        try:
            _input = {"user_id": user_id}
            data = schema.UserPathParamSchema().load(_input)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # initalize outputs
        output = {}
        status_code = 200

        # do business logic
        try:
            output = self.controller.get_user(data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            status_code = err.status_code

        # format and return output
        json_output = json.dumps(output)
        return json_output, status_code

    def update_user(self, user_id):
        # parse inputs
        try:
            _path_input = {"user_id": user_id}
            path_data = schema.UserPathParamSchema().load(_path_input)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # parse inputs - json data
        try:
            _body_input = flask.request.get_json()
            body_data = schema.UserSchema().load(_body_input)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # initalize outputs
        output = {}
        status_code = 200

        # do business logic
        try:
            output = self.controller.update_user(path_data, body_data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            status_code = err.status_code

        # format and return output
        json_output = json.dumps(output)
        return json_output, status_code
