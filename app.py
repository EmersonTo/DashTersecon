import dash
import dash_bootstrap_components as dbc

# SLATE
server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE],server = server)


