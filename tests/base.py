import unittest
import uuid

import database.connection
import sqlalchemy
import sqlalchemy.orm as orm


class TransactionTestingBaseClass(unittest.TestCase):
    connection: sqlalchemy.engine.Engine
    session: orm.Session
    transaction: sqlalchemy.engine.Transaction

    @classmethod
    def setUpClass(cls):
        engine = database.connection.get_database_connection()
        cls.connection = engine.connect()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        self.session = orm.Session(bind=self.connection)
        self.transaction = self.connection.begin()
        return self.session

    def tearDown(self):
        self.transaction.rollback()
        self.session.close()
