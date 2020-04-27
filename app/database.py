# [[ project layout ]]
#
# [ server viewpoint ]
#
# server
#   -> database (🗺 you are here!)
#   -> routes
#       -> views
#           -> controller
#               -> models
#
# [ migrations viewpoint ]
#
# migrations
#   -> database (🗺 you are here!)
#   -> models
#
# database.py sets up the database connection


# builtin imports
import os

# 3rd party imports
import sqlalchemy


def get_database_connection() -> sqlalchemy.engine.Engine :
    '''
    get_database_connection gets up the database connection, via a sqlalchemy engine

    docs => https://docs.sqlalchemy.org/en/13/core/engines.html
    '''
    engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))
    return engine
