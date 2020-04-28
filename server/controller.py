import database.connection
import server.errors as errors
import sqlalchemy.orm as orm
from database.models import User
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
        name = data.get("name")
        if not isinstance(name, str):
            raise errors.InvalidUserInput("`name` had invalid type")

        # parse inputs (part 3)
        if name == "":
            raise errors.InvalidUserInput("`name` was empty")

        print(f"name is {name}")

        # initalize outputs
        output = {}

        return output

    def get_users(self, data) -> {}:
        # initalize outputs
        output = {}

        return output


controller = __Controller()
