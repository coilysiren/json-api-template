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

import database.connection
import database.models as models
import marshmallow
import server.errors as errors
import server.schema as schema
import sqlalchemy.orm as orm
from server.decider import Decider


class __Controller(object):
    session: orm.Session

    def set_session(self, session):
        """
        set_session is used to attach an active database session to the controller
        the controller uses the database session later, to do all of its work
        """
        self.session = session

    def create_user(self, data) -> {}:
        # parse inputs (json data)
        try:
            userData = schema.UserInputSchema().load(data)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic - part 1 (eg. check that there isnt a user with this email)
        user = (
            self.session.query(models.User).filter_by(email=userData["email"]).first()
        )
        if user is not None:
            raise errors.InvalidUserInput(
                "a user already exists with this email address"
            )

        # do business logic - part 2 (eg. create the user)
        user = models.User()
        user = schema.UserInputSchema.update_user(user, userData)
        self.session.add(user)
        self.session.commit()

        # return our created user
        output = schema.UserOutputSchema().load(user)
        return output

    def get_users(self, data) -> {}:
        # parse inputs (query params)
        try:
            queryData = schema.UserQuerySchema().load(data)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic (eg. get users)
        offset = (queryData["page"] - 1) * queryData["limit"]
        query = self.session.query(models.User).limit(queryData["limit"]).offset(offset)
        if query.count() == 0:
            raise errors.NotFound(f"found no users for query input")

        # return query results
        output = schema.UserOutputSchema(many=True).load(query)
        return {"users": output}

    def get_user(self, user_id) -> {}:
        # parse inputs (path params)
        try:
            user_id = schema.UserPathSchema().load({"user_id": user_id})["user_id"]
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic (eg. find a user)
        user = self.session.query(models.User).filter_by(id=user_id).first()
        if user is None:
            raise errors.NotFound("a user with the given id could not be found")

        # return our found user
        output = schema.UserOutputSchema().load(user)
        return output

    def update_user(self, user_id, data) -> {}:
        # parse inputs - part 1 (path params)
        try:
            user_id = schema.UserPathSchema().load({"user_id": user_id})["user_id"]
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # parse inputs - part 2 (json data)
        try:
            userData = schema.UserInputSchema().load(data)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic - part 1 (eg. find the user to update)
        user = self.session.query(models.User).filter_by(id=user_id).first()
        if user is None:
            raise errors.NotFound("a user with the given user_id could not be found")

        # do business logic - part 2 (eg. update the user)
        user = models.User()
        user = schema.UserInputSchema.update_user(user, userData)
        self.session.add(user)
        self.session.commit()

        # return our updated user
        output = schema.UserOutputSchema().load(user)
        return output


# controller singleton, explained briefly above
controller = __Controller()
