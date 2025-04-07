from packages.pkg_analyse_elegibilite import *
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from app import *
from dash_iconify import DashIconify
from dash.dependencies import Input, Output, State
from prossess_data.prossess import *
from dash import callback, Input, Output, State
from packages.pkg_kpi import *
import dash
import json


df_elig=cluster_df(data_final)
with open("Translation/traduction_analyse_eligibilite.json", "r", encoding="utf-8") as fichier:
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

def page_deux(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme,language='fr', data_final=None):
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
    translations = TRANSLATIONS[language]
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
    liste_arrondissement = data_final['Arrondissement de résidence'].unique()
    
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
                                    html.P(translations["Taux d'éligibilité global"]),
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
                                    html.P(translations["taux de don deja effectue"]),
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
                                    html.P(translations["Âge moyen des éligibles"]),
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
                                    html.P(translations["Âge moyen des donneurs"]),
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
                                    translations["Principaux facteurs d'Éligibilité et d'Indisponibilité"]
                                ], style={"display": "flex", "align-items": "center"})
                            ], width=8),
                            dbc.Col([
                                dbc.Button([
                                    translations["Indisponibilité "],
                                    DashIconify(
                                        icon="mdi:block-helper",
                                        width=20,
                                        height=20,
                                        style={"margin-left": "5px"}
                                    )
                                ], color="danger", className="mr-2", 
                                           size="sm", style={"font-size": "8px", "margin-right": "5px"}, id='princip_indisp'),
                                dbc.Button([
                                    translations["Éligibilité "],
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
                            figure=raison_indispo_plot(data=data_final, language=language),
                            responsive=True,
                            style={'height': '340px'}
                        )
                    ]),
                    # Ajout de l'icône d'aide
                    create_help_icon("princip-raison", theme, language),
                    # Modal explicatif pour ce graphique
                    create_explanatory_modal("princip-raison", translations["princip_raison_description"], theme, language)
                ], className="mb-4 shadow-sm", style={'height': '410px', 'position': 'relative', **card_style}),  # Application du style de carte avec position relative
            
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
                                html.Span(id="filter-title", children=translations["Filtre(Sexe,Status Matrimonial)"])
                            ], style={"display": "flex", "align-items": "center"})
                        ], width=9),
                        dbc.Col([
                            # Ajout du bouton de bascule avec icône dynamique
                            dbc.Button([
                                html.Div(id="toggle-icon", children=[
                                    DashIconify(
                                        icon="mdi:toggle-switch-off-outline",
                                        width=40,
                                        height=10,
                                        style={"margin-right": "5px", "color": "#8B5CF6"}
                                    )
                                ]),
                                translations["Changer filtre"]
                            ], 
                            id="toggle-filter-btn", 
                            color="light", 
                            size="sm", 
                            className="float-end",
                            style={"font-size": "10px"})
                        ], width=3, className="text-end")
                    ])
                ]),
                
                dbc.CardBody([
                    # Conteneur pour les filtres Sexe/Status Matrimonial
                    html.Div(id="sexe-status-filters", children=[
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='sexe_list',
                                    options=[
                                        {'label': translations['Homme'], 'value': 'Homme'},
                                        {'label': translations['Femme'], 'value': 'Femme'},
                                        
                                    ],
                                    clearable=False,
                                    value=[liste_sexe[0]],
                                    style=style_dropdow,
                                    multi=True
                                ),
                            ], width=6),
                            
                            dbc.Col([
                                dcc.Dropdown(
                                    id="statusmatri",
                                    options=[
                                        {"label": translations['Marié (e)'], "value": 'Marié (e)'},
                                        {"label": translations['Célibataire'], "value": 'Célibataire'},
                                        {"label": translations['Divorcé(e)'], "value": 'Divorcé(e)'},
                                        {"label": translations['veuf (veuve)'], "value": 'veuf (veuve)'}
                                    ],
                                    clearable=False,
                                    value='Marié (e)',  # Valeur par défaut
                                    style=style_dropdow,
                                    multi=True  # Dropdown simple, pas multi-sélection
                                ),
                            ], width=6)
                        ])
                    ], style={"display": "block"}),
                    
                    # Conteneur pour le filtre Arrondissement (initialement caché)
                    html.Div(id="arrondissement-filter", children=[
                        dcc.Dropdown(
                            id='arrondissement_list',
                            options=[
                                {'label': i, 'value': i} for i in liste_arrondissement
                            ],
                            clearable=False,
                            value=[liste_arrondissement[0]],
                            style={**style_dropdow, 'width': '100%'},
                            multi=True
                        )
                    ], style={"display": "none"})
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
                                    translations["Autres Facteurs"]
                                ], style={"display": "flex", "align-items": "center"})
                            ], width=8),
                            dbc.Col([
                                html.Div([  # Ajout d'un conteneur div avec display flex
                                    dbc.Button([
                                        translations["Indisponibilité "],
                                        DashIconify(
                                            icon="mdi:block-helper",
                                            width=20,
                                            height=5,
                                            style={"margin-left": "5px"}
                                        )
                                    ], color="danger", className="mr-2", size="sm", id='autre_indispo',
                                    style={"font-size": "8px", "margin-right": "5px"}),  # Ajout d'une marge droite
                                    dbc.Button([
                                        translations["Éligibilité "],
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
                            figure=return_wordmap_indispo(data=data_final, language=language),
                            responsive=True,
                            style={'height': '460px'}  # Ajout d'une hauteur pour le graphique
                        )
                    ], style={'height': '510px'}),
                    # Ajout de l'icône d'aide
                    create_help_icon("autre-raison", theme, language),
                    # Modal explicatif pour ce graphique
                    create_explanatory_modal("autre-raison", translations["autre_raison_description"], theme, language)
                ], className="mb-4 shadow-sm", style={'position': 'relative', **card_style})  # Application du style de carte
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
                        translations["Analyse de l'éligibilité"]
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
                                      eligibility_column='ÉLIGIBILITÉ AU DON.',
                                      language=language),
                            responsive=True,
                            style={'height': '470px'}
                        )
                    ]),
                ]),
                # Ajout de l'icône d'aide
                create_help_icon("eligibility-factors", theme, language),
                # Modal explicatif pour ce graphique
                create_explanatory_modal("eligibility-factors", translations["eligibility_factors_description"], theme, language)
            ], className="h-100 shadow-sm", style={'position': 'relative', **card_style})
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
                            translations["Caractérisation des personnes éligibles"]
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
                            figure=plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'], language=language), # Vous devrez créer cette fonction
                            responsive=True,
                            style={'height': '460px','margin-top':'0px'}
                        )
                    ])
                    
                    
                ]),
                # Ajout de l'icône d'aide
                create_help_icon("eligib-demograp", theme, language),
                # Modal explicatif pour ce graphique
                create_explanatory_modal("eligib-demograp", translations["eligib_demograp_description"], theme, language)
            ], className="h-100 shadow-sm", style={'position': 'relative', **card_style})
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
                        translations["Analyses Donneurs Effectifs"]
                    ], style={"display": "flex", "align-items": "center", "font-weight": "bold"}),
                    html.Div([
                        dbc.Button([
                            DashIconify(
                                icon="mdi:view-dashboard-variant",
                                width=16,
                                height=16,
                                style={"margin-right": "5px", "vertical-align": "middle"}
                            ),
                            translations["Hiérarchie"]
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
                        figure=create_treemap(df=df_volontaire, language=language),  
                        responsive=True,
                        style={'height': '460px'}
                    )
                ])
            ]),
            # Ajout de l'icône d'aide
            create_help_icon("donneurs-effectifs", theme, language),
            # Modal explicatif pour ce graphique
            create_explanatory_modal("donneurs-effectifs", translations["donneurs_effectifs_description"], theme, language)
        ], className="h-100 shadow-sm", style={'position': 'relative', **card_style})
    ], md=12)  # Full width
], className="mb-4")    
            
    ])
    
# Callback pour basculer entre les modes de filtre
@app.callback(
    [Output("filter-title", "children"),
     Output("sexe-status-filters", "style"),
     Output("arrondissement-filter", "style"),
     Output("toggle-icon", "children")],
    [Input("toggle-filter-btn", "n_clicks")],
    [State("filter-title", "children"),
     State("language-store", "data")],
)
def toggle_filter_mode(n_clicks, current_title, language):
    """
    Bascule entre les modes de filtre (Sexe/Status Matrimonial et Arrondissement).
    Met également à jour l'icône du bouton pour refléter l'état actuel.
    
    Args:
        n_clicks (int): Nombre de clics sur le bouton de bascule
        current_title (str): Titre actuel du filtre
        language (str): Langue actuelle de l'interface
        
    Returns:
        tuple: (Nouveau titre, style pour sexe-status-filters, style pour arrondissement-filter, nouvelle icône)
    """
    translations = TRANSLATIONS[language]
    
    if n_clicks is None:
        # État initial - mode Sexe/Status (off)
        return (
            translations["Filtre(Sexe,Status Matrimonial)"], 
            {"display": "block"}, 
            {"display": "none"}, 
            DashIconify(
                icon="mdi:toggle-switch-off-outline",
                width=20,
                height=20,
                style={"margin-right": "5px", "color": "#8B5CF6"}
            )
        )
    
    if current_title == translations["Filtre(Sexe,Status Matrimonial)"]:
        # Basculer vers filtre Arrondissement (on)
        return (
            translations["Filtre(Arrondissement)"], 
            {"display": "none"}, 
            {"display": "block"}, 
            DashIconify(
                icon="mdi:toggle-switch",
                width=20,
                height=20,
                style={"margin-right": "5px", "color": "#8B5CF6"}
            )
        )
    else:
        # Basculer vers filtre Sexe/Status Matrimonial (off)
        return (
            translations["Filtre(Sexe,Status Matrimonial)"], 
            {"display": "block"}, 
            {"display": "none"}, 
            DashIconify(
                icon="mdi:toggle-switch-off-outline",
                width=20,
                height=20,
                style={"margin-right": "5px", "color": "#8B5CF6"}
            )
        )
    
# Callback pour les boutons indispo et éligibilité secondaires
@app.callback(
    Output("autre-raison", "figure"),
    Output("autre_indispo", "disabled"),
    Output("autre_elegi", "disabled"),
    [
        Input("autre_indispo", "n_clicks"),
        Input("autre_elegi", "n_clicks"),
        Input('sexe_list', 'value'),
        Input('arrondissement_list', 'value'),
        Input('filter-title', 'children'),
    ],
    [
        State("autre_indispo", "disabled"),
        State("autre_elegi", "disabled"),
        State("language-store", "data")
    ],
    prevent_initial_call=False
)
def mettre_a_jour_figure_autre(n_clicks_indispo, n_clicks_elegi, value_sexe, value_arrond, current_filter, indispo_disabled, elegi_disabled, language):
    """
    Met à jour le graphique "autre-raison" en fonction des boutons "autre_indispo" et "autre_elegi" et des filtres actifs.
    """
    
    translations = TRANSLATIONS[language]
    ctx = callback_context
    
    # Déterminer les données filtrées en fonction du mode de filtre actif
    if current_filter == translations["Filtre(Sexe,Status Matrimonial)"]:
        filtered_data = data_final[data_final['Genre'].isin(value_sexe)]
    else:
        if isinstance(value_arrond, str):
            value_arrond = [value_arrond]
        filtered_data = data_final[data_final['Arrondissement de résidence'].isin(value_arrond)]
    
    # Si pas de déclencheur défini (charge initiale)
    if not ctx.triggered:
        # Afficher le graphique par défaut
        return return_wordmap_indispo(data=filtered_data, language=language), True, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Si c'est un changement de filtre
    if button_id in ["sexe_list", "arrondissement_list", "filter-title"]:
        # On vérifie l'état actuel pour déterminer quel graphique est affiché
        if indispo_disabled:
            # Le bouton indispo est désactivé = mode indisponibilité actif
            return return_wordmap_indispo(data=filtered_data, language=language), True, False
        elif elegi_disabled:
            # Le bouton éligibilité est désactivé = mode éligibilité actif
            return return_wordmap(data=filtered_data, language=language), False, True
        else:
            # Aucun bouton sélectionné, on utilise le mode par défaut
            return return_wordmap_indispo(data=filtered_data, language=language), True, False
    
    # Si c'est un clic sur un bouton
    elif button_id == "autre_indispo":
        return return_wordmap_indispo(data=filtered_data, language=language), True, False
    elif button_id == "autre_elegi":
        return return_wordmap(data=filtered_data, language=language), False, True
    
    # Par défaut, mode indisponibilité
    return return_wordmap_indispo(data=filtered_data, language=language), True, False

# Callback pour les boutons indispo et éligibilité principaux
@app.callback(
    Output("princip-raison", "figure"),
    Output("princip_indisp", "disabled"),
    Output("princip_eleg", "disabled"),
    [
        Input("princip_indisp", "n_clicks"),
        Input("princip_eleg", "n_clicks"),
        Input('sexe_list', 'value'),
        Input('statusmatri', 'value'),
        Input('arrondissement_list', 'value'),
        Input('filter-title', 'children')
    ],
    [
        State("princip_indisp", "disabled"),
        State("princip_eleg", "disabled"),
        State("language-store", "data")
    ],
    prevent_initial_call=False
)
def mettre_a_jour_figure_princip(n_clicks_indispo, n_clicks_elegi, value_sexe, value_status, value_arrond, current_filter, indispo_disabled, elegi_disabled, language):
    """
    Mettre à jour le graphique principal en fonction des boutons indisponibilité et éligibilité, ainsi que des filtres actifs.
    """
    
    translations = TRANSLATIONS[language]
    ctx = callback_context
    
    # Déterminer les données filtrées en fonction du mode de filtre actif
    if current_filter == translations["Filtre(Sexe,Status Matrimonial)"]:
        if isinstance(value_status, str):
            value_status = [value_status]
        filtered_data = data_final[
            (data_final['Genre'].isin(value_sexe)) & 
            (data_final['Situation Matrimoniale (SM)'].isin(value_status))
        ]
    else:
        if isinstance(value_arrond, str):
            value_arrond = [value_arrond]
        filtered_data = data_final[
            data_final['Arrondissement de résidence'].isin(value_arrond)
        ]
    
    # Si pas de déclencheur défini (charge initiale)
    if not ctx.triggered:
        # Afficher le graphique par défaut
        return raison_indispo_plot(data=filtered_data, language=language), True, False
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Si c'est un changement de filtre
    if button_id in ["sexe_list", "statusmatri", "arrondissement_list", "filter-title"]:
        # On vérifie l'état actuel pour déterminer quel graphique est affiché
        if indispo_disabled:
            # Le bouton indispo est désactivé = mode indisponibilité actif
            return raison_indispo_plot(data=filtered_data, language=language), True, False
        elif elegi_disabled:
            # Le bouton éligibilité est désactivé = mode éligibilité actif
            return plot_elegibi_raison_elegibi(data=filtered_data, language=language), False, True
        else:
            # Aucun bouton sélectionné, on utilise le mode par défaut
            return raison_indispo_plot(data=filtered_data, language=language), True, False
    
    # Si c'est un clic sur un bouton
    elif button_id == "princip_indisp":
        return raison_indispo_plot(data=filtered_data, language=language), True, False
    elif button_id == "princip_eleg":
        return plot_elegibi_raison_elegibi(data=filtered_data, language=language), False, True
    
    # Par défaut, mode indisponibilité
    return raison_indispo_plot(data=filtered_data, language=language), True, False

@app.callback(
    [Output('pourcentage_eligi', 'children'),  
     Output('taux_don', 'children'),          
     Output('age_moy_elig', 'children'),     
     Output('age_don', 'children')],         
    [Input('sexe_list', 'value'),            
     Input('statusmatri', 'value'),
     Input('arrondissement_list', 'value'),
     Input('filter-title', 'children')]        
)
def update_metrics(selected_sexe, selected_status, selected_arrond, current_filter):
    """
    Mise à jour des indicateurs de performance en fonction des filtres actifs.
    """
    
    # Déterminer les données filtrées en fonction du mode de filtre actif
    if current_filter == "Filtre(Sexe,Status Matrimonial)" or current_filter == "Filter(Gender,Marital Status)":
        if not isinstance(selected_status, list):
            selected_status = [selected_status]
        if not isinstance(selected_sexe, list):
            selected_sexe = [selected_sexe]    
            
        filtered_data = data_final[
            (data_final['Genre'].isin(selected_sexe)) & 
            (data_final['Situation Matrimoniale (SM)'].isin(selected_status))
        ]
    else:
        if not isinstance(selected_arrond, list):
            selected_arrond = [selected_arrond]
            
        filtered_data = data_final[
            data_final['Arrondissement de résidence'].isin(selected_arrond)
        ]
    
    # Calculer les nouvelles valeurs
    a = str(pourcentage_eligibilite(filtered_data)) + ' %'
    b = str(taux_don(filtered_data)) + ' %'
    c = str(age_moyen_elig(filtered_data)) + ' Ans'
    d = str(age_moyen_don(filtered_data)) + ' Ans'
    
    # Retourner les nouvelles valeurs pour mise à jour
    return a, b, c, d

# Callbacks pour les icônes d'aide et les modaux
@app.callback(
    Output("modal-princip-raison", "is_open"),
    [Input("help-btn-princip-raison", "n_clicks"), Input("close-princip-raison", "n_clicks")],
    [State("modal-princip-raison", "is_open")],
)
def toggle_modal_princip_raison(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-autre-raison", "is_open"),
    [Input("help-btn-autre-raison", "n_clicks"), Input("close-autre-raison", "n_clicks")],
    [State("modal-autre-raison", "is_open")],
)
def toggle_modal_autre_raison(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-eligibility-factors", "is_open"),
    [Input("help-btn-eligibility-factors", "n_clicks"), Input("close-eligibility-factors", "n_clicks")],
    [State("modal-eligibility-factors", "is_open")],
)
def toggle_modal_eligibility_factors(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-eligib-demograp", "is_open"),
    [Input("help-btn-eligib-demograp", "n_clicks"), Input("close-eligib-demograp", "n_clicks")],
    [State("modal-eligib-demograp", "is_open")],
)
def toggle_modal_eligib_demograp(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

@app.callback(
    Output("modal-donneurs-effectifs", "is_open"),
    [Input("help-btn-donneurs-effectifs", "n_clicks"), Input("close-donneurs-effectifs", "n_clicks")],
    [State("modal-donneurs-effectifs", "is_open")],
)
def toggle_modal_donneurs_effectifs(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

# Callback pour les boutons Clusters et Profils
@app.callback(
    Output('eligibility-factors-chart', 'figure'),
    [Input('btn-clusters', 'n_clicks'),
     Input('btn-profils', 'n_clicks')],
    [State('language-store', 'data')],
    prevent_initial_call=True
)
def update_eligibility_chart(clusters_clicks, profils_clicks, language):
    """
    Met à jour le graphique d'éligibilité en fonction du bouton cliqué.
    
    Args:
        clusters_clicks (int): Nombre de clics sur le bouton Clusters
        profils_clicks (int): Nombre de clics sur le bouton Profils
        language (str): Langue actuelle ('fr' ou 'en')
    
    Returns:
        plotly.graph_objs._figure.Figure: La figure mise à jour
    """
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if triggered_id == 'btn-clusters':
        # Afficher les clusters
        return plot_cluster_distribution(df=cluster_df(data=data_final), language=language)
    else:
        # Afficher les profils (comportement par défaut)
        return plot_combined_eligibility_heatmap(
            df=cluster_df(data=data_final), 
            numeric_vars=['Age'],
            cat_vars=['Genre', 'Situation Matrimoniale (SM)', 'Religion', "Niveau d'etude", 'A-t-il (elle) déjà donné le sang'],
            eligibility_column='ÉLIGIBILITÉ AU DON.',
            language=language
        )

# Callback pour les boutons Page 1 et Page 2
@app.callback(
    Output('eligib-demograp', 'figure'),
    [Input('page1', 'n_clicks'),
     Input('page2', 'n_clicks')],
    [State('language-store', 'data')],
    prevent_initial_call=True
)
def update_eligib_demograp(page1_clicks, page2_clicks, language):
    """
    Met à jour le diagramme de Sankey en fonction du bouton cliqué.
    
    Args:
        page1_clicks (int): Nombre de clics sur le bouton Page 1
        page2_clicks (int): Nombre de clics sur le bouton Page 2
        language (str): Langue actuelle ('fr' ou 'en')
    
    Returns:
        plotly.graph_objs._figure.Figure: La figure mise à jour
    """
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if triggered_id == 'page1':
        # Afficher la page 1 - Religion
        return plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'], language=language)
    elif triggered_id == 'page2':
        # Afficher la page 2 - Niveau d'études
        return plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', "Niveau d'etude"], language=language)
    
    # Par défaut, afficher la page 1
    return plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'], language=language)

# Callback pour les boutons Hiérarchie et Age vs sexe
@app.callback(
    Output('donneurs-effectifs-graph', 'figure'),
    [Input('btn-hierarchie', 'n_clicks'),
     Input('btn-age-femme', 'n_clicks')],
    [State('language-store', 'data')],
    prevent_initial_call=True
)
def update_donneurs_effectifs(hierarchie_clicks, age_femme_clicks, language):
    """
    Met à jour le graphique des donneurs effectifs en fonction du bouton cliqué.
    
    Args:
        hierarchie_clicks (int): Nombre de clics sur le bouton Hiérarchie
        age_femme_clicks (int): Nombre de clics sur le bouton Age vs sexe
        language (str): Langue actuelle ('fr' ou 'en')
    
    Returns:
        plotly.graph_objs._figure.Figure: La figure mise à jour
    """
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if triggered_id == 'btn-hierarchie':
        # Afficher la hiérarchie des donneurs
        return create_treemap(df=df_volontaire, language=language)
    elif triggered_id == 'btn-age-femme':
        # Afficher la distribution de l'âge par sexe
        return create_age_distribution(df=df_volontaire, language=language)
    
    # Par défaut, afficher la hiérarchie
    return create_treemap(df=df_volontaire, language=language)