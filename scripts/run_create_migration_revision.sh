#!/bin/bash

set -euo pipefail
set -o xtrace

name=${1:-"TODO: enforce migration name"}

command="alembic -c setup.cfg revision --autogenerate -m \"$name\""

docker-compose run migrations bash -c "./scripts/run_on_container_init.sh && $command"
