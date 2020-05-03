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
import marshmallow
import sqlalchemy
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
        set_session is used to attach an active database session to the controller.
        The controller uses the database session later, to do most of its work.
        """
        self.session = session

    def create_user(self, post_body) -> dict:
        # parse inputs - json data
        try:
            post_data = schema.UserSchema().load(post_body)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - check that there isnt a user with this email
        existing_user = (
            self.session.query(models.User).filter_by(email=post_data["email"]).first()
        )
        if existing_user is not None:
            raise errors.InvalidUserInput(
                "a user already exists with this email address"
            )

        # business logic - create the user
        user = models.User()
        user = update_user(user, post_data)
        self.session.add(user)
        self.session.commit()

        # return our created user
        output = schema.UserSchema().dump(user)
        return output

    def get_users(self, query_params) -> dict:
        # parse inputs - query params
        try:
            query_data = schema.UserQueryParamSchema().load(query_params)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - get users
        query = self.session.query(models.User)

        # businesss logic - sorting
        if query_data["sort_by"] != "":
            column = getattr(models.User, query_data["sort_by"])
            if query_data["order"] == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
        else:
            query = query.order_by(models.User.createTime.desc())

        # business logic - pagination
        offset = (query_data["page"] - 1) * query_data["limit"]
        query = query.limit(query_data["limit"]).offset(offset)

        # business logic - bounds checking
        if query.count() == 0:
            raise errors.NotFound("found no users for query input")

        # return query results
        output = schema.UserSchema(many=True).dump(query)
        return {"users": output}

    def get_user(self, path_params: dict) -> dict:
        # parse inputs - path params
        try:
            path_data = schema.UserPathParamSchema().load(path_params)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - find a user
        user = (
            self.session.query(models.User)
            .filter_by(user_id=path_data["user_id"])
            .first()
        )
        if user is None:
            raise errors.NotFound("a user with the given user_id could not be found")

        # return our found user
        output = schema.UserSchema().dump(user)
        return output

    def update_user(self, path_params: dict, post_body: dict) -> dict:
        # parse inputs - path params
        try:
            path_data = schema.UserPathParamSchema().load(path_params)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # parse inputs - json data
        try:
            post_data = schema.UserSchema().load(post_body)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # business logic - find the user to update
        user = (
            self.session.query(models.User)
            .filter_by(user_id=path_data["user_id"])
            .first()
        )
        if user is None:
            raise errors.NotFound("a user with the given user_id could not be found")

        # business logic - update the user
        user = update_user(user, post_data)
        self.session.add(user)
        self.session.commit()

        # return our updated user
        output = schema.UserSchema().dump(user)
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

    if data.get("name") is not None:
        user.name = data.get("name")

    return user


# controller singleton, explained briefly at the top of the file
# TODO: remove the need for this singleton
# TODO: remove usage of global state
controller = __Controller()
