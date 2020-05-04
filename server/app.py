"""
app.py sets up the server configuration, and attaches the views to the routes.
It is meant to be run as an entrypoint script, and should fail if there are any
obvious fatal configuration issues.
"""

import dotenv
import falcon

import database.connection
from server.user_controller import UserController
from server.user_views import UserViews
import server.routes


def create_app() -> falcon.App:
    # environment variables
    dotenv.load_dotenv()

    # falcon setup (no dependencies)
    app = falcon.App()

    # database setup (no dependencies)
    session = database.connection.get_database_session()

    # view + controller setup (requires the database session)
    user_controller = UserController(session=session)
    user_views = UserViews(controller=user_controller)

    # routes setup (requires the app and the views)
    server.routes.setup_routes(app, user_views)

    return app
