#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Dash apps"""
import dash
#from jinja2 import Environment, PackageLoader, select_autoescape
import jinja2

from app.views import get_top_menu_items

env = jinja2.Environment(
  loader     = jinja2.PackageLoader("app", "templates"),
  autoescape = jinja2.select_autoescape(),
)


def customize_index_string(app, url):
  """Custom app's index string"""
  app.index_string = env.get_template("dash_layout.html").render(
    top_menu_items = get_top_menu_items(url)
  )


def add_route(app, url):
  """Add route to the app"""
  app.server.add_url_rule(url, endpoint=url, view_func=app.index)
  app.routes.append(url)


def create_dash_app(server, url_rule, url_base_pathname):
  """Create a Dash app with customized index layout

  :param server: base Flask app
  :param url_rule: url rule as endpoint in base Flask app
  :param url_base_pathname: url base pathname used as dash internal route prefix
  """
  app = dash.Dash(name=__name__, server=server, url_base_pathname=url_base_pathname)

  customize_index_string(app, url_rule)
  add_route(app, url_rule)

  return app
