# [[ project layout ]]
#
# [ server viewpoint ]
#
# server
#   -> database
#   -> routes
#       -> views
#           -> controller
#               -> models
#
# [ migrations viewpoint ]
#
# migrations (🗺 you are here!)
#   -> database
#   -> models
#
# migrations.py runs the database migrations. It is designed as an entrypoint script
# that is run by alembic.


# 3rd party imports
import alembic.context

# local imports
import app.database
import app.models


def run_migrations():
    """
    run_migations runs "online" migrations via alembic

    docs => https://alembic.sqlalchemy.org/en/latest/tutorial.html
    """
    # grab database engine
    engine = app.database.get_database_connection()

    # with an active connection
    with engine.connect() as connection:
        # configure alembic
        alembic.context.configure(
            connection=connection, target_metadata=app.models.Base.metadata,
        )
        # and open a transaction to run migrations
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


run_migrations()
