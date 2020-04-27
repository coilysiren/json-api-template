#!/bin/bash

set -euo pipefail
set -o xtrace

description=${1:-"TODO: your migration descriptin"}

command="pipenv run alembic revision -m \"$description\""

docker-compose run migrations bash -c "$command"
