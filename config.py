"""Global configs"""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = environ.get("SECRET_KEY")
