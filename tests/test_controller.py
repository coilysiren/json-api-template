"""
tests_controller.py includes a large set of integration tests for the controller

the tests test across both the controller and the database, and generally also
test schema dumping / loading
"""

import unittest
import uuid
from copy import copy

import sqlalchemy
import sqlalchemy.orm as orm
from parameterized import parameterized

import database.connection
import database.models as models
import server.errors as errors
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


class ControllerTestCase(DBTransactionTestCase):
    controller = controller

    def setUp(self):
        session = super().setUp()
        self.controller.set_session(session)

    def _create_user(self, email="", role="standard", **kwargs):
        if email == "":
            email = str(uuid.uuid4()) + "@example.com"
        return self.controller.create_user({"email": email, "role": role, **kwargs})


class TestControllerCreateUser(ControllerTestCase):
    controller = controller

    @parameterized.expand(
        [
            ("", errors.InvalidUserInput),
            (None, errors.InvalidUserInput),
            ({}, errors.InvalidUserInput),
            ({"not_relevant": True}, errors.InvalidUserInput),
            ({"email": {}, "role": "standard"}, errors.InvalidUserInput),
            ({"name": "", "role": "standard"}, errors.InvalidUserInput),
            ({"email": True, "role": "standard"}, errors.InvalidUserInput),
            ({"email": None, "role": "standard"}, errors.InvalidUserInput),
            ({"email": 1, "role": "standard"}, errors.InvalidUserInput),
        ]
    )
    def test_create_user_bad_inputs(self, args, expected_error):
        with self.assertRaises(expected_error):
            self.controller.create_user(args)

    def test_create_user_valid_input(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        output = self._create_user(email=email)
        # testing assertions
        self.assertEqual(output["email"], email)

    def test_create_user_no_repeat_emails(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        self._create_user(email=email)
        # testing assertions
        with self.assertRaises(errors.InvalidUserInput):
            self._create_user(email=email)

    def test_create_user_session_persistence(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        self._create_user(email=email)
        # testing assertions
        output = (
            self.controller.session.query(models.User).filter_by(email=email).first()
        )
        self.assertIsInstance(output, models.User)
        self.assertEqual(output.email, email)

    def test_create_user_with_uuid_and_control_case(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        # control assertions
        output = (
            self.controller.session.query(models.User).filter_by(email=email).first()
        )
        self.assertIsNone(output)
        # logic under test
        self._create_user(email=email)
        # testing assertions
        output = (
            self.controller.session.query(models.User).filter_by(email=email).first()
        )
        self.assertIsNotNone(output)

    def test_create_then_get(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        # logic under test
        self._create_user(email=email)
        output = self.controller.get_users({})
        # testing assertions
        self.assertEqual(output["users"][0]["email"], email)

    def test_create_bad_role(self):
        with self.assertRaises(errors.InvalidUserInput):
            self._create_user(role="BAD ROLE")


class TestControllerGetUsers(ControllerTestCase):
    controller = controller

    @parameterized.expand(
        [
            ("", errors.InvalidUserInput),
            (None, errors.InvalidUserInput),
            ({"limit": True}, errors.InvalidUserInput),
            ({"limit": None}, errors.InvalidUserInput),
        ]
    )
    def test_get_user_bad_inputs(self, args, expected_error):
        with self.assertRaises(expected_error):
            self.controller.get_users(args)

    def test_get_multiple(self):
        # setup
        count = 3
        for _ in range(count):
            self._create_user()
        # logic under test
        output = self.controller.get_users({})
        # testing assertions
        self.assertEqual(len(output["users"]), count)

    def test_get_one_result(self):
        # setup
        count = 3
        for _ in range(count):
            self._create_user()
        # logic under test
        output = self.controller.get_users({"limit": 1})
        # testing assertions
        self.assertEqual(len(output["users"]), 1)

    def test_get_user_by_role(self):
        # setup
        self._create_user(role="admin")
        # logic under test
        output = self.controller.get_users({"roles": ["admin"]})
        # testing assertions
        self.assertEqual(len(output["users"]), 1)

    def test_get_user_by_role_select_one(self):
        # setup
        self._create_user(role="admin")
        self._create_user(role="standard")
        # logic under test
        output = self.controller.get_users({"roles": ["standard"]})
        # testing assertions
        self.assertEqual(len(output["users"]), 1)

    def test_get_user_by_role_select_empty(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_users({"roles": [""]})

    def test_get_user_by_role_select_bad_role(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_users({"roles": ["BAD ROLE"]})

    def test_get_user_by_role_no_preference(self):
        # setup
        self._create_user(role="admin")
        self._create_user(role="standard")
        # logic under test
        output = self.controller.get_users({})
        # testing assertions
        self.assertEqual(len(output["users"]), 2)

    def test_get_user_by_role_select_neither(self):
        # setup
        self._create_user(role="admin")
        self._create_user(role="admin")
        # logic under test
        with self.assertRaises(errors.NotFound):
            self.controller.get_users({"roles": ["standard"]})

    def test_get_user_by_role_select_all(self):
        # setup
        self._create_user(role="admin")
        self._create_user(role="standard")
        # logic under test
        output = self.controller.get_users({"roles": ["admin", "standard"]})
        # testing assertions
        self.assertEqual(len(output["users"]), 2)

    def test_get_limit_too_large(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_users({"limit": 9999999999999999999})

    def test_get_pagination(self):
        # setup
        self._create_user()
        self._create_user()
        # logic under test
        output_one = self.controller.get_users({"limit": 1, "page": 1})
        output_two = self.controller.get_users({"limit": 1, "page": 2})
        # testing assertions
        self.assertNotEqual(output_one["users"][0]["id"], output_two["users"][0]["id"])

    def test_clipped_pagination(self):
        # setup
        count = 5
        for _ in range(count):
            self._create_user()
        # logic under test
        output_one = self.controller.get_users({"limit": count - 1, "page": 2})
        # testing assertions
        # 2nd page should have 1 user
        self.assertEqual(len(output_one["users"]), 1)

    def test_page_two_of_three(self):
        # setup
        count = 9
        for _ in range(count):
            self._create_user()
        # logic under test
        output_one = self.controller.get_users({"limit": 3, "page": 2})
        # testing assertions
        self.assertEqual(len(output_one["users"]), 3)

    def test_page_past_max_max(self):
        self._create_user()
        with self.assertRaises(errors.NotFound):
            self.controller.get_users({"page": 9999999999})


class TestControllerGetUser(ControllerTestCase):
    controller = controller

    def test_get_not_found(self):
        with self.assertRaises(errors.NotFound):
            self.controller.get_user({"user_id": 1337})

    def test_get_not_found_very_big_number(self):
        with self.assertRaises(errors.NotFound):
            self.controller.get_user(
                {"user_id": 9999999999999999999999999999999999999999999999999999999}
            )

    def test_get_bad_input_infinity(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_user({"user_id": float("inf")})

    def test_get_bad_input_negative(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_user({"user_id": -1})

    def test_get_bad_input(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_user({"user_id": "BAD INPUT"})

    def test_get_bad_input_cat(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.get_user({"user_id": "🐈"})

    def test_get_one_user(self):
        # setup
        count = 5
        create_output = {}
        for i in range(count):
            if i == 2:
                create_output = self._create_user()
        # logic under test
        get_output = self.controller.get_user({"user_id": create_output["id"]})
        # testing assertions
        self.assertTrue(get_output)
        self.assertEqual(get_output["id"], create_output["id"])


class TestControllerUpdateUsers(ControllerTestCase):
    controller = controller

    def test_update_user_with_name_change(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        old_name = "luna cyrin"
        create_user_output = self._create_user(email=email, givenName=old_name)

        # control assertions
        self.assertEqual(create_user_output["givenName"], old_name)

        # logic under test
        new_name = "luna faye"
        _id = create_user_output["id"]
        update_user_input = copy(create_user_output)
        update_user_input.update(givenName=new_name)
        new_output = self.controller.update_user({"user_id": _id}, update_user_input)

        # testing assertions
        self.assertEqual(new_output["givenName"], new_name)
        self.assertEqual(new_output["id"], _id)

    def test_update_user_does_not_create_new(self):
        # setup part 1
        email = str(uuid.uuid4()) + "@example.com"
        old_name = "luna cyrin"
        create_user_output = self._create_user(email=email, givenName=old_name)
        # setup part 2
        new_name = "luna faye"
        _id = create_user_output["id"]
        update_user_input = copy(create_user_output)
        update_user_input.update(givenName=new_name)

        # logic under test
        self.controller.update_user({"user_id": _id}, update_user_input)

        # testing assertions
        output = self.controller.get_users({})
        self.assertEqual(len(output["users"]), 1)

    def test_update_user_rejects_bad_json_input(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        old_name = "luna cyrin"
        create_user_output = self._create_user(email=email, givenName=old_name)

        # control assertions
        self.assertEqual(create_user_output["givenName"], old_name)

        # logic under test
        new_name = 100
        _id = create_user_output["id"]
        update_user_input = copy(create_user_output)
        update_user_input.update(givenName=new_name)
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.update_user({"user_id": _id}, update_user_input)

        # testing assertions
        output = (
            self.controller.session.query(models.User)
            .filter_by(givenName=old_name)
            .first()
        )
        self.assertIsNotNone(output)

    def test_update_does_not_unset_fields(self):
        # setup
        email = str(uuid.uuid4()) + "@example.com"
        old_name = "luna cyrin"
        create_user_output = self._create_user(email=email, givenName=old_name)

        # control assertions
        self.assertEqual(create_user_output["givenName"], old_name)

        # logic under test
        _id = create_user_output["id"]
        new_output = self.controller.update_user({"user_id": _id}, {}) # <= empty update data

        # testing assertions
        # assert nothing has changed!
        self.assertEqual(create_user_output["givenName"], new_output["givenName"])
        self.assertEqual(create_user_output["givenName"], new_output["givenName"])
        self.assertEqual(create_user_output["email"], new_output["email"])
        self.assertEqual(create_user_output["role"], new_output["role"])
        self.assertEqual(create_user_output["id"], new_output["id"])
        self.assertEqual(create_user_output["smsUser"], new_output["smsUser"])

    def test_update_user_rejects_bad_path_param(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.update_user("BAD USER ID", {})

    def test_update_user_not_found(self):
        with self.assertRaises(errors.NotFound):
            self.controller.update_user(
                {"user_id": 1337}, {"email": "lynn@example.com", "role": "admin"}
            )

    def test_update_bad_role(self):
        with self.assertRaises(errors.InvalidUserInput):
            self.controller.update_user(
                {"user_id": 1337}, {"email": "lynn@example.com", "role": "BAD ROLE"}
            )
