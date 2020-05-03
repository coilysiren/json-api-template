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
    for method, rule, view in [
        ("POST", "/users", views.create_user),
        ("GET", "/users", views.get_users),
        ("PUT", "/users/<int:user_id>", views.update_user),
        ("GET", "/users/<int:user_id>", views.get_user),
        # TODO: delete
    ]:
        app.add_url_rule(rule, methods=[method], view_func=view)
    return app
