# isort: 3rd party imports
import pytest
import sqlalchemy.orm as orm

# isort: our imports
from server.controller import controller


@pytest.fixture(scope="function")
def session(connection):
    transaction = connection.begin()
    session = orm.Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()


def test_create_user(session):
    output = controller.create_user("")
    assert output is not {}
