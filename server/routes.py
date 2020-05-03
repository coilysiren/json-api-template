"""
routes.py attaches the views to the routes. It is invoked during server configuration
(eg at server startup time)
"""

import flask

from server.views import Views


def setup_routes(app: flask.Flask, views: Views) -> flask.Flask:
    """
    setup_routes attaches our views to our routes

    docs => https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
    """
    app.route("/users", methods=["POST"])(views.create_user)
    app.route("/users", methods=["GET"])(views.get_users)
    app.route("/users/<int:user_id>", methods=["PUT"])(views.update_user)
    app.route("/users/<int:user_id>", methods=["GET"])(views.get_user)
    # TODO: delete
    return app
