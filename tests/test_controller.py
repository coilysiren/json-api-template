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

    def create_user(self, name=""):
        if name == "":
            name = str(uuid.uuid4())
        user = models.User(name=name)
        self.controller.session.add(user)
        self.controller.session.commit()

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
        name = "lynn cyrin"
        # logic under test
        output = self.controller.create_user({"name": name})
        # assertions
        self.assertEqual(output["name"], name)

    def test_create_user_session_persistence(self):
        # setup inputs
        name = "luna faye"
        # logic under test
        self.controller.create_user({"name": name})
        # assertions
        query = self.controller.session.query(models.User).filter_by(name=name).first()
        self.assertIsInstance(query, models.User)
        self.assertEqual(query.name, name)

    def test_create_user_with_uuid_and_control_case(self):
        # control case
        name = str(uuid.uuid4())
        query = self.controller.session.query(models.User).filter_by(name=name).first()
        self.assertIsNone(query)
        # logic under test
        self.controller.create_user({"name": name})
        # test case
        query = self.controller.session.query(models.User).filter_by(name=name).first()
        self.assertIsNotNone(query)

    def test_create_then_get(self):
        # setup inputs
        name = str(uuid.uuid4())
        # logic under test
        self.controller.create_user({"name": name})
        output = self.controller.get_users({"name": name})
        # test case
        self.assertEqual(output["users"][0]["name"], name)

    def test_get_multiple(self):
        # logic under test
        self.controller.create_user({"name": str(uuid.uuid4())})
        self.controller.create_user({"name": str(uuid.uuid4())})
        self.controller.create_user({"name": str(uuid.uuid4())})
        output = self.controller.get_users({})
        # test case
        self.assertEqual(len(output["users"]), 3)
