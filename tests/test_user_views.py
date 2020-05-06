"""
tests_controller.py includes a large set of integration tests for the controller

This heavy-weight set of integration tests is inspired by the body of thought
described here: https://kentcdodds.com/blog/write-tests.

In short:
- Write tests
- Not too many
- Mostly integration.
"""

from tests.base import TestClient


# disable "too few public methods" warning, since this is placeholder code
# pylint: disable=R0903


class UserTestClient(TestClient):
    pass


class TestCreateUser(UserTestClient):
    def test_placeholder(self):
        return self
