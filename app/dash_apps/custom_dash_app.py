"""Sample callback Dash app"""
from dash import dcc, html
from dash.dependencies import Input, Output

from app.dash_apps import create_dash_app

# endpoint of this page
URL_RULE = "/custom-app"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/custom-app/"


def create_dash(server):
    """Create a Dash view"""
    app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)

    app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.H1(id="title", children="Custom App"),
            html.Div(
                "Change value in the input box!",
                style={"marginBottom": "20px"},
            ),
            html.Label("Input:", className="form-label", htmlFor="input"),
            dcc.Input(id="input", type="text", className="form-control"),
            html.Div(id="output", className="form-text"),
        ]
    )

    @app.callback(Output("output", "children"), [Input("input", "value")])
    def update_output_div(value):
        return f"Output: {value}"

    return app.server
