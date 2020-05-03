"""
app.py sets up the server configuration, and attaches the views to the routes.
It is meant to be run as an entrypoint script, and should fail if there are any
obvious fatal configuration issues.
"""

import dotenv
import flask

import database.connection
import server.routes as routes
from server.controller import Controller
from server.views import Views


def create_app() -> flask.Flask:
    """
    create_app creates the flask application

    docs => https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    """
    # environment variables
    dotenv.load_dotenv()

    # flask setup
    app = flask.Flask(__name__)

    # database setup
    session = database.connection.get_database_session()

    # controller setup
    controller = Controller(session=session)

    # views setup
    views = Views(controller=controller)

    # routes setup
    app = routes.setup_routes(app, views)

    return app
