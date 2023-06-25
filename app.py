import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
# SLATE

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
templates = "SLATE"
load_figure_template("SLATE")

