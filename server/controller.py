"""
controller.py is responsible for a variety of things:
    - input validation
    - session querying
    - session saving
    - all other business logic

It utilized via importing the `controller` singleton, rather than
importing the __Controller class directly (hence the underscores).

The vast majority of our code logic lives in the controller, so all our tests
revolve around testing the controller.

The controller keeps 1 thing in its state: the current database session.
The session is passed into the controller when the application is starting up.
"""
import sys

import marshmallow
import sqlalchemy.orm as orm

import database.models as models
import server.errors as errors
import server.schema as schema


# disable the warning about the underscores in our class name
# pylint: disable=C0103


class __Controller:
    session: orm.Session

    def set_session(self, session):
        """
        set_session is used to attach an active database session to the controller
        the controller uses the database session later, to do all of its work
        """
        self.session = session

    def create_user(self, post_body) -> dict:
        # parse inputs (json data)
        try:
            post_data = schema.UserPostCreateSchema().load(post_body)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - part 1 (check that there isnt a user with this email)
        #
        # NOTE! I'm assuming here that we don't want users with duplicate emails.
        #
        # In a work environment, I would check in with the person who is creating
        # requirements to see if that is an accurate assumption.
        existing_user = (
            self.session.query(models.User).filter_by(email=post_data["email"]).first()
        )
        if existing_user is not None:
            raise errors.InvalidUserInput(
                "a user already exists with this email address"
            )

        # business logic - part 2 (create the user)
        user = models.User()
        user = update_user(user, post_data)
        self.session.add(user)
        self.session.commit()

        # return our created user
        output = schema.UserPostCreateSchema().dump(user)
        return output

    def get_users(self, query_params) -> dict:
        # parse inputs (query params)
        try:
            query_data = schema.UserQueryParamSchema().load(query_params)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - part 1 (get users)
        query = self.session.query(models.User)

        # business logic - part 2 (filter by role)
        if len(query_data["roles"]) != 0:
            query = query.filter(models.User.role.in_(query_data["roles"]))

        # business logic - part 3 (pagination)
        offset = (query_data["page"] - 1) * query_data["limit"]
        query = query.limit(query_data["limit"]).offset(offset)

        # business logic - part 4 (bounds checking)
        if query.count() == 0:
            raise errors.NotFound("found no users for query input")

        # return query results
        output = schema.BaseUserPostSchema(many=True).dump(query)
        return {"users": output}

    def get_user(self, path_params: dict) -> dict:
        # parse inputs (path params)
        try:
            path_data = schema.UserPathParamSchema().load(path_params)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic (find a user)
        user = (
            self.session.query(models.User).filter_by(id=path_data["user_id"]).first()
        )
        if user is None:
            raise errors.NotFound("a user with the given id could not be found")

        # return our found user
        output = schema.BaseUserPostSchema().dump(user)
        return output

    def update_user(self, path_params: dict, post_body: dict) -> dict:
        # parse inputs - part 1 (path params)
        try:
            path_data = schema.UserPathParamSchema().load(path_params)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # parse inputs - part 2 (json data)
        try:
            post_data = schema.UserPostUpdateSchema().load(post_body)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - part 1 (find the user to update)
        user = (
            self.session.query(models.User).filter_by(id=path_data["user_id"]).first()
        )
        if user is None:
            raise errors.NotFound("a user with the given user_id could not be found")

        # business logic - part 2 (update the user)
        user = update_user(user, post_data)
        self.session.add(user)
        self.session.commit()

        # return our updated user
        output = schema.BaseUserPostSchema().dump(user)
        return output


def update_user(user: models.User, data: dict) -> models.User:
    """
    update_user takes in a user and schema data, and updates
    that user with the schema data

    Its vaguely unclear where this function truly belongs!
    I thoroughly encourage moving it.
    """

    # It would be nice if this was something like
    # `data.fields.email.value` instead! Need to check if the
    # marshmallow API supports that.
    if data.get("email") is not None:
        user.email = data.get("email")

    if data.get("role") is not None:
        user.role = data.get("role")

    if data.get("familyName") is not None:
        user.familyName = data.get("familyName")

    if data.get("givenName") is not None:
        user.givenName = data.get("givenName")

    if data.get("smsUser") is not None:
        user.smsUser = data.get("smsUser")

    return user


# controller singleton, explained briefly above
controller = __Controller()
