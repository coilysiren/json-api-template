import database.connection
import sqlalchemy.orm as orm
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
