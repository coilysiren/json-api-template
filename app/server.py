# project layout
#
# server (you are here!)
#   -> views
#       -> controller
#           -> models
#
# ( brief description )


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
