# project layout
#
# server
#   -> views (you are here!)
#       -> controller
#           -> models
#
# ( brief description )


# builtin imports
import json


def index():
    return json.dumps({"message": "hello ✨"}, ensure_ascii=False)
