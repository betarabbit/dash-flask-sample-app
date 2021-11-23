# Background
(Plotly Dash)[https://plotly.com/dash/] is a web application framework for Python that allows you to build beautiful, responsive, interactive data visualizations in seconds. However, an application can only display data aren't always useful. If we want to have a fully-featured application, we need to make use of its backend (Flask)[https://flask.palletsprojects.com/en/2.0.x/].

# Issues
Even though Dash piggyback off of Flask, this Flask is in a sandbox, and doesn't have a lot of the same functionalities. For example, the following ones are missing or requires Dash enterprise version:

- Database Integration
- Authentication
- Multiple Pages/Routes
- Custom Style
- etc.

# Design
To overcome all above issues, instead of using the Flask spinned up by Dash, we would like to create a base Flask application and put our Dash applications on top of it.

## Principles
- __Flexible__ -- Be able to create any kind of application with Dash and Flask.
- __Fully-featured__ -- Both Dash and Flask need to be fully featured, no limitations to functionality
- __Customizable__ -- Be able to customize the look and feel of the application.
- __Simple__ -- Be able to create a Dash application with minimal effort.

## Solutions
Generally, There are 2 approaches to achieve this:

- __Sub applications__: Create a base Flask application and initialize Dash applications using the parent Flask server, register them as sub applications with custom routes.
- __iframe__: Create a base Flask application, put Dash applications in `iframe`, and use Flask pages to load these `iframe`.

## Which one is better
Comparing the approach of putting Dash application in `iframe`, even though it may be the easiest way, due to the absolute isolation nature of `iframe`, it also introduces new issues:
- __Hard to Customize__: The `iframe` approach is hard to customize, because it is not possible to change the look and feel of the application in it.
- __Inconsistent__: The `iframe` approach is inconsistent, because it has its own navigation system than the main frame, click links in `iframe` will not trigger a page jump in the main frame.
- __Not scalable__: The `iframe` approach is not scalable, because it is not possible to create a multi-page Dash application.

From above we can see that the first approach sub-applications is more flexible and can be used for any kind of application.

## Code Structure
The code structure of the base Flask application is as follows:
```bash
├── app
│   ├── dash_apps               -- All Dash applications are stored here
│   │   ├── custom_dash_app.py
│   │   ├── experiment_detail_dash_app.py
│   │   ├── experiment_list_dash_app.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── static
│   │   └── styles.css  -- Custom CSS styles
│   ├── templates
│   │   ├── dash_layout.html    -- Layout of Dash applications
│   │   ├── header.html         -- Extracted common header for all pages
│   │   ├── index.html          -- Main page
│   │   └── layout.html         -- Layout of the main page
│   └── views.py                -- Flask route and top menu definitions
├── config.py
├── poetry.lock
├── poetry.toml
├── pyproject.toml
├── README.md
├── scripts
│   ├── fix.sh
│   ├── run.sh
│   └── setup.sh
├── setup.cfg
└── wsgi.py
```

## Implementation Details
To achieve the sub-apps implementation, we need to implement the following key code functions.

- Create the base application blueprint
- Register the base application blueprint in Flask
- Link Dash to the base application and define its layout/route endpoint

### Create the base application blueprint:
Blueprint is a Flask component to implement modular Flask application.

`app/views.py`
```python
from flask import Blueprint, render_template

base_app = Blueprint("base_app", __name__)

@base_app.route("/")
def index():
    """Landing page."""
    return render_template("index.html", top_menu_items=get_top_menu_items("/"))
```

### Register the base application blueprint in Flask
It is called application factory pattern in Flask's term, create a `create_app` function, and return the application object. Flask will call this function to serve requests.

`app/__init__.py`
```python
from flask import Flask

from app.views import base_app

def create_app(test_config=None):
    """Create and configure Flask app"""

    app = Flask(__name__)

    app.register_blueprint(base_app)

    return app
```

### Link Dash to the base application and define its layout/route endpoint
Create the Dash app using the base application

`app/dash_apps/__init__.py`
```python
def customize_index_string(app, url):
    """Custom app's index string"""
    app.index_string = env.get_template("dash_layout.html").render(
        top_menu_items=get_top_menu_items(url)
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
```

`app/dash_apps/custom_dash_app.py`
```python
from app.dash_apps import create_dash_app

# endpoint of this page
URL_RULE = "/custom-app"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/custom-app/"


def create_dash(server):
    """Create a Dash view"""
    app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)

    # dash app definitions goes here
    ...

    return app.server
``` 
# How to Add Dash applications
There are total 2 steps to add a Dash application to the base Flask application:

Step 1: Create the Dash application

1-1: Create a `.py` file in `app/dash_apps` directory.

1-2: Follow below code structure to create a Dash application:
```python
from app.dash_apps import create_dash_app

# endpoint of this page
URL_RULE = "/custom-app"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/custom-app/"


def create_dash(server):
    """Create a Dash view"""
    app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)

    # dash app definitions goes here, same what you would do in normal Dash application
    ...

    return app.server
``` 

Step 2: Add top menu items in `app/views.py` for the Dash application (optional)
```python
top_menus = [
    {"path": "/", "title": "Home"},
    {"path": "/experiments", "title": "Experiments"},
    {"path": "/custom-app", "title": "Custom App"},
    ...
]
```

# How to Run
Execute the following command to run the application, if `FLASK_ENV=development` is set, the application will run in debug mode:
```bash
bash scripts/run.sh
```
