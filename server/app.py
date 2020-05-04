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


def create_app() -> falcon.API:
    # environment variables
    dotenv.load_dotenv()

    # falcon setup (no dependencies)
    app = falcon.API()

    # database setup (no dependencies)
    session = database.connection.get_database_session()

    # view + controller setup (requires the database session)
    user_controller = UserController(session=session)
    user_views = UserViews(controller=user_controller)

    # routes setup (requires the app and the views)
    app.add_route("/users", user_views, suffix="users")
    app.add_route("/users/{user_id}", user_views, suffix="user")

    return app
