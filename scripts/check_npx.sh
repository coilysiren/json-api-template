#!/bin/bash

# check if `npx` is installed

set -euo pipefail

command -v npx >/dev/null 2>&1 || { echo >&2 "npx needs to be installed, please install it on mac with \"brew install npm\""; exit 1; }
