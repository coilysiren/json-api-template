import database.connection
import database.models as models
import server.errors as errors
import sqlalchemy.orm as orm
from server.decider import Decider


class __Controller(object):
    session: orm.Session

    def set_session(self, session):
        self.session = session

    def create_user(self, data) -> {}:
        # parse inputs
        if not hasattr(data, "get"):
            raise errors.InvalidUserInput("json input was invalid")

        # parse inputs (part 2)
        name = data.get("name", "")
        if not isinstance(name, str):
            raise errors.InvalidUserInput("`name` had invalid type")

        # parse inputs (part 3)
        if name == "":
            raise errors.InvalidUserInput("`name` was empty")

        # do business logic
        user = models.User(name=name)
        self.session.add(user)
        self.session.commit()
        output = user.data

        return output

    def get_users(self, data) -> {}:
        # parse inputs
        if not hasattr(data, "get"):
            raise errors.InvalidUserInput("json input was invalid")

        # parse inputs (part 2)
        name = data.get("name", "")
        if name != "" and not isinstance(name, str):
            raise errors.InvalidUserInput("`name` had invalid type")

        # do business logic (eg. the get query)
        if name == "":
            query = self.session.query(models.User).all()
        else:
            query = self.session.query(models.User).filter_by(name=name)

        # process output
        output = {"users": []}
        for user in query:
            output["users"].append(user.data)

        return output


controller = __Controller()
