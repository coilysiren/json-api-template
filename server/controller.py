# isort: 3rd party imports
import sqlalchemy.orm as orm

# isort: our imports
import database.connection
from database.models import User
from server.decider import Decider


class __Controller(object):
    session: orm.Session = None

    def set_session(self, session):
        self.session = session

    def create_user(self, data) -> {}:
        output = {}
        return output

    def get_users(self, data) -> {}:
        output = {}
        return output


controller = __Controller()