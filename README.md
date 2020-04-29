# bluelink code test

## Decisions Made

- null columns, defaults on columns
- email and role are required
- empty emails? empty roles?
- no length on names => https://www.w3.org/International/questions/qa-personal-names#singlefield

## Development Setup

**[ required ]** This project makes heavy use of docker, so that following tools are the only ones required for building the project in a basic fashion:

- docker
- docker-compose

**[ optional ]** If you want to setup more complex development tooling (editor auto-complete, linters, debugging, etc) then you will also need all of the following:

- homebrew via https://brew.sh/, and the following homebrew installed tools via `brew install $tool`
  - postgres
  - python@3.8
- the above python install above comes with pip, and via pip you will also want to **globally** install the following via `pip install $tool`
  - pipenv
  - pylint
  - black
- finally, run `make dev` to initialize a **local** installation of all of the above dev tools

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
#   -> errors.py
#   -> routes.py
#     -> views.py
#   -> controller.py
#     -> schema.py
#
# [ tests layer ]
#
# -> test_controller.py
# -> test_decider.py
#
```
