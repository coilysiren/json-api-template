import falcon

from server.user_views import UserViews


def setup_routes(app: falcon.App, user_views: UserViews) -> falcon.App:
    app.add_route("/users", user_views, suffix="users")
    app.add_route("/users/{user_id}", user_views, suffix="user")
    return app
