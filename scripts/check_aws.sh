#!/bin/bash

# check if `aws` is installed

set -euo pipefail

command -v aws >/dev/null 2>&1 || { echo >&2 "aws cli needs to be installed, please install it on mac with via the directions here => https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html"; exit 1; }

# interviewer note:
#
# in a company environment the above link would likely point to an internal wiki page
# rather than pointing directly to the aws docs
#
# the motivation there being that aws has multiple installation modes
# and companies likely want to enforce people using a specific one
