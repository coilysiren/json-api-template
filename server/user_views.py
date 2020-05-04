"""
view.py is a thin layer used to mapping our routes to our controller logic
"""

import json

import marshmallow

import server.errors as errors
import server.schema as schema
from server.user_controller import UserController


class UserViews:
    controller: UserController

    def __init__(self, controller: UserController):
        self.controller = controller

    def on_post_users(self, req, resp):
        # parse inputs
        try:
            data = schema.UserSchema().load(req)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic
        try:
            output = self.controller.create_user(data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        json_output = json.dumps(output)

    def on_get_users(self, req, resp):
        # parse inputs
        try:
            data = schema.UserQueryParamSchema().load(req)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic
        try:
            output = self.controller.get_users(data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        json_output = json.dumps(output)

    def on_get_user(self, req, resp):
        # parse inputs
        try:
            data = schema.UserPathParamSchema().load(req)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic
        try:
            output = self.controller.get_user(data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        json_output = json.dumps(output)

    def on_put_user(self, req, resp):
        # parse inputs
        try:
            path_data = schema.UserPathParamSchema().load(req)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # parse inputs - json data
        try:
            body_data = schema.UserSchema().load(req)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic
        try:
            output = self.controller.update_user(path_data, body_data)

        # process errors
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        json_output = json.dumps(output)
