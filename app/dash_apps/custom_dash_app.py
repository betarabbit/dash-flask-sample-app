#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Sample callback Dash app"""
import dash as ds

from app.dash_apps import create_dash_app
#import app

# endpoint of this page
URL_RULE = "/custom-app"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/custom-app/"

def create_dash(server):
  """Create a Dash view"""
  app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)

  app.layout = ds.html.Div([
    ds.dcc.Location(id="url", refresh=False),
    ds.html.H1(id="title", children="Custom App"),
    ds.html.Div(
      "Change value in the input box!",
      style = {"marginBottom": "20px"},
    ),
    ds.html.Label("Amino-acid Sequence:", className="form-label", htmlFor="sequence"),
    ds.dcc.Textarea(id=f"sequence", className="form-control"),
    ds.html.Label("Job Title:", className="form-label", htmlFor="job_title"),
    ds.dcc.Input(id=f"job_title", type="text", className="form-control"),
    ds.html.Label("e-mail:", className="form-label", htmlFor="email"),
    ds.dcc.Input(id=f"email", type="email", className="form-control"),
    #ds.html.Div(id="output", className="form-text"),
  ])

  @app.callback(ds.Output("output", "children"), [ds.Input("input", "value")])
  def update_output_div(value):
    return f"Output: {value}"

  return app.server
