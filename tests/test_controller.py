import unittest

import pytest

import database.connection
import sqlalchemy
import sqlalchemy.orm as orm
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

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_create_user(self):
        output = controller.create_user("")
        assert output is not {}

    def test_create_user_two(self):
        output = controller.create_user("")
        assert output is {}
