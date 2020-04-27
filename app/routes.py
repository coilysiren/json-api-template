# [[ project layout ]]
#
# [ server viewpoint ]
#
# server
#   -> database
#   -> routes (🗺 you are here!)
#       -> views
#           -> controller
#               -> models
#
# [ migrations viewpoint ]
#
# migrations
#   -> database
#   -> models
#
# routes.py attaches the views to the routes. It is invoked during server configuration
# (eg at server startup time)


# 3rd party imports
import flask

# local imports
import .views


def setup_routes(app: flask.Flask) -> flask.Flask:
    '''
    setup_routes attaches our views to our routes

    docs => https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
    '''
    app.route("/", methods=["GET"])(views.index)
    return app
