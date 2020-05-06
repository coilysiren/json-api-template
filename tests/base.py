import unittest

import falcon
import sqlalchemy
import sqlalchemy.orm as orm

import database.connection
import server.app


class TestClient(unittest.TestCase):
    # falcon testing client, used by subclasses
    client: falcon.testing.TestClient

    # database transaction state, used internally
    _connection: sqlalchemy.engine.Engine
    _session: orm.Session
    _transaction: sqlalchemy.engine.Transaction

    @classmethod
    def setUpClass(cls):
        # database transaction setup
        # docs => https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
        engine = database.connection.get_database_connection()
        cls._connection = engine.connect()
        cls._session = orm.Session(bind=cls._connection)

        # falcon testing client setup
        # docs => https://falcon.readthedocs.io/en/stable/api/testing.html
        app = server.app.create_app(cls._session)
        cls.app = falcon.testing.TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls._connection.close()
        cls._session.close()

    def setUp(self):
        self._transaction = self._connection.begin()

    def tearDown(self):
        self._transaction.rollback()
