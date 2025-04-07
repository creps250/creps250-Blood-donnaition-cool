from packages.pkg_evolution_temporelle import *
from dash import html, dcc, callback_context, ctx
import dash_bootstrap_components as dbc
from app import *
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify
from prossess_data.process_temporelle import *
from packages.pkg_kpi import *
import json



with open("Translation/translation_evol_temp.json", "r", encoding="utf-8") as fichier:

    TRANSLATIONS = json.load(fichier)


# Composant pour l'icône d'aide et le modal explicatif
def create_help_icon(modal_id, theme, language="fr"):
    """
    Crée une icône d'aide avec un effet de pulsation qui ouvre un modal explicatif.
    
    Args:
        modal_id (str): ID unique pour le modal
        theme (str): Thème actuel ('light' ou 'dark')
        language (str): Langue actuelle ('fr' ou 'en')
        
    Returns:
        html.Div: Un div contenant l'icône d'aide positionnée
    """
    translations = TRANSLATIONS[language]
    
    return html.Div([
        html.Button(
            DashIconify(
                icon="carbon:help",
                width=24,
                height=24,
                color="#ffffff" if theme == 'dark' else "#3A7AB9",
            ),
            id=f"help-btn-{modal_id}",
            className="help-icon-btn",
            n_clicks=0,
            title=translations["Aide"],
            **{"data-bs-toggle": "tooltip", "data-bs-placement": "top"}
        ),
    ], className="help-icon-container", style={
        "position": "absolute",
        "bottom": "10px",
        "left": "10px",
        "zIndex": "100"
    })

# Composant pour créer un modal explicatif
def create_explanatory_modal(modal_id, description, theme, language="fr"):
    """
    Crée un modal explicatif avec une description du graphique.
    
    Args:
        modal_id (str): ID unique pour le modal
        description (str): Description du graphique à afficher
        theme (str): Thème actuel ('light' ou 'dark')
        language (str): Langue actuelle ('fr' ou 'en')
        
    Returns:
        dbc.Modal: Un composant modal de Bootstrap Dash
    """
    translations = TRANSLATIONS[language]
    
    # Classe du modal selon le thème
    modal_class = "dark-mode-modal" if theme == 'dark' else "light-mode-modal"
    
    # Styles pour le bouton
    button_style = {
        'backgroundColor': '#3A7AB9',
        'color': 'white',
        'borderRadius': '8px',
        'fontWeight': 'bold',
        'border': 'none',
        'padding': '8px 20px',
        'transition': 'all 0.2s ease'
    }
    
    # Composant modal
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle([
                    DashIconify(
                        icon="carbon:chart-relationship",
                        width=24,
                        height=24,
                        style={"marginRight": "10px"}
                    ),
                    translations["Comprendre ce graphique"]
                ]),
                close_button=True
            ),
            dbc.ModalBody([
                html.P(description, style={
                    'fontSize': '1rem',
                    'lineHeight': '1.6',
                    'marginBottom': '20px'
                }),
                # Option pour ajouter une image d'exemple ou une illustration
                html.Div([
                    DashIconify(
                        icon="carbon:idea",
                        width=24,
                        height=24,
                        className="tip-icon"
                    ),
                    html.Span("Astuce : Survolez les éléments du graphique pour voir les détails.", 
                             className="tip-text")
                ], className="tip-box", style={
                    'backgroundColor': '#f8f9fa',
                    'padding': '10px',
                    'borderLeft': '4px solid #3A7AB9',
                    'borderRadius': '4px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'gap': '10px'
                })
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    translations["Fermer"],
                    id=f"close-{modal_id}",
                    className="ms-auto",
                    n_clicks=0,
                    style=button_style
                )
            ),
        ],
        id=f"modal-{modal_id}",
        is_open=False,
        centered=True,
        size="lg",
        backdrop="static",
        scrollable=True,
        className=modal_class
    )



def page_trois(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme, language="fr"):
    
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
    language : str
        La langue à utiliser ('fr' ou 'en')

    Returns
    -------
    html.Div
        Le contenu HTML de la page 3 de l'application.
    """
    translations = TRANSLATIONS[language]
    if theme == 'light':
        card_style = {'backgroundColor': light_theme['cardBg'], 'position': 'relative'}
        style_dropdow = {'width': '150px', 'backgroundColor': '#D9DADC', 'border': 'none', 'fontSize': '12px'}
    else:
        card_style = {'backgroundColor': dark_theme['cardBg'], 'color': 'white', 'position': 'relative'}
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
                            html.P(translations["Taux de dons (%)"]),
                        ]),
                    ])
                ], className="mb-2 shadow-sm", style={"height": "140px", **card_style}),
                # Ajout de l'icône d'aide
                create_help_icon("taux-dons", theme, language),
                # Modal explicatif pour ce graphique
                create_explanatory_modal("taux-dons", translations["taux_dons_description"], theme, language)
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
                            html.I(translations['realise en'] + " " + str(compter_dons_par_mois(data_don)[1])),
                            html.P(translations["Meilleurs taux de progression de don"]),
                        ]),
                    ])
                ], className="mb-2 shadow-sm", style={"height": "140px", **card_style}),
                # Ajout de l'icône d'aide
                create_help_icon("taux-progression", theme, language),
                # Modal explicatif pour ce graphique
                create_explanatory_modal("taux-progression", translations["taux_progression_description"], theme, language)
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
                                html.Span(translations["Évolution Mensuel des dons"], style={"vertical-align": "middle"})
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
                                    translations["Remove Filter"]
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
                            figure=retourn_evolution_mois(data_don, title=translations["Évolution mensuelle des dons de sang"]),
                            responsive=True, style={'height': 380}, id='evol-annee'
                        )
                    ]),
                    # Ajout de l'icône d'aide
                    create_help_icon("evol-mensuelle", theme, language),
                    # Modal explicatif pour ce graphique
                    create_explanatory_modal("evol-mensuelle", translations["evol_mensuelle_description"], theme, language)
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
                                html.Span(translations["Caracteristiques demographiques"], style={"vertical-align": "middle"})
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
                                figure=Plot_genre(data_cluster_don, 'Situation Matrimoniale (SM)', 
                                                 title=translations["Repartition du"] + " " + 
                                                 translations["Genre"].lower() + " " + 
                                                 translations["des donneurs de sang"]),
                                responsive=True, 
                                style={'height': 510, 'width': '100%'}  # Modifié pour prendre 100% de largeur
                            )
                        ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center'})  # Centrage du graphique
                    ]),
                    # Ajout de l'icône d'aide
                    create_help_icon("caract-demo", theme, language),
                    # Modal explicatif pour ce graphique
                    create_explanatory_modal("caract-demo", translations["caract_demo_description"], theme, language)
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
                            html.Span(translations["Modèles de comportement et éligibilité des donneurs"], style={"vertical-align": "middle"})
                        ], style={"display": "flex", "align-items": "center"}),
                        
                        # Boutons à droite
                        html.Div([
                            dbc.Button(translations["Calendrier"], color="primary", outline=True, size="sm", className="me-2",id="btn-calendar"),
                            dbc.Button(translations["Modèles de comportement"], color="primary", outline=True, size="sm",id="btn-modele")
                        ], style={"display": "flex", "align-items": "center"})
                    ], style={"display": "flex", "justify-content": "space-between", "align-items": "center", "width": "100%"})
                ], className="p-0"),
            dbc.CardBody([
                dcc.Graph(
                    figure=create_calendar_heatmap(data_final, title=translations["Calendrier des remplissages de fiches"]),
                    responsive=True, style={'height': 480}, id='acm-eligibility'
                )
            ]),
            # Ajout de l'icône d'aide
            create_help_icon("calendar-heatmap", theme, language),
            # Modal explicatif pour ce graphique
            create_explanatory_modal("calendar-heatmap", translations["calendar_heatmap_description"], theme, language)
        ], className="shadow-sm mt-3", style={"height": 550, **card_style})
    ], width=12)
])
        ])
  
  
@app.callback(
    Output('caract-demo', 'figure'),
    Input('caract-menu', 'value'),
    [State('language-store', 'data')],
    suppress_callback_exceptions=True
)
def update_graph(selected_value, language="fr"):
    # Mise à jour du graphique en fonction de la sélection
    """
    Updates the 'caract-demo' graph based on the selected value from the dropdown menu.

    Parameters:
    -----------
    selected_value : str
        The value selected from the 'caract-menu' dropdown, which determines the 
        category to visualize in the graph.
    language : str
        The current language ('fr' or 'en')

    Returns:
    --------
    plotly.graph_objs.Figure
        A plotly figure object representing the distribution of the selected 
        category among blood donors.
    """
    translations = TRANSLATIONS[language]
    title = translations["Repartition du"] + " " + selected_value.lower() + " " + translations["des donneurs de sang"]
    return Plot_genre(data_don, selected_value, title=title)


@app.callback(
    Output("acm-eligibility", "figure"),
    [Input("btn-calendar", "n_clicks"), 
     Input("btn-modele", "n_clicks")],
    [State('language-store', 'data')],
    prevent_initial_call=True
)
def update_output(calendar_clicks, modele_clicks, language="fr"):
    # Récupérer le bouton qui a été cliqué
    """
    Updates the 'acm-eligibility' graph based on the button clicks from the navbar.

    Parameters:
    -----------
    calendar_clicks : int
        The number of clicks on the "Calendrier" button.
    modele_clicks : int
        The number of clicks on the "Modèles de comportement" button.
    language : str
        The current language ('fr' or 'en')

    Returns:
    --------
    plotly.graph_objs.Figure
        A plotly figure object representing either a heatmap of the calendar or a dashboard of eligibility.
    """
    translations = TRANSLATIONS[language]
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "btn-calendar":
        # Générer le heatmap du calendrier
        return create_calendar_heatmap(data_final, title=translations["Calendrier des remplissages de fiches"])
    elif trigger_id == "btn-modele":
        # Générer le dashboard d'éligibilité
        return create_acm_eligibility_dashboard(data=data_final, variables=None, 
                                              title=translations["Analyse des donneurs de sang: Éligibilité et comportements"])
    
    # Par défaut, ne rien afficher
    return {}


@app.callback(
    Output('evol-annee', 'figure'),
    [Input('caract-menu', 'value'),
     Input('filtre1', 'n_clicks')],
    [State('language-store', 'data')],
    suppress_callback_exceptions=True
)
def update_graph(selected_value, n_clicks, language="fr"):
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
    language : str
        The current language ('fr' or 'en')

    Returns:
    --------
    plotly.graph_objs.Figure
        A plotly figure object representing the distribution of the selected
        category among blood donors over time.
    """
    translations = TRANSLATIONS[language]
    ctx = dash.callback_context
    
    # Identify which input triggered the callback
    if not ctx.triggered:
        # No trigger, return default (assuming caract-menu has initial value)
        return retourn_evolution_mois(data_don, title=translations["Évolution mensuelle des dons de sang"])
    
    # Get the ID of the component that triggered the callback
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'caract-menu':
        # If the dropdown menu triggered the callback
        title = translations["Répartition du nombre de dons au fil des mois par"] + " " + selected_value
        return plot_mois_vars_counts(var_=selected_value, title=title)
    
    elif trigger_id == 'filtre1' and n_clicks > 0:
        # If the filter button triggered the callback
        return retourn_evolution_mois(data_don, title=translations["Évolution mensuelle des dons de sang"])
    
    # Default case (should not normally happen)
    return retourn_evolution_mois(data_don, title=translations["Évolution mensuelle des dons de sang"])

# Callbacks pour les icônes d'aide et les modaux
@app.callback(
    Output("modal-taux-dons", "is_open"),
    [Input("help-btn-taux-dons", "n_clicks"), Input("close-taux-dons", "n_clicks")],
    [State("modal-taux-dons", "is_open")],
)
def toggle_modal_taux_dons(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-taux-progression", "is_open"),
    [Input("help-btn-taux-progression", "n_clicks"), Input("close-taux-progression", "n_clicks")],
    [State("modal-taux-progression", "is_open")],
)
def toggle_modal_taux_progression(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-evol-mensuelle", "is_open"),
    [Input("help-btn-evol-mensuelle", "n_clicks"), Input("close-evol-mensuelle", "n_clicks")],
    [State("modal-evol-mensuelle", "is_open")],
)
def toggle_modal_evol_mensuelle(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-caract-demo", "is_open"),
    [Input("help-btn-caract-demo", "n_clicks"), Input("close-caract-demo", "n_clicks")],
    [State("modal-caract-demo", "is_open")],
)
def toggle_modal_caract_demo(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-calendar-heatmap", "is_open"),
    [Input("help-btn-calendar-heatmap", "n_clicks"), Input("close-calendar-heatmap", "n_clicks")],
    [State("modal-calendar-heatmap", "is_open")],
)
def toggle_modal_calendar_heatmap(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open