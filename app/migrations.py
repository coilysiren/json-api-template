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
# that should be run directly in your terminal.


# 3rd party imports
import alembic

# local imports
import .database
import .models


def run_migrations():
    '''
    run_migations runs "online" migrations via alembic

    docs => https://alembic.sqlalchemy.org/en/latest/tutorial.html
    '''
    # grab database engine
    engine = database.get_database_connection()

    # with an active connection
    with engine.connect() as connection:
        # configure alembic
        alembic.context.configure(
            connection=connection,
            target_metadata=models.Base.metadata,
        )
        # and open a transaction to run migrations
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


if __name__ == "__main__":
    run_migrations()
