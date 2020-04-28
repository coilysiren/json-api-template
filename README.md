# `a27`

🚧 contents under construction 🚧

## Development Setup

This project makes heavy use of docker, so that following tools are the only ones **required** for building the project in a basic fashion:

- docker
- docker-compose

**Optionally** if you want to setup more complex development tooling (editor auto-complete, linters, debugging, etc) then you will also need all of the following:

- homebrew, and the following homebrew installed tools
  - postgres
  - python @ 3.8
- python above comes with pip, and via pip you will also need the following
  - pylint
  - pytest
  - black

## Development Workflow

The most common commands are listed in the `Makefile`, and are run via `make test`, `make run`, etc etc.

More esoteric commands are listed in the `./scripts/` folder, you will generally not need to run these directly unless instructed to do so / you personally know that you need to do so. They are run like so: `./scripts/check_docker.sh`.

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
# [ server layer ]
#
# -> app.py
#   -> routes.py
#     -> views.py
#   -> controller.py
#     -> decider.py
#
# [ tests layer ]
#
# -> test_controller.py
# -> test_decider.py
#
```
