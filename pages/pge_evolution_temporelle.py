from packages.pkg_evolution_temporelle import *
from dash import html, dcc, callback_context, ctx
import dash_bootstrap_components as dbc
from app import *
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify
from prossess_data.process_temporelle import *
from packages.pkg_kpi import *


def page_trois(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme):
    
    """
    Page 3 de l'application qui affiche les KPIs sur la page d'accueil, 
    ainsi que des graphiques sur l'évolution temporelle des dons et des caracteristiques 
    demographiques des donneurs.

    Parameters
    ----------
    theme : str
        Le thème actuel ('light' ou 'dark') qui détermine les couleurs à utiliser.
    plot_font_color : str
        La couleur du texte des graphiques.
    plot_bg : str
        La couleur de fond des graphiques.
    plot_paper_bg : str
        La couleur de fond des graphiques.
    plot_grid_color : str
        La couleur de la grille des graphiques.
    light_theme : dict
        Le dictionnaire contenant les couleurs du thème clair.
    dark_theme : dict
        Le dictionnaire contenant les couleurs du thème sombre.

    Returns
    -------
    html.Div
        Le contenu HTML de la page 3 de l'application.
    """
    if theme == 'light':
        card_style = {'backgroundColor': light_theme['cardBg']}
        style_dropdow = {'width': '150px', 'backgroundColor': '#D9DADC', 'border': 'none', 'fontSize': '12px'}
    else:
        card_style = {'backgroundColor': dark_theme['cardBg'], 'color': 'white'}
        style_dropdow = {'width': '150px', 'backgroundColor': 'black', 'border': 'none', 'fontSize': '12px', 'color': 'black'}
    

    return html.Div([
        dbc.Row([
        # Première ligne avec quatre cartes
        dbc.Col([dbc.Row([ 
            # Première carte - Taux de dons
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            DashIconify(
                                icon="mdi:gift-outline",
                                width=40,
                                height=40,
                                style={"color": "white"}
                            ),
                        ], style={"float": "left", "margin-right": "15px", "background-color": "#3A7AB9", "padding": "15px", "border-radius": "5px"}),
                        html.Div([
                            html.H2(str(taux_don(data_final)) +" %", className="card-title"),
                            html.P("Taux de dons (%)"),
                        ]),
                    ])
                ], className="mb-2 shadow-sm", style={"height": "140px", **card_style})
            ], width=6),
            # Deuxieme carte - Ajouter une nouvelle métrique
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            DashIconify(
                                icon="mdi:trending-up",
                                width=40,
                                height=40,
                                style={"color": "white"}
                            ),
                        ], style={"float": "left", "margin-right": "15px", "background-color": "#E9573F", "padding": "15px", "border-radius": "5px"}),
                        html.Div([
                            html.H2("+" + str(compter_dons_par_mois(data_don)[0]) + " %", className="card-title"),
                            html.I('realise en ' + str(compter_dons_par_mois(data_don)[1])),
                            html.P("Meilleurs taux de progression de don"),
                        ]),
                    ])
                ], className="mb-2 shadow-sm", style={"height": "140px", **card_style})
            ], width=6)
            
        ]),
           dbc.Col([
                dbc.Card([
                   dbc.CardHeader([
                        html.Div([
                            # Icône et titre à gauche
                            html.Div([
                                DashIconify(
                                    icon="mdi:chart-bar",
                                    width=24,
                                    height=24,
                                    style={"margin-right": "5px", "margin-left": "5px", "color": "#3A7AB9"}
                                ),
                                html.Span("Évolution Mensuel des dons", style={"vertical-align": "middle"})
                            ], style={"display": "flex", "align-items": "center"}),
                            
                            # Bouton de filtre (sans slider)
                            html.Div([
                                dbc.Button([
                                    DashIconify(
                                        icon="mdi:filter-remove-outline",
                                        width=16,
                                        height=16,
                                        style={"margin-right": "5px"}
                                    ),
                                    "Remove Filter"
                                ],
                                id="filtre1",
                                color="white",
                                size="sm",
                                className="btn btn-light btn-sm"
                                )
                            ], style={"display": "flex", "align-items": "center", "justify-content": "flex-end"})
                        ], style={"display": "flex", "justify-content": "space-between", "align-items": "center", "width": "100%"})
                    ], className="p-0"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=retourn_evolution_mois(data_don),
                            responsive=True, style={'height': 380}, id='evol-annee'
                        )
                    ])
                ], className="shadow-sm", style={"height": 450, **card_style})
            ], width=12)      
        ],width=6),
        dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Div([
                                DashIconify(
                                    icon="mdi:account-details",
                                    width=24,
                                    height=24,
                                    style={"margin-right": "10px", "color": "#E9573F"}
                                ),
                                html.Span("Caracteristiques demographique", style={"vertical-align": "middle"})
                            ], style={"display": "flex", "align-items": "center"}),
                            dcc.Dropdown(
                                id='caract-menu',
                                options=[
                                    {'label': i, 'value': i} for i in data_cluster_don.columns.tolist()[:-2]
                                ], clearable=False,
                                value='Genre',  # Option par défaut
                                style=style_dropdow # Ajustez la largeur selon vos besoins
                            )
                        ], 
                        className="d-flex justify-content-between align-items-center")
                    ),
                    dbc.CardBody([
                        html.Div([
                            dcc.Graph(id='caract-demo',
                                figure=Plot_genre(data_cluster_don, 'Situation Matrimoniale (SM)', 'Repartition du genre des donneurs de sang'),
                                responsive=True, 
                                style={'height': 510, 'width': '100%'}  # Modifié pour prendre 100% de largeur
                            )
                        ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center'})  # Centrage du graphique
                    ])
                ], className="shadow-sm", style={"height": 600, **card_style})
            ], width=6),  # Augmenté de 5 à 6 pour donner plus d'espace au piechart
        ]),
        dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                    html.Div([
                        # Icône et titre à gauche
                        html.Div([
                            DashIconify(
                                icon="mdi:account-group",
                                width=24,
                                height=24,
                                style={"margin-right": "5px", "margin-left": "5px", "color": "#3A7AB9"}
                            ),
                            html.Span("Modèles de comportement et éligibilité des donneurs", style={"vertical-align": "middle"})
                        ], style={"display": "flex", "align-items": "center"}),
                        
                        # Boutons à droite
                        html.Div([
                            dbc.Button("Calendrier", color="primary", outline=True, size="sm", className="me-2",id="btn-calendar"),
                            dbc.Button("Modèles de comportement", color="primary", outline=True, size="sm",id="btn-modele")
                        ], style={"display": "flex", "align-items": "center"})
                    ], style={"display": "flex", "justify-content": "space-between", "align-items": "center", "width": "100%"})
                ], className="p-0"),
            dbc.CardBody([
                dcc.Graph(
                    figure=create_calendar_heatmap(data_final),#create_acm_eligibility_dashboard(data=data_final, variables=None),
                    responsive=True, style={'height': 480}, id='acm-eligibility'
                )
            ])
        ], className="shadow-sm mt-3", style={"height": 550, **card_style})
    ], width=12)
])
        ])
  
  
@app.callback(
    Output('caract-demo', 'figure'),
    Input('caract-menu', 'value'),
    suppress_callback_exceptions=True
)
def update_graph(selected_value):
    # Mise à jour du graphique en fonction de la sélection
    """
    Updates the 'caract-demo' graph based on the selected value from the dropdown menu.

    Parameters:
    -----------
    selected_value : str
        The value selected from the 'caract-menu' dropdown, which determines the 
        category to visualize in the graph.

    Returns:
    --------
    plotly.graph_objs.Figure
        A plotly figure object representing the distribution of the selected 
        category among blood donors.
    """

    return Plot_genre(data_don, selected_value, f'Repartition du {selected_value} des donneurs de sang')


@app.callback(
    Output("acm-eligibility", "figure"),
    [Input("btn-calendar", "n_clicks"), 
     Input("btn-modele", "n_clicks")],
    prevent_initial_call=True
)
def update_output(calendar_clicks, modele_clicks):
    # Récupérer le bouton qui a été cliqué
    """
    Updates the 'acm-eligibility' graph based on the button clicks from the navbar.

    Parameters:
    -----------
    calendar_clicks : int
        The number of clicks on the "Calendrier" button.
    modele_clicks : int
        The number of clicks on the "Modèles de comportement" button.

    Returns:
    --------
    plotly.graph_objs.Figure
        A plotly figure object representing either a heatmap of the calendar or a dashboard of eligibility.
    """

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "btn-calendar":
        # Générer le heatmap du calendrier
        return create_calendar_heatmap(data_final)
    elif trigger_id == "btn-modele":
        # Générer le dashboard d'éligibilité
        return create_acm_eligibility_dashboard(data=data_final, variables=None)
    
    # Par défaut, ne rien afficher
    return {}


@app.callback(
    Output('evol-annee', 'figure'),
    [Input('caract-menu', 'value'),
     Input('filtre1', 'n_clicks')],
    suppress_callback_exceptions=True
)
def update_graph(selected_value, n_clicks):
    # Mise à jour du graphique en fonction de la sélection
    """
    Updates the 'evol-annee' graph based on the selected value from the dropdown menu
    and the filter button.

    Parameters:
    -----------
    selected_value : str
        The value selected from the 'caract-menu' dropdown, which determines the
        category to visualize in the graph.
    n_clicks : int
        The number of clicks on the "Filtre" button.

    Returns:
    --------
    plotly.graph_objs.Figure
        A plotly figure object representing the distribution of the selected
        category among blood donors over time.
    """
    ctx = dash.callback_context
    
    # Identify which input triggered the callback
    if not ctx.triggered:
        # No trigger, return default (assuming caract-menu has initial value)
        return retourn_evolution_mois(data_don)
    
    # Get the ID of the component that triggered the callback
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'caract-menu':
        # If the dropdown menu triggered the callback
        return plot_mois_vars_counts(var_=selected_value, title=f'Répartition du nombre de dons au fil des mois par {selected_value}')
    
    elif trigger_id == 'filtre1' and n_clicks > 0:
        # If the filter button triggered the callback
        return retourn_evolution_mois(data_don)
    
    # Default case (should not normally happen)
    return retourn_evolution_mois(data_don)
