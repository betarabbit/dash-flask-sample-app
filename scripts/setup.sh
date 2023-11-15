#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/env

# Activate virtual environment
poetry shell

# Install dependencies
peotry install
