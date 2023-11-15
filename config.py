#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Global configs"""
import os
#from os import environ, path

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
  """Base config class"""
  CSRF_ENABLED = True
  SECRET_KEY   = os.environ.get("SECRET_KEY")
