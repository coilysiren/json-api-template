import unittest

import pytest

import database.connection
import server.errors as errors
import sqlalchemy
import sqlalchemy.orm as orm
from parameterized import parameterized
from server.controller import controller


class TestController(unittest.TestCase):
    connection: sqlalchemy.engine.Engine
    session: orm.Session
    transaction: sqlalchemy.engine.Transaction
    controller = controller

    @classmethod
    def setUpClass(cls):
        engine = database.connection.get_database_connection()
        cls.connection = engine.connect()
        cls.session = orm.Session(bind=cls.connection)
        cls.controller.set_session(cls.session)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        cls.session.close()

    def setUp(self):
        self.transaction = self.connection.begin()

    def tearDown(self):
        self.transaction.rollback()

    @parameterized.expand(
        [
            ("", errors.InvalidUserInput),
            (None, errors.InvalidUserInput),
            ({}, errors.InvalidUserInput),
            ({"not_relevant": True}, errors.InvalidUserInput),
            ({"name": {}}, errors.InvalidUserInput),
            ({"name": ""}, errors.InvalidUserInput),
            ({"name": True}, errors.InvalidUserInput),
            ({"name": None}, errors.InvalidUserInput),
            ({"name": 1}, errors.InvalidUserInput),
        ]
    )
    def test_create_user_bad_inputs(self, args, expectedError):
        with self.assertRaises(expectedError):
            self.controller.create_user(args)
