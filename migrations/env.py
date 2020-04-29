# migrations/env.py runs the database migrations. It is designed as an entrypoint script
# that is run by alembic.


import alembic.context

import database.connection
import database.models


def run_migrations():
    """
    run_migations runs "online" migrations via alembic

    docs => https://alembic.sqlalchemy.org/en/latest/tutorial.html
    """
    # grab database engine
    engine = database.connection.get_database_connection()

    # with an active connection
    with engine.connect() as connection:
        # configure alembic
        alembic.context.configure(
            connection=connection, target_metadata=database.models.Base.metadata,
        )
        # and open a transaction to run migrations
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


# only alembic should import this file
# because this next line is responsible for running migrations
run_migrations()
