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
    app.add_url_rule("/users", methods=["POST"], view_func=views.create_user)
    app.add_url_rule("/users", methods=["GET"], view_func=views.get_users)
    app.add_url_rule(
        "/users/<int:user_id>", methods=["PUT"], view_func=views.update_user
    )
    app.add_url_rule("/users/<int:user_id>", methods=["GET"], view_func=views.get_user)
    # TODO: delete
    return app
