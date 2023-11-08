#!/usr/bin/env bash

# SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# cd $SCRIPT_DIR/..

isort --atomic .
flake8
mypy app --ignore-missing-imports
