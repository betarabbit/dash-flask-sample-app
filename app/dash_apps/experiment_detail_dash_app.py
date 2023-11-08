#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Sample basic Dash app"""
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from app.dash_apps import create_dash_app

# endpoint of this page
URL_RULE = "/experiments/<experiment_id>"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/experiment-detail/"


def create_dash(server):
  """Create a Dash view"""
  app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)
  
  df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
  })

  fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
  
  app.layout = html.Div(
    children = [
      dcc.Location(id="url", refresh=False),
      html.Nav(
        html.Ol(
          children = [
            html.Li(
              children  = html.A("Experiments", href="/experiments"),
              className = "breadcrumb-item",
            ),
            html.Li(
              id        = "current-breadcrumb-item",
              className = "breadcrumb-item active",
            ),
          ],
          className = "breadcrumb",
        )
      ),
      html.Div(id="description", children=""),
      dcc.Graph(id="example-graph", figure=fig),
    ]
  )

  @app.callback(
    [
      Output("current-breadcrumb-item", "children"),
      Output("description", "children"),
    ],
    [Input("url", "pathname")],
  )
  def update_id(pathname):
    experiment_id = pathname.split("/")[-1]
    return (
      f"Experiment {experiment_id}",
      f"Description of experiment {experiment_id}",
    )

  return app.server
