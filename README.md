# bluelink code test

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
# - connection.py
# - models.py
#
# [ migrations layer ]
#
# - env.py
# - versions/*.py
#
# [ server layer ]
#
# - app.py
#   - errors.py
#   - routes.py
#     - views.py     <-|
#   - controller.py  <-- the interesting parts!
#     - schema.py    <-|
#
# [ tests layer ]
#
# - test_controller.py  <-- also interesting!
#
```

## Testing

In addition to running `make test` (or looking at Github Actions) you can run tests manually like so:

```bash
# if you get a race condition on the database starting up
# then try `make run` a 2nd time!

make run

brew install httpie

http localhost:8000/users email=lynncyrin@gmail.com role=admin
http localhost:8000/users
http localhost:8000/users email=lynncyrin+testing@gmail.com role=standard smsUser=true
http localhost:8000/users email=BAD_EMAIL

# lists in query strings are a bit weird
http localhost:8000/users\?roles=standard\&roles=admin
http localhost:8000/users\?roles=admin

# Make note of the id above, as it is needed in the following lines.
# It will most likely be "1"!

http localhost:8000/users/1
http PUT localhost:8000/users/1 givenName=lynn
http localhost:8000/users
```
