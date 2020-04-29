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
        # parse inputs
        try:
            userInput = schema.UserInputSchema().load(data)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic (eg. create a user)
        user = models.User()
        user = userInput.update_user(user)
        self.session.add(user)
        self.session.commit()

        # return our created user
        output = schema.UserOutputSchema().load(user)
        return output

    def get_users(self, data) -> {}:
        # parse inputs
        try:
            userQuery = schema.UserQuerySchema().load(data)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic (eg. get users)
        query = self.session.query(models.User).all()

        # return query results
        output = schema.UserOutputSchema(many=True).load(query)
        return output

    def get_user(self, user_id) -> {}:
        # parse inputs
        if user_id == "":
            raise errors.InvalidUserInput("the `user_id` was empty")

        # do business logic (eg. find a user)
        user = self.session.query(models.User).filter_by(id=user_id).first()
        if user is None:
            raise errors.NotFound("a user with the given id could not be found")

        # return our found user
        output = schema.UserOutputSchema().load(user)
        return output

    def update_user(self, user_id, data) -> {}:
        # parse inputs (part 1)
        if user_id == "":
            raise errors.InvalidUserInput("the `user_id` was empty")
        # parse inputs (part 2)
        try:
            userInput = schema.UserInputSchema().load(data)
        except marshmallow.ValidationError as err:
            raise errors.InvalidUserInput(err.messages)

        # do business logic - part 1 (eg. find the user to update)
        user = self.session.query(models.User).filter_by(id=user_id).first()
        if user is None:
            raise errors.NotFound("a user with the given id could not be found")

        # do business logic - part 2 (eg. update the user)
        user = models.User()
        user = userInput.update_user(user)
        self.session.add(user)
        self.session.commit()

        # return our updated user
        output = schema.UserOutputSchema().load(user)
        return output


controller = __Controller()
