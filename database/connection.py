# database.py sets up the database connection state


import os

import sqlalchemy
import sqlalchemy.orm as orm


def get_database_connection() -> sqlalchemy.engine.Engine:
    """
    get_database_connection sets up the database connection, via a sqlalchemy engine

    docs => https://docs.sqlalchemy.org/en/13/core/engines.html
    """
    return sqlalchemy.create_engine(os.getenv("DATABASE_URL"))


def get_database_session() -> orm.Session:
    """
    get_database_session uses the sqlachemy engine to setup a database session

    docs => https://docs.sqlalchemy.org/en/13/orm/tutorial.html
    """
    return orm.sessionmaker(bind=get_database_connection())
