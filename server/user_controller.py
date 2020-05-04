"""
controller.py is responsible for a variety of things:
    - input validation
    - session querying
    - session saving
    - all other business logic

The controller keeps 1 thing in its state: the current database session.
The session is passed into the controller when the application is starting up.
"""

import sqlalchemy.orm as orm

import database.models as models
import server.errors as errors
import server.schema as schema


class UserController:
    session: orm.Session

    def __init__(self, session: orm.Session):
        self.session = session

    def create_user(self, data) -> dict:
        # check that there isnt a user with this email
        existing_user = (
            self.session.query(models.User).filter_by(email=data["email"]).first()
        )
        if existing_user is not None:
            raise errors.InvalidUserInput(
                "a user already exists with this email address"
            )

        # create the user
        user = models.User()
        user = user.update(data)
        self.session.add(user)
        self.session.commit()

        # return our created user
        output = schema.UserSchema().dump(user)
        return output

    def get_users(self, data) -> dict:
        # get users
        query = self.session.query(models.User)

        # businesss logic - sorting
        if data["sort_by"] != "":
            column = getattr(models.User, data["sort_by"])
            if data["order"] == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
        else:
            query = query.order_by(models.User.createTime.desc())

        # pagination
        offset = (data["page"] - 1) * data["limit"]
        query = query.limit(data["limit"]).offset(offset)

        # bounds checking
        if query.count() == 0:
            raise errors.NotFound("found no users for query input")

        # return query results
        results = schema.UserSchema(many=True).dump(query)
        output = {"users": results}
        return output

    def get_user(self, data: dict) -> dict:
        # find a user
        user = (
            self.session.query(models.User).filter_by(user_id=data["user_id"]).first()
        )
        if user is None:
            raise errors.NotFound("a user with the given user_id could not be found")

        # return our found user
        output = schema.UserSchema().dump(user)
        return output

    def update_user(self, path_data: dict, body_data: dict) -> dict:
        # find the user to update
        user = (
            self.session.query(models.User)
            .filter_by(user_id=path_data["user_id"])
            .first()
        )
        if user is None:
            raise errors.NotFound("a user with the given user_id could not be found")

        # update the user
        user = user.update(body_data)
        self.session.add(user)
        self.session.commit()

        # return our updated user
        output = schema.UserSchema().dump(user)
        return output
