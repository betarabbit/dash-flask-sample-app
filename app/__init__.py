#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Base Flask app"""
import importlib
import logging
import os

from flask import Flask

from app.views import base_app
from config import Config

# Logging configuration
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)


def create_app(test_config=None):
  """Create and configure Flask app"""
  app = Flask(__name__)
  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_object(Config)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  app.register_blueprint(base_app)

  # Find all Dash apps file (who's name ends with "_dash_app.py")
  files = [
    f
    for f in os.listdir(os.path.join(os.path.dirname(__file__), "dash_apps"))
    if f.endswith("_dash_app.py")
  ]

  # Import all Dash apps and call their create_app() function
  for file in files:
    module = importlib.import_module("app.dash_apps." + file[:-3])
    app = module.create_dash(app)

  return app
