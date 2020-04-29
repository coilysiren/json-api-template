import unittest
import uuid

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

    def _create_user(self, email="", role="standard"):
        if email == "":
            email = str(uuid.uuid4()) + "@example.com"
        return self.controller.create_user({"email": email, "role": role})

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

    @parameterized.expand(
        [
            ("", errors.InvalidUserInput),
            (None, errors.InvalidUserInput),
            ({"name": True}, errors.InvalidUserInput),
            ({"name": None}, errors.InvalidUserInput),
            ({"name": 1}, errors.InvalidUserInput),
        ]
    )
    def test_get_user_bad_inputs(self, args, expectedError):
        with self.assertRaises(expectedError):
            self.controller.get_users(args)

    def test_create_user_valid_input(self):
        # setup inputs
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        output = self._create_user(email=email)
        # assertions
        self.assertEqual(output["email"], email)

    def test_create_user_session_persistence(self):
        # setup inputs
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        self._create_user(email=email)
        # assertions
        output = (
            self.controller.session.query(models.User).filter_by(email=email).first()
        )
        self.assertIsInstance(output, models.User)
        self.assertEqual(output.email, email)

    def test_create_user_with_uuid_and_control_case(self):
        # setup inputs
        email = str(uuid.uuid4()) + "@example.com"
        # control case
        output = (
            self.controller.session.query(models.User).filter_by(email=email).first()
        )
        self.assertIsNone(output)
        # logic under test
        self._create_user(email=email)
        # test case
        output = (
            self.controller.session.query(models.User).filter_by(email=email).first()
        )
        self.assertIsNotNone(output)

    def test_create_then_get(self):
        # setup inputs
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        self._create_user(email=email)
        output = self.controller.get_users({})
        # test case
        self.assertEqual(output["users"][0]["email"], email)

    def test_get_multiple(self):
        # setup
        count = 3
        for _ in range(count):
            self._create_user()
        # logic under test
        output = self.controller.get_users({})
        # test case
        self.assertEqual(len(output["users"]), count)
