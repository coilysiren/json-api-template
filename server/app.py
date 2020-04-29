"""
app.py sets up the server configuration, and attaches the views to the routes.
It is meant to be run as an entrypoint script, and should fail if there are any
obvious fatal configuration issues.
"""

import dotenv
import flask

import database.connection
import server.routes
from server.controller import controller


def create_app() -> flask.Flask:
    """
    create_app creates the flask application

    docs => https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    """
    # environment variables
    dotenv.load_dotenv()

    # flask configuration
    app = flask.Flask(__name__)
    app = server.routes.setup_routes(app)

    # database configuration
    controller.set_session(database.connection.get_database_session())

    return app
