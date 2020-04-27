# project layout
#
# server (you are here!)
#   -> views
#       -> controller
#           -> models
#
# server.py sets up the server configuration, and attached the views to the routes.
# It is meant to be run as an entrypoint script, and should fail if there are any
# fatal configuration issues.


# 3rd party imports
import dotenv
import flask
# local imports
import views

# environment variables
dotenv.load_dotenv()

# flask configuration
app = flask.Flask(__name__)

# server routes
app.route("/", methods=["GET"])(views.index)
