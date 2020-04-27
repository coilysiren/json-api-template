#!/bin/bash

# check if `docker-compose` is installed

set -euo pipefail

command -v docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose needs to be installed, please install it on mac with via the directions here => https://docs.docker.com/compose/install/"; exit 1; }

# interviewer note:
#
# in a company environment the above link would likely point to an internal wiki page
# rather than pointing directly to the docker docs
#
# the motivation there being that docker has multiple installation modes
# and companies likely wnat to enforce people using a specific one
