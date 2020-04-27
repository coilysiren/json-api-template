#!/bin/bash

set -euo pipefail
set -o xtrace

container=${1:-"server"}

docker exec -it "$(docker container ls --filter "name=$container" --quiet)" bash
