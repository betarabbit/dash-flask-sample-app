#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Sample basic Dash app"""
import pandas as pd
#from dash import html
import dash as ds

from app.dash_apps import create_dash_app
#import app

# endpoint of this page
URL_RULE = "/experiments"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/experiment-list/"


def create_dash(server):
  """Create a Dash view"""
  app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)
  
  df = pd.DataFrame(
    {"ID": [1, 2, 3], "Name": ["Experiment 1", "Experiment 2", "Experiment 2"]}
  )

  app.layout = ds.html.Div(
    children = [
      ds.html.Nav(
        children = ds.html.Ol(
          [ds.html.Li("Experiments", id="current-breadcrumb-item", className="breadcrumb-item active", ), ],
          className = "breadcrumb",
        )
      ),
      ds.html.Div(children="List of all experiments."),
      ds.html.Table(
        children = [
          ds.html.Thead(ds.html.Tr([ds.html.Th(col) for col in df.columns])),
          ds.html.Tbody([
            ds.html.Tr(
              [
                ds.html.Td(
                  ds.html.A(df.iloc[i][col], href = f"/experiments/{df.iloc[i][col]}",) if col == "ID" else df.iloc[i][col]
                )
                for col in df.columns
              ]
            )
            for i in range(len(df))
          ]),
        ],
        className = "table table-hover table-bordered",
      ),
      ]
    )

  return app.server
