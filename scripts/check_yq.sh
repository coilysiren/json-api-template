#!/bin/bash

# check if `yq` is installed

set -euo pipefail

command -v yq >/dev/null 2>&1 || { echo >&2 "yq needs to be installed, please install it on mac with \"brew install yq\""; exit 1; }
