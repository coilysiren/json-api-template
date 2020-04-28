# `a27`

🚧 contents under construction 🚧

## Development

The following tools should be installed with homebrew:

- docker / docker-compose
- homebrew
- npx
- yq / jq
- python @ 3.8

## Project Layout

```python
# [ database layer ]
#
# -> connection.py
# -> models.py
#
# [ migrations layer ]
#
# -> env.py
# -> versions/*.py
#
# [ server viewpoint ]
#
# -> app.py
#   -> routes.py
#     -> views.py
#   -> controller.py
#     -> decider.py
```
