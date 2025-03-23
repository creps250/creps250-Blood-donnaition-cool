import dash
import dash_bootstrap_components as dbc

font_awesome1 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css'
font_awesome3 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/solid.min.css'

app = app = dash.Dash(__name__, 
                      external_stylesheets=[dbc.themes.BOOTSTRAP]
                      , suppress_callback_exceptions=True)

server = app.server
