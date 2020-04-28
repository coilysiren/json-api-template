import unittest

import pytest

import database.connection
import database.models as models
import server.errors as errors
import sqlalchemy
import sqlalchemy.orm as orm
from parameterized import parameterized
from server.controller import controller


class DBTransactionTestCase(unittest.TestCase):
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


class TestController(DBTransactionTestCase):
    controller = controller

    def setUp(self):
        session = super().setUp()
        self.controller.set_session(session)

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

    def test_create_user_valid_input(self):
        # setup inputs
        name = "lynn cyrin"
        # logic under test
        output = self.controller.create_user({"name": name})
        # assertions
        self.assertEqual(output["name"], name)

    def test_create_user_session_persistence(self):
        # setup inputs
        name = "lynn cyrin"
        # logic under test
        self.controller.create_user({"name": name})
        # assertions
        output = self.controller.session.query(models.User).filter_by(name=name).first()
        self.assertIsInstance(output, models.User)
        self.assertEqual(output.name, name)
