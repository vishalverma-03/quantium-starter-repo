import pytest
from dash import Dash
from dash.testing.application_runners import import_app

@pytest.fixture
def app():
    # Import your Dash app
    app = import_app("scripts.dashboard")  # path to your dashboard.py file
    return app

def test_header_is_present(dash_duo, app):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")
    assert header.text == "Soul Foods Pink Morsel Sales Dashboard"

def test_visualisation_is_present(dash_duo, app):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("div.js-plotly-plot")
    assert graph is not None

def test_region_picker_is_present(dash_duo, app):
    dash_duo.start_server(app)
    region_picker = dash_duo.find_element("input[type='radio']")
    assert region_picker is not None
