# [[ project layout ]]
#
# [ server viewpoint ]
#
# server (🗺 you are here!)
#   -> database
#   -> routes
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
# server.py sets up the server configuration, and attaches the views to the routes.
# It is meant to be run as an entrypoint script, and should fail if there are any
# obvious fatal configuration issues.


# 3rd party imports
import dotenv
import flask

# local imports
import .routes


def create_app():
    '''
    create_app creates the flask application

    docs => https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    '''
    # environment variables
    dotenv.load_dotenv()
    # flask configuration
    app = flask.Flask(__name__)
    app = routes.setup_routes(app)
