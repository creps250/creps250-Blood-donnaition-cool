import dash
import dash_bootstrap_components as dbc

font_awesome1 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css'
font_awesome3 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/solid.min.css'

app = app = dash.Dash(__name__,
                      external_stylesheets=[dbc.themes.BOOTSTRAP],
                      suppress_callback_exceptions=True, title="Tableau de bord des dons de sang",
                      meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
                      )
'''
    Initialise l'application Dash.
    :param __name__: Le nom du module.
    :param external_stylesheets: Les feuilles de style externes à utiliser.
    :param suppress_callback_exceptions: Indique si les exceptions de rappel doivent être supprimées.
    '''
    
app._suppress_callback_exceptions = True    

server = app.server
