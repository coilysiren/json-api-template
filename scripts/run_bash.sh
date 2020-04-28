#!/bin/bash

set -euo pipefail
set -o xtrace

container=${1:-"server"}

docker-compose run "$container" bash -c "pipenv install --system && bash"
