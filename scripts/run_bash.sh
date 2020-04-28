#!/bin/bash

set -euo pipefail
set -o xtrace

container=${1:-"server"}

docker-compose run "$container" bash -c "./scripts/run_on_container_init.sh && bash"
