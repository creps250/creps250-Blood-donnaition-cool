from packages.pkg_analyse_elegibilite import *
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from app import *
from dash_iconify import DashIconify
from dash.dependencies import Input, Output, State
from prossess_data.prossess import *
import dash  
from prossess_data.process_analyse_elegibilite import *
from dash import callback, Input, Output, State
from packages.pkg_kpi import *


df_elig=cluster_df(data_final)

def page_deux(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme, data_final=None):
    # Si data_final n'est pas fourni, on utilise une variable globale
    
    """
    Crée la page 2 de l'application (Analyse de l'éligibilité) avec les éléments suivants:
    - Une carte supérieure avec 4 cartes pour afficher les KPIs de taux d'éligibilité global, taux de dons global, âge moyen des éligibles, âge moyen des donneurs
    - Une carte inférieure avec 2 dropdowns pour filtrer les données par sexe et status marital
    - Une grande carte inférieure avec un graphique en barres horizontales pour afficher les principaux facteurs d'éligibilité et d'indisponibilité
    - Une carte inférieure avec un graphique en barres verticales pour afficher les autres facteurs
    - Une carte inférieure avec un graphique en barres verticales pour afficher les profils des personnes éligibles
    - Une carte inférieure avec un graphique en barres verticales pour afficher les caractéristiques des personnes éligibles
    - Une carte inférieure avec un graphique en barres verticales pour afficher les analyses des donneurs effectifs
    """
    if theme == 'light':
        card_style = {'backgroundColor': light_theme['cardBg']}
        style_dropdow = {'width': '230px', 'backgroundColor': '#D9DADC ', 'border': 'none','fontSize': '12px'}
    else:
        card_style = {'backgroundColor':   dark_theme['cardBg'],'color':'white'}
        style_dropdow = {'width': '230px', 'backgroundColor': 'black', 'border': 'none','fontSize': '12px','color':'black'}
    
    if data_final is None: 
        from prossess_data.prossess import data_final
        
    a = str(pourcentage_eligibilite(data_final)) + ' %'
    b = str(taux_don(data_final)) + ' %'
    c = str(age_moyen_elig(data_final)) + ' Ans'
    d = str(age_moyen_don(data_final)) + ' Ans'
        
    liste_sexe = data_final['Genre'].unique()
    return html.Div([
            dbc.Row([
            # Première colonne principale (50% de la largeur)
            dbc.Col([
                # Première ligne avec 2 cartes
                dbc.Row([
                    # Carte pour le taux d'éligibilité global
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([ 
                                html.Div([
                                    DashIconify(
                                        icon="mdi:check-decagram",
                                        width=40,
                                        height=40,
                                        style={"color": "white"}
                                    ),
                                ], style={"float": "left", "margin-right": "15px", "background-color": "#F7A93B", "padding": "15px", "border-radius": "5px"}),
                                html.Div([
                                    html.H2(a , className="card-title",id='pourcentage_eligi'),
                                    html.P("Taux d'éligibilité global"),
                                ]),
                            ])
                        ], className="mb-4 shadow-sm",style=card_style)  # Application du style de carte
                    ], md=6),
                    
                    # Carte pour le taux de dons global
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
                                    html.H2(b, className="card-title",id='taux_don'),
                                    html.P("taux de don deja effectue"),
                                ]),
                            ])
                        ], className="mb-4 shadow-sm",style=card_style)  # Application du style de carte
                    ], md=6),
                ]),
                
                # Deuxième ligne avec 2 autres cartes
                dbc.Row([
                    # Carte pour l'âge moyen des personnes éligibles
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    DashIconify(
                                        icon="mdi:account-group",
                                        width=40,
                                        height=40,
                                        style={"color": "white"}
                                    ),
                                ], style={"float": "left", "margin-right": "15px", "background-color": "#48B95E", "padding": "15px", "border-radius": "5px"}),
                                html.Div([
                                    html.H2(c, className="card-title",id='age_moy_elig'),
                                    html.P("Âge moyen des éligibles"),
                                ]),
                            ])
                        ], className="mb-4 shadow-sm",style=card_style)  # Application du style de carte
                    ], md=6),
                    
                    # Nouvelle carte (4ème)
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    DashIconify(
                                        icon="mdi:account-group",
                                        width=40,
                                        height=40,
                                        style={"color": "white"}
                                    ),
                                ], style={"float": "left", "margin-right": "15px", "background-color": "#E74C3C", "padding": "15px", "border-radius": "5px"}),
                                html.Div([
                                    html.H2(d, className="card-title",id='age_don'),
                                    html.P("Âge moyen des donneurs"),
                                ]),
                            ])
                        ], className="mb-4 shadow-sm",style=card_style)  # Application du style de carte
                    ], md=6),
                ]),

                # Graphique du bas
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    DashIconify(
                                        icon="mdi:filter-variant",
                                        width=24,
                                        height=24,
                                        style={"margin-right": "10px", "vertical-align": "middle", "color": "#6366F1"}  # Couleur indigo moderne
                                    ),
                                    "Principaux facteurs d'Éligibilité et d'Indisponibilité"
                                ], style={"display": "flex", "align-items": "center"})
                            ], width=8),
                            dbc.Col([
                                dbc.Button([
                                    "Indisponibilité ",
                                    DashIconify(
                                        icon="mdi:block-helper",
                                        width=20,
                                        height=20,
                                        style={"margin-left": "5px"}
                                    )
                                ], color="danger", className="mr-2", 
                                           size="sm", style={"font-size": "8px", "margin-right": "5px"}, id='princip_indisp'),
                                dbc.Button([
                                    "Éligibilité ",
                                    DashIconify(
                                        icon="mdi:check-circle",
                                        width=20,
                                        height=20,
                                        style={"margin-left": "5px"}
                                    )
                                ], color="success", size="sm", style={"font-size": "8px"}, id='princip_eleg')
                            ], width=4, style={"text-align": "right"})
                        ])
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='princip-raison',
                            figure=raison_indispo_plot(data=data_final),
                            responsive=True,
                            style={'height': '340px'}
                        )
                    ])
                ], className="mb-4 shadow-sm", style={'height': '410px',**card_style}),  # Application du style de carte
            
            ], md=7),
            
            # Deuxième colonne principale (50% de la largeur)
            dbc.Col([
                # Grande carte supérieure
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                DashIconify(
                                    icon="mdi:tune-vertical",
                                    width=24,
                                    height=24,
                                    style={"margin-right": "10px", "vertical-align": "middle", "font-size": "8px", "color": "#8B5CF6"}  # Violet moderne
                                ),
                                "Filtre(Sexe,Status Matrimonial)"
                            ], style={"display": "flex", "align-items": "center"})
                        ])
                    ])
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id='sexe_list',
                                options=[
                                    {'label': i, 'value': i} for i in liste_sexe
                                ],
                                clearable=False,
                                value=[liste_sexe[0]],
                                style=style_dropdow,
                                multi=True
                            ),
                        ], width=6),
                        dbc.Col([
                            dcc.Dropdown(
                                id='statusmatri',
                                options=[
                                    # Ajoutez vos options ici, par exemple:
                                    {'label': 'Marié (e)', 'value': 'Marié (e)'},
                                    {'label': 'Célibataire', 'value': 'Célibataire'},
                                    {'label': 'Divorcé(e)', 'value': 'Divorcé(e)'},
                                    {'label': 'veuf (veuve)', 'value': 'veuf (veuve)'}
                                ],
                                clearable=False,
                                value='Marié (e)',  # Valeur par défaut
                                style=style_dropdow,
                                multi=True  # Dropdown simple, pas multi-sélection
                            ),
                        ], width=6)
                    ])
                ])
            ], className="mb-4 shadow-sm",style=card_style),  # Application du style de carte
                
                # Carte inférieure avec graphique
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    DashIconify(
                                        icon="mdi:chart-bar",
                                        width=24,
                                        height=24,
                                        style={"margin-right": "15px", "vertical-align": "middle", "font-size": "8px", "color": "#EC4899"}  # Rose vif
                                    ),
                                    "Autres Facteur"
                                ], style={"display": "flex", "align-items": "center"})
                            ], width=8),
                            dbc.Col([
                                html.Div([  # Ajout d'un conteneur div avec display flex
                                    dbc.Button([
                                        "Indisponibilité",
                                        DashIconify(
                                            icon="mdi:block-helper",
                                            width=20,
                                            height=5,
                                            style={"margin-left": "5px"}
                                        )
                                    ], color="danger", className="mr-2", size="sm", id='autre_indispo',
                                    style={"font-size": "8px", "margin-right": "5px"}),  # Ajout d'une marge droite
                                    dbc.Button([
                                        "Éligibilité ",
                                        DashIconify(
                                            icon="mdi:check-circle",
                                            width=20,
                                            height=5,
                                            style={"margin-left": "5px"}
                                        )
                                    ], color="success", size="sm", style={"font-size": "8px"}, id='autre_elegi')
                                ], style={"display": "flex", "justify-content": "flex-end"})  # Utilisation de flex
                            ], width=4)
                        ])
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='autre-raison',
                            figure=return_wordmap_indispo(data=data_final),
                            responsive=True,
                            style={'height': '460px'}  # Ajout d'une hauteur pour le graphique
                        )
                    ], style={'height': '510px'})
                ], className="mb-4 shadow-sm",style=card_style)  # Application du style de carte
            ], md=5),
        ]),
        dbc.Row([
        # Première carte: Analyse de l'éligibilité
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        DashIconify(
                            icon="mdi:chart-pie",
                            width=24,
                            height=24,
                            style={"margin-right": "10px", "vertical-align": "middle", "color": "#14B8A6"}  # Teal moderne
                        ),
                        "Analyse de l'éligibilité"
                    ], style={"display": "flex", "align-items": "center", "font-weight": "bold", "flex-grow": "1"}),
                    
                    html.Div([
                        dbc.Button([
                            DashIconify(
                                icon="mdi:chart-cluster",
                                width=18,
                                height=18,
                                style={"margin-right": "5px", "vertical-align": "middle"}
                            ),
                            "Clusters"
                        ], id="btn-clusters", color="light", className="me-2"),
                        dbc.Button([
                            DashIconify(
                                icon="mdi:account-group",
                                width=18,
                                height=18,
                                style={"margin-right": "5px", "vertical-align": "middle"}
                            ),
                            "Profils"
                        ], id="btn-profils", color="light")
                    ], style={"display": "flex", "align-items": "center"})
                        ], style={"display": "flex", "justify-content": "space-between"}),
                dbc.CardBody([
                    # Graphique des facteurs d'éligibilité
                    html.Div([
                        dcc.Graph(
                            id='eligibility-factors-chart',
                            figure=plot_combined_eligibility_heatmap(df=cluster_df(data = data_final), numeric_vars=['Age'],
                                      cat_vars=['Genre', 'Situation Matrimoniale (SM)', 'Religion',"Niveau d'etude", 'A-t-il (elle) déjà donné le sang'] ,
                                      eligibility_column='ÉLIGIBILITÉ AU DON.'),
                            responsive=True,
                            style={'height': '470px'}
                        )
                    ]),
                ])
            ], className="h-100 shadow-sm",style=card_style)
        ], md=7),
        
        # Deuxième carte: Caractérisation des personnes éligibles
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.Div([
                            DashIconify(
                                icon="mdi:account-group",
                                width=24,
                                height=24,
                                style={"margin-right": "10px", "vertical-align": "middle", "color": "#F59E0B"}  # Orange ambre
                            ),
                            "Caractérisation des personnes éligibles"
                        ], style={"display": "flex", "align-items": "center", "font-weight": "bold"}),
                        html.Div([
                            dbc.Button([
                                DashIconify(
                                    icon="simple-icons:sankey",
                                    width=16,
                                    height=16,
                                    style={"margin-right": "5px", "vertical-align": "middle"}
                                ),
                                "Page 1"
                            ], color="light", size="sm", className="me-2", id="page1"),
                            dbc.Button([
                                DashIconify(
                                    icon="simple-icons:sankey",
                                    width=16,
                                    height=16,
                                    style={"margin-right": "5px", "vertical-align": "middle"}
                                ),
                                "Page 2"
                            ], color="light", size="sm", id="page2"),
                        ], style={"display": "flex", "align-items": "center"})
                    ], style={"display": "flex", "align-items": "center", "justify-content": "space-between", "width": "100%"})
                ]),
                dbc.CardBody([
                    # Graphique de caractérisation
                    html.Div([
                        dcc.Graph(
                            id='eligib-demograp',
                            figure=plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion']), # Vous devrez créer cette fonction
                            responsive=True,
                            style={'height': '460px','margin-top':'0px'}
                        )
                    ])
                    
                    
                ])
            ], className="h-100 shadow-sm",style=card_style)
        ], md=5)
    ], className="mb-4"),
    dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Div([
                        DashIconify(
                            icon="mdi:account-multiple-check",
                            width=24,
                            height=24,
                            style={"margin-right": "10px", "vertical-align": "middle", "color": "#22C55E"}  # Green color
                        ),
                        "Analyses Donneurs Effectifs"
                    ], style={"display": "flex", "align-items": "center", "font-weight": "bold"}),
                    html.Div([
                        dbc.Button([
                            DashIconify(
                                icon="mdi:view-dashboard-variant",
                                width=16,
                                height=16,
                                style={"margin-right": "5px", "vertical-align": "middle"}
                            ),
                            "Hiérarchie"
                        ], color="light", size="sm", className="me-2", id="btn-hierarchie"),
                        dbc.Button([
                            DashIconify(
                                icon="mdi:gender-male-female",
                                width=16,
                                height=16,
                                style={"margin-right": "5px", "vertical-align": "middle"}
                            ),
                            "Âge vs sexe"
                        ], color="light", size="sm", id="btn-age-femme"),
                    ], style={"display": "flex", "align-items": "center"})
                ], style={"display": "flex", "align-items": "center", "justify-content": "space-between", "width": "100%"})
            ]),
            dbc.CardBody([
                # You can add a placeholder graph or content here
                html.Div([
                    dcc.Graph(
                        id='donneurs-effectifs-graph',
                        # Replace this with an actual graph function when you have the implementation
                        figure=create_treemap(df=df_volontaire),  
                        responsive=True,
                        style={'height': '460px'}
                    )
                ])
            ])
        ], className="h-100 shadow-sm", style=card_style)
    ], md=12)  # Full width
], className="mb-4")    
            
    ])
    
    
# Callback pour les boutons indispo et éligibilité secondaires
@app.callback(
    Output("autre-raison", "figure"),
    Output("autre_indispo", "disabled"),
    Output("autre_elegi", "disabled"),
    [
        Input("autre_indispo", "n_clicks"),
        Input("autre_elegi", "n_clicks"),
        Input('sexe_list', 'value')
    ],
    [
        State("autre_indispo", "disabled"),
        State("autre_elegi", "disabled")
    ],
    prevent_initial_call=False  # Modification pour gérer le cas initial
)
def mettre_a_jour_figure_autre(n_clicks_indispo, n_clicks_elegi, value_sexe, indispo_disabled, elegi_disabled):
    """
    Met à jour le graphique "autre-raison" en fonction des boutons "autre_indispo" et "autre_elegi".
    
    Si le bouton "autre_indispo" est activé, affiche le graphique des raisons d'indisponibilité
    Si le bouton "autre_elegi" est activé, affiche le graphique des raisons d'éligibilité
    Si le bouton "sexe_list" change, met à jour le graphique en fonction de l'état actuel des boutons
    """
    
    ctx = callback_context
    
    # Si pas de déclencheur défini (charge initiale)
    if not ctx.triggered:
        # Afficher le graphique par défaut
        filtered_data = data_final[data_final['Genre'].isin(value_sexe)]
        return return_wordmap_indispo(data=filtered_data), True, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Données filtrées par sexe
    filtered_data = data_final[data_final['Genre'].isin(value_sexe)]
    
    # Si c'est un changement de sexe_list
    if button_id == "sexe_list":
        # On vérifie l'état actuel pour déterminer quel graphique est affiché
        if indispo_disabled:
            # Le bouton indispo est désactivé = mode indisponibilité actif
            return return_wordmap_indispo(data=filtered_data), True, False
        elif elegi_disabled:
            # Le bouton éligibilité est désactivé = mode éligibilité actif
            return return_wordmap(data=filtered_data), False, True
        else:
            # Aucun bouton sélectionné, on utilise le mode par défaut
            return return_wordmap_indispo(data=filtered_data), True, False
    
    # Si c'est un clic sur un bouton
    elif button_id == "autre_indispo":
        return return_wordmap_indispo(data=filtered_data), True, False
    elif button_id == "autre_elegi":
        return return_wordmap(data=filtered_data), False, True
    
    # Par défaut, mode indisponibilité
    return return_wordmap_indispo(data=filtered_data), True, False

# Callback pour les boutons indispo et éligibilité principaux
@app.callback(
    Output("princip-raison", "figure"),
    Output("princip_indisp", "disabled"),
    Output("princip_eleg", "disabled"),
    [
        Input("princip_indisp", "n_clicks"),
        Input("princip_eleg", "n_clicks"),
        Input('sexe_list', 'value'),
        Input('statusmatri','value')
    ],
    [
        State("princip_indisp", "disabled"),
        State("princip_eleg", "disabled")
    ],
    prevent_initial_call=False  #
)
def mettre_a_jour_figure_princip(n_clicks_indispo, n_clicks_elegi, value_sexe,value_status, indispo_disabled, elegi_disabled):
    """
    Mettre à jour le graphique principal en fonction des boutons indisponibilité et éligibilité, ainsi que des sélections de sexe et de situation matrimoniale.
    
    Parameters:
    ------------
    n_clicks_indispo : int
        Nombre de clics sur le bouton "Indisponibilité"
    n_clicks_elegi : int
        Nombre de clics sur le bouton "Éligibilité"
    value_sexe : list
        La liste des sexes sélectionnés
    value_status : list
        La liste des situations matrimoniales sélectionnées
    indispo_disabled : bool
        L'état actuel du bouton "Indisponibilité" (True = désactivé)
    elegi_disabled : bool
        L'état actuel du bouton "Éligibilité" (True = désactivé)
    
    Returns:
    --------
    figure : plotly.graph_objs.Figure
        Le graphique à afficher
    indispo_disabled : bool
        L'état mis à jour du bouton "Indisponibilité"
    elegi_disabled : bool
        L'état mis à jour du bouton "Éligibilité"
    """
    
    ctx = callback_context
    if isinstance(value_status, str):
        value_status = [value_status]
    
    # Si pas de déclencheur défini (charge initiale)
    if not ctx.triggered:
        # Afficher le graphique par défaut
        filtered_data = data_final[data_final['Genre'].isin(value_sexe)][data_final['Situation Matrimoniale (SM)'].isin(value_status)]
        return raison_indispo_plot(data=filtered_data), True, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Données filtrées par sexe
    filtered_data = data_final[data_final['Genre'].isin(value_sexe)][data_final['Situation Matrimoniale (SM)'].isin(value_status)]
    
    # Si c'est un changement de sexe_list
    if button_id == "sexe_list":
        # On vérifie l'état actuel pour déterminer quel graphique est affiché
        if indispo_disabled:
            # Le bouton indispo est désactivé = mode indisponibilité actif
            return raison_indispo_plot(data=filtered_data), True, False
        elif elegi_disabled:
            # Le bouton éligibilité est désactivé = mode éligibilité actif
            return plot_elegibi_raison_elegibi(data=filtered_data), False, True
        else:
            # Aucun bouton sélectionné, on utilise le mode par défaut
            return raison_indispo_plot(data=filtered_data), True, False
    
    # Si c'est un clic sur un bouton
    elif button_id == "princip_indisp":
        return raison_indispo_plot(data=filtered_data), True, False
    elif button_id == "princip_eleg":
        return plot_elegibi_raison_elegibi(data=filtered_data), False, True
    
    # Par défaut, mode indisponibilité
    return raison_indispo_plot(data=filtered_data), True, False




@callback(
    [Output("eligib-demograp", "figure"),
     Output("page1", "className"),
     Output("page2", "className")],
    [Input("page1", "n_clicks"),
     Input("page2", "n_clicks")],
    [State("eligib-demograp", "figure")]
)
def update_graph_and_buttons(btn1_clicks, btn2_clicks, current_figure):
    # Identifier quel bouton a été cliqué en dernier
    """
    Met à jour le graphique "eligib-demograp" en fonction des boutons "page1" et "page2".
    
    Si le bouton "page1" est cliqué, affiche le graphique de ruban avec les variables "Niveau d'etude", "ÉLIGIBILITÉ AU DON.", "Situation Matrimoniale (SM)" et "Age_Class"
    Si le bouton "page2" est cliqué, affiche le graphique de ruban avec les variables "Genre", "ÉLIGIBILITÉ AU DON." et "Religion"
    Si aucun bouton n'est cliqué, conserve le graphique actuel
    """
    
    ctx = callback_context
    
    # Classes CSS pour le bouton actif et inactif
    active_class = "me-2 bg-secondary text-white"  # Plus foncé
    inactive_class = "me-2 btn-light"              # Gris clair
    
    if not ctx.triggered:
        # Par défaut, au chargement initial
        figure = plot_ruban(data_don=data_final, cols=["Niveau d'etude", 'ÉLIGIBILITÉ AU DON.', 'Situation Matrimoniale (SM)', 'Age_Class'])
        return figure, active_class, inactive_class
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "page1":
        figure = plot_ruban(data_don=data_final, cols=["Niveau d'etude", 'ÉLIGIBILITÉ AU DON.', 'Situation Matrimoniale (SM)', 'Age_Class'])
        return figure, active_class, inactive_class
    
    elif button_id == "page2":
        figure = plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'])
        return figure, inactive_class, active_class
    
    # Cas par défaut
    return current_figure, active_class, inactive_class



@app.callback(
    [Output('pourcentage_eligi', 'children'),  
     Output('taux_don', 'children'),          
     Output('age_moy_elig', 'children'),     
     Output('age_don', 'children')],         
    [Input('sexe_list', 'value'),            
     Input('statusmatri', 'value')]          
)
def update_metrics(selected_sexe, selected_status):
    # Filtrer les données en fonction des sélection
    # s
    
    """
    Mise à jour des indicateurs de performance en fonction des sélections de sexe et de situation matrimoniale
    
    Parameters:
    ------------
    selected_sexe : list
        La liste des sexes sélectionnés
    selected_status : list
        La liste des situations matrimoniales sélectionnées
    
    Returns:
    --------
    a : str
        Le pourcentage d'individus éligibles
    b : str
        Le taux de don
    c : str
        L'âge moyen des individus éligibles
    d : str
        L'âge moyen des donneurs
    """
    if not isinstance(selected_status, list):
        selected_status = [selected_status]
    if not isinstance(selected_sexe, list):
        selected_status = [selected_sexe]    
        
        
    filtered_data = data_final[
        (data_final['Genre'].isin(selected_sexe)) & 
        (data_final['Situation Matrimoniale (SM)'].isin(selected_status))
    ]
    
    # Calculer les nouvelles valeurs
    a = str(pourcentage_eligibilite(filtered_data)) + ' %'
    b = str(taux_don(filtered_data)) + ' %'
    c = str(age_moyen_elig(filtered_data)) + ' Ans'
    d = str(age_moyen_don(filtered_data)) + ' Ans'
    
    # Retourner les nouvelles valeurs pour mise à jour
    return a, b, c, d



@app.callback(
    [Output("eligibility-factors-chart", "figure"),
     Output("btn-clusters", "style"),
     Output("btn-profils", "style")],
    [Input("btn-clusters", "n_clicks"),
     Input("btn-profils", "n_clicks")]
)
def update_chart(clusters_clicks, profils_clicks):
    """
    Met à jour le graphique "eligibility-factors-chart" en fonction des boutons "btn-clusters" et "btn-profils".
    
    Si le bouton "btn-clusters" est cliqué, affiche le graphique des clusters.
    Si le bouton "btn-profils" est cliqué, affiche le graphique combiné des profils d'éligibilité.
    
    Parameters:
    ------------
    clusters_clicks : int
        Nombre de clics sur le bouton "btn-clusters"
    profils_clicks : int
        Nombre de clics sur le bouton "btn-profils"
    
    Returns:
    --------
    fig : plotly.graph_objs.Figure
        La figure à afficher
    clusters_style : dict
        Le style CSS du bouton "btn-clusters" (par défaut, un fond gris)
    profils_style : dict
        Le style CSS du bouton "btn-profils" (par défaut, un fond gris)
    """
    ctx = dash.callback_context
    
    # Déterminer quel bouton a été cliqué
    if not ctx.triggered:
        button_id = "btn-clusters"  # Par défaut
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Définir les styles des boutons en fonction du bouton cliqué
    clusters_style = {"background-color": "#e2e2e2"} if button_id == "btn-clusters" else {}
    profils_style = {"background-color": "#e2e2e2"} if button_id == "btn-profils" else {}
    
    # Générer la figure appropriée
    if button_id == "btn-clusters":
        fig = plot_cluster_distribution(df_elig)
    else:  # profils
        fig = plot_combined_eligibility_heatmap(
            df=df_elig, 
            numeric_vars=['Age'],
            cat_vars=['Genre', 'Situation Matrimoniale (SM)', 'Religion', 
                     "Niveau d'etude", 'A-t-il (elle) déjà donné le sang'],
            eligibility_column='ÉLIGIBILITÉ AU DON.'
        )
    
    return fig, clusters_style, profils_style


# Add these callback functions outside of the page_deux function
@callback(
    Output('donneurs-effectifs-graph', 'figure'),
    [Input('btn-hierarchie', 'n_clicks'),
     Input('btn-age-femme', 'n_clicks')],
    prevent_initial_call=True
)
def update_graph(hierarchie_clicks, age_femme_clicks):
    # Determine which button was clicked
    """
    Mise à jour du graphique "donneurs-effectifs-graph" en fonction des boutons "btn-hierarchie" et "btn-age-femme".

    Si le bouton "btn-hierarchie" est cliqué, affiche le graphique de la hiérarchie des donneurs.
    Si le bouton "btn-age-femme" est cliqué, affiche le graphique de la distribution des âges des femmes.

    Parameters:
    ------------
    hierarchie_clicks : int
        Nombre de clics sur le bouton "btn-hierarchie"
    age_femme_clicks : int
        Nombre de clics sur le bouton "btn-age-femme"

    Returns:
    --------
    fig : plotly.graph_objs.Figure
        La figure à afficher
    """
    ctx = callback_context
    
    if not ctx.triggered:
        return {}
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Use the global data_final from prossess module
    
    if button_id == 'btn-hierarchie':
        # Create treemap when Hierarchie button is clicked
        return create_treemap(df=df_volontaire)
    elif button_id == 'btn-age-femme':
        # Create age distribution when Âge vs Femme button is clicked
        return create_age_distribution(df=df_volontaire)
    
    return {}


