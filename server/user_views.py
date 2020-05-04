"""
view.py is a thin layer used to mapping our routes to our controller logic
"""

import json

import falcon
import marshmallow

import server.errors as errors
import server.schema as schema
from server.user_controller import UserController


class UserViews:
    controller: UserController

    def __init__(self, controller: UserController):
        self.controller = controller

    def on_post_users(self, req: falcon.Request, resp: falcon.Response):
        # parse inputs
        try:
            data = schema.UserSchema().load(req.params)
        except marshmallow.ValidationError as err:
            resp.media = json.dumps({"error": err.messages})
            resp.status = falcon.HTTP_400
            return

        # do business logic
        try:
            output = self.controller.create_user(data)
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        resp.media = output

    def on_get_users(self, req: falcon.Request, resp: falcon.Response):
        # parse inputs
        try:
            data = schema.UserQueryParamSchema().load(req.params)
        except marshmallow.ValidationError as err:
            resp.media = json.dumps({"error": err.messages})
            resp.status = falcon.HTTP_400
            return

        # do business logic
        try:
            output = self.controller.get_users(data)
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        resp.media = output

    def on_get_user(self, req: falcon.Request, resp: falcon.Response, user_id: str):
        # parse inputs
        try:
            data = schema.UserPathParamSchema().load({"user_id": user_id})
        except marshmallow.ValidationError as err:
            resp.media = json.dumps({"error": err.messages})
            resp.status = falcon.HTTP_400
            return

        # do business logic
        try:
            output = self.controller.get_user(data)
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        resp.media = output

    def on_put_user(self, req: falcon.Request, resp: falcon.Response, user_id: str):
        # parse inputs - get data
        try:
            path_data = schema.UserPathParamSchema().load({"user_id": user_id})
        except marshmallow.ValidationError as err:
            resp.media = json.dumps({"error": err.messages})
            resp.status = falcon.HTTP_400
            return

        # parse inputs - json data
        try:
            body_data = schema.UserSchema().load(req.params)
        except marshmallow.ValidationError as err:
            resp.media = json.dumps({"error": err.messages})
            resp.status = falcon.HTTP_400
            return

        # do business logic
        try:
            output = self.controller.update_user(path_data, body_data)
        except errors.ErrorWithStatus as err:
            output = {"error": str(err)}
            resp.status_code = err.status_code

        # format and return output
        resp.media = output
