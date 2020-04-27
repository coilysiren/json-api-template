# [[ project layout ]]
#
# [ server viewpoint ]
#
# server
#   -> database
#   -> routes
#       -> views (🗺 you are here!)
#           -> controller
#               -> models
#
# [ migrations viewpoint ]
#
# migrations
#   -> database
#   -> models


# builtin imports
import json


def index():
    return json.dumps({"message": "hello ✨"}, ensure_ascii=False)
