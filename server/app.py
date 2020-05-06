"""
app.py sets up the server configuration, and attaches the views to the routes.
It is meant to be run as an entrypoint script, and should fail if there are any
obvious fatal configuration issues.
"""

import dotenv
import falcon

import database.connection
import server.routes
from server.user_controller import UserController
from server.user_views import UserViews


def create_app(database_session=None) -> falcon.App:
    # environment variables
    dotenv.load_dotenv()

    # falcon setup (no dependencies)
    app = falcon.App()

    # database setup (no dependencies)
    # the `database_session` arg is passed in during tests
    if database_session is None:
        database_session = database.connection.get_database_session()

    # view + controller setup (requires the database session)
    user_controller = UserController(session=database_session)
    user_views = UserViews(controller=user_controller)

    # routes setup (requires the app and the views)
    server.routes.setup_routes(app, user_views)

    return app
