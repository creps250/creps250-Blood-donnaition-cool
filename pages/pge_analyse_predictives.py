from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from app import *
from datetime import datetime
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Input, Output, State
import requests




def page_quatre(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme):
    # Styles basés sur le thème
    card_style = {
    'backgroundColor': light_theme['cardBg'] if theme == 'light' else dark_theme['cardBg'],
    'borderRadius': '15px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'padding': '20px',
    'marginBottom': '20px',
    'color': light_theme['textColor'] if theme == 'light' else dark_theme['textColor']
}
    
    header_style = {
        'textAlign': 'center', 
        'marginBottom': '30px',
        'color': light_theme['textColor'] if theme == 'light' else dark_theme['textColor'],
        'borderBottom': f'2px solid {light_theme["accentColor"] if theme == "light" else dark_theme["accentColor"]}',
        'paddingBottom': '15px'
    }
    
    section_title_style = {
        'color': light_theme['accentColor'] if theme == 'light' else dark_theme['accentColor'],
        'marginTop': '10px',
        'marginBottom': '20px',
        'fontWeight': 'bold'
    }
    
    button_style = {
        'backgroundColor': light_theme['accentColor'] if theme == 'light' else dark_theme['accentColor'],
        'color': 'white',
        'border': 'none',
        'borderRadius': '5px',
        'padding': '12px 24px',
        'fontSize': '16px',
        'fontWeight': 'bold',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'width': '100%',
        'marginTop': '20px'
    }
    
    # Créer une jauge pour visualiser l'éligibilité
    def create_gauge(value, title): 
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title, 'font': {'size': 24, 'color': plot_font_color}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': plot_font_color},
                'bar': {'color': "rgba(50, 168, 82, 0.8)" if value >= 75 else "rgba(255, 153, 51, 0.8)" if value >= 50 else "rgba(214, 39, 40, 0.8)"},
                'bgcolor': "white" if theme == 'light' else "rgba(50, 50, 50, 0.8)",
                'borderwidth': 2,
                'bordercolor': plot_font_color,
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(214, 39, 40, 0.3)'},
                    {'range': [50, 75], 'color': 'rgba(255, 153, 51, 0.3)'},
                    {'range': [75, 100], 'color': 'rgba(50, 168, 82, 0.3)'},
                ]
            }
        ))
        
        fig.update_layout(
            paper_bgcolor=plot_paper_bg,
            plot_bgcolor=plot_bg,
            font={'color': plot_font_color, 'family': 'Arial'},
            margin=dict(l=30, r=30, b=30, t=50),
            height=250
        )
        
        return fig
    
    # Créez l'image pour l'en-tête
    blood_drop_icon = html.Div([
        html.I(className="fas fa-tint fa-4x", style={'color': '#e74c3c'})
    ], style={'textAlign': 'center', 'marginBottom': '15px'})
    
    # Créer une jauge vide pour le chargement initial
    default_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        title={'text': "Probabilité d'éligibilité", 'font': {'size': 24, 'color': plot_font_color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': plot_font_color},
            'bar': {'color': "rgba(214, 39, 40, 0.8)"},
            'bgcolor': "white" if theme == 'light' else "rgba(50, 50, 50, 0.8)",
            'borderwidth': 2,
            'bordercolor': plot_font_color,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(214, 39, 40, 0.3)'},
                {'range': [50, 75], 'color': 'rgba(255, 153, 51, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(50, 168, 82, 0.3)'},
            ]
        }
    ))
    
    default_gauge.update_layout(
        paper_bgcolor=plot_paper_bg,
        plot_bgcolor=plot_bg,
        font={'color': plot_font_color, 'family': 'Arial'},
        margin=dict(l=30, r=30, b=30, t=50),
        height=250
    )
    
    return html.Div([
        # En-tête avec icône
        html.Div([
            blood_drop_icon,
            html.H1("Prédiction d'Éligibilité au Don de Sang", 
                   style={'textAlign': 'center', 'color': '#e74c3c', 'fontWeight': 'bold'})
        ], style={'marginBottom': '30px'}),

        # Conteneur principal
        dbc.Row([
            # Colonne 1: Formulaire
            dbc.Col([
                # Données démographiques
                dbc.Card([
                    dbc.CardHeader(html.H3("Données Démographiques", style=section_title_style)),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Genre", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Dropdown(
                                    id="genre",
                                    options=[
                                        {"label": "Homme", "value": "Homme"},
                                        {"label": "Femme", "value": "Femme"}
                                    ],
                                    value="Homme",
                                    style={'borderRadius': '5px'},
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label("Âge", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="age",
                                    type="number",
                                    placeholder="Âge",
                                    min=18,
                                    max=65,
                                    value=30,
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Label("Niveau d'études", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Dropdown(
                                    id="niveau_etude",
                                    options=[
                                        {"label": "Primaire", "value": "Primaire"},
                                        {"label": "Secondaire", "value": "Secondaire"},
                                        {"label": "Universitaire", "value": "Universitaire"},
                                        {"label": "Pas Précisé", "value": "Pas Précisé"},
                                        {"label": "Aucun", "value": "Aucun"}
                                    ],
                                    value="Secondaire",
                                    style={'borderRadius': '5px'},
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label("Situation Matrimoniale", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Dropdown(
                                    id="situation_matrimoniale",
                                    options=[
                                        {"label": "Célibataire", "value": "Célibataire"},
                                        #Célibataire
                                        {"label": "Marié (e)", "value": "Marié (e)"},
                                        {"label": "Divorcé(e)", "value": "Divorcé(e)"},
                                         {"label": "veuf (veuve)", "value": "veuf (veuve)"},
                                    ],
                                    value="Célibataire",
                                    style={'borderRadius': '5px'},
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Label("Religion", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Dropdown(
                                    id="religion",
                                    options=[
                                        {"label": "Chrétien (Catholique)", "value": "Chretien (Catholique)"},
                                        {"label": "Chrétien (Protestant)", "value": "Chretien (Protestant )"},
                                        {"label": "Musulman", "value": "Musulman"},
                                        {"label": "Pas Précisé", "value": "Pas Précisé"}
                                    ],
                                    value="Pas Précisé",
                                    style={'borderRadius': '5px'},
                                    className="mb-3"
                                )
                            ], width=12)
                        ]),
                        
                        # Nouveaux champs ajoutés - Ligne 1
                        dbc.Row([
                            dbc.Col([
                                html.Label("Profession", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="profession",
                                    type="text",
                                    placeholder="Profession",
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label("Nationalité", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="nationalite",
                                    type="text",
                                    placeholder="Nationalité",
                                    value="",
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Nouveaux champs ajoutés - Ligne 2
                        dbc.Row([
                            dbc.Col([
                                html.Label("Taille (cm)", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="taille",
                                    type="number",
                                    placeholder="Taille en cm",
                                    min=140,
                                    max=220,
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label("Poids (kg)", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="poids",
                                    type="number",
                                    placeholder="Poids en kg",
                                    min=45,
                                    max=150,
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Nouveaux champs ajoutés - Ligne 3
                        dbc.Row([
                            dbc.Col([
                                html.Label("Arrondissement de résidence", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="arrondissement_de_residence",
                                    type="text",
                                    placeholder="Arrondissement",
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label("Quartier de résidence", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Input(
                                    id="quartier_residence",
                                    type="text",
                                    placeholder="Quartier",
                                    style={'width': '100%', 'padding': '8px', 'borderRadius': '5px', 'border': '1px solid #ccc'},
                                    className="mb-3"
                                )
                            ], width=6)
                        ])
                    ])
                ], style=card_style),
                
                # Données médicales
                dbc.Card([
                    dbc.CardHeader(html.H3("Données Médicales", style=section_title_style)),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Taux d'hémoglobine (g/dL)", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                                dcc.Slider(
                                    id="taux_hemoglobine",
                                    min=8,
                                    max=20,
                                    step=0.1,
                                    value=13.5,
                                    marks={i: f'{i}' for i in range(8, 21, 2)},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    className="mb-4"
                                )
                            ], width=12)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Label("A déjà donné le sang", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                                dbc.RadioItems(
                                    id="a_deja_donne",
                                    options=[
                                        {"label": "Oui", "value": "Oui"},
                                        {"label": "Non", "value": "Non"}
                                    ],
                                    value="Non",
                                    inline=True,
                                    className="mb-3"
                                )
                            ], width=12)
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                html.Div(id="date_dernier_don_container", style={"display": "none"}, children=[
                                    html.Label("Date du dernier don", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Mois"),
                                            dcc.Dropdown(
                                                id="mois_dernier_don",
                                                options=[{"label": m, "value": i+1} for i, m in enumerate([
                                                    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                                                    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
                                                ])],
                                                value=1,
                                                style={'borderRadius': '5px'},
                                            )
                                        ], width=6),
                                        dbc.Col([
                                            html.Label("Année"),
                                            dcc.Dropdown(
                                                id="annee_dernier_don",
                                                options=[{"label": str(year), "value": year} for year in range(2020, 2026)],
                                                value=2024,
                                                style={'borderRadius': '5px'},
                                            )
                                        ], width=6)
                                    ])
                                ])
                            ], width=12)
                        ])
                    ])
                ], style=card_style)
            ], md=6),
            
            # Colonne 2: Résultats de prédiction
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("Résultats de la Prédiction", style=section_title_style)),
                    dbc.CardBody([
                        # Image ou animation pour le sang
                        html.Div([
                            html.Img(src="assets/blood_donor.png", style={'width': '100%', 'maxWidth': '300px', 'margin': '0 auto', 'display': 'block'}),
                        ], id="prediction-image", style={'textAlign': 'center', 'marginBottom': '20px', 'display': 'block'}),
                        
                        # Zone pour la jauge de prédiction
                        html.Div(id="gauge-container", style={'display': 'none'}, children=[
                            dcc.Graph(id="eligibility-gauge", figure=default_gauge, config={'displayModeBar': False})
                        ]),
                        
                        # Zone pour les résultats textuels
                        html.Div(id="prediction-output", style={"marginTop": "20px", 'textAlign': 'center'}),
                        
                        # Conseils et recommandations
                        html.Div(id="recommendation-section", style={'display': 'none', 'marginTop': '20px'}, children=[
                            html.H4("Conseils et Recommandations", style={'borderBottom': '1px solid #ccc', 'paddingBottom': '10px'}),
                            html.Div(id="recommendation-content")
                        ])
                    ])
                ], style=card_style)
            ], md=6)
        ]),
        
        # Bouton de prédiction
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    "Prédire l'éligibilité",
                    id="predict-button",
                    color="danger",
                    className="mt-3 mb-4",
                    style={'fontWeight': 'bold', 'padding': '12px', 'width': '100%'},
                    n_clicks=0  # Initialisation explicite à 0
                )
            ], width={"size": 6, "offset": 3})
        ]),
        html.A("Visiter la documentation de l API", href="https://api-blood-donnation.onrender.com/docs#/", target="_blank")
    ], style={'padding': '20px'})


@app.callback(
    Output("date_dernier_don_container", "style"),
    Input("a_deja_donne", "value")
)
def toggle_date_dernier_don(a_deja_donne):
    if a_deja_donne == "Oui":
        return {"display": "block", "marginBottom": "20px"}
    return {"display": "none"}


@app.callback(
    [
        Output("prediction-output", "children"),
        Output("gauge-container", "style"),
        Output("eligibility-gauge", "figure"),
        Output("recommendation-section", "style"),
        Output("recommendation-content", "children"),
        Output("prediction-image", "style")
    ],
    Input("predict-button", "n_clicks"),
    State("genre", "value"),
    State("age", "value"),
    State("niveau_etude", "value"),
    State("situation_matrimoniale", "value"),
    State("religion", "value"),
    State("taux_hemoglobine", "value"),
    State("a_deja_donne", "value"),
    State("mois_dernier_don", "value"),
    State("annee_dernier_don", "value"),
    # Nouveaux champs ajoutés
    State("profession", "value"),
    State("taille", "value"),
    State("poids", "value"),
    State("arrondissement_de_residence", "value"),
    State("quartier_residence", "value"),
    State("nationalite", "value")
)
def update_prediction(n_clicks, genre, age, niveau_etude, situation_matrimoniale, 
                      religion, taux_hemoglobine, a_deja_donne, mois_dernier_don, annee_dernier_don,
                      profession, taille, poids, arrondissement_de_residence, quartier_residence, nationalite):
    
    # Vérifier si le callback a été déclenché
    ctx = callback_context
    if not ctx.triggered:
        # Pas de déclenchement (chargement initial de la page)
        default_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=0,
            title={'text': "Probabilité d'éligibilité", 'font': {'size': 24}},
            gauge={'axis': {'range': [0, 100]}}
        ))
        default_gauge.update_layout(margin=dict(l=30, r=30, b=30, t=50), height=250)
        
        return "", {"display": "none"}, default_gauge, {"display": "none"}, "", {'textAlign': 'center', 'marginBottom': '20px', 'display': 'block'}
    
    # Vérifier si le bouton a été cliqué
    if n_clicks is None or n_clicks == 0:
        # Pas de clic sur le bouton
        default_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=0,
            title={'text': "Probabilité d'éligibilité", 'font': {'size': 24}},
            gauge={'axis': {'range': [0, 100]}}
        ))
        default_gauge.update_layout(margin=dict(l=30, r=30, b=30, t=50), height=250)
        
        return "", {"display": "none"}, default_gauge, {"display": "none"}, "", {'textAlign': 'center', 'marginBottom': '20px', 'display': 'block'}
    
    # Calculer la date du dernier don si applicable
    date_dernier_don = None
    if a_deja_donne == "Oui":
        date_dernier_don = f"{mois_dernier_don:02d}/{annee_dernier_don}"
    
    # Préparer les données pour l'API
    data = {
        "Genre": genre,
        "Age": age,
        "Niveau_etude": niveau_etude,
        "Situation_Matrimoniale": situation_matrimoniale,
        "Religion": religion,
        "Taux_hemoglobine": taux_hemoglobine,
        "A_deja_donne": a_deja_donne,
        "Date_dernier_don": date_dernier_don,
        # Nouveaux champs ajoutés
        "profession": profession,
        "Taille": taille,
        "Poids": poids,
        "Arrondissement_de_residence": arrondissement_de_residence,
        "Quartier_residence": quartier_residence,
        "Nationalite": nationalite
    }
    
    try:
        # Faire une requête à l'API de prédiction
        response = requests.post("https://api-blood-donnation.onrender.com/predict", json=data)
        result = response.json()
        
        # Calculer la probabilité pour l'affichage
        probability = result.get("probability", 0.5) * 100 if result.get("probability") is not None else 0
        
        # Créer la jauge
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability,
            title={'text': "Probabilité d'éligibilité", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "rgba(50, 168, 82, 0.8)" if probability >= 75 else 
                               "rgba(255, 153, 51, 0.8)" if probability >= 50 else 
                               "rgba(214, 39, 40, 0.8)"},
                'bgcolor': "white",
                'borderwidth': 2,
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(214, 39, 40, 0.3)'},
                    {'range': [50, 75], 'color': 'rgba(255, 153, 51, 0.3)'},
                    {'range': [75, 100], 'color': 'rgba(50, 168, 82, 0.3)'},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': probability
                }
            }
        ))
        
        gauge_fig.update_layout(
            #margin=dict(l=30, r=30, b=30, t=50),
            margin=dict(l=100, r=10, b=10, t=10),
            height=250
        )
        
        # Générer des conseils basés sur les données
        recommendations = []
        
        if not result.get("eligible", False):
            if taux_hemoglobine < 12:
                recommendations.append(
                    html.P([
                        html.I(className="fas fa-utensils mr-2", style={'marginRight': '8px', 'color': '#e74c3c'}),
                        "Améliorez votre taux d'hémoglobine en consommant des aliments riches en fer comme la viande rouge, les épinards et les lentilles."
                    ])
                )
            
            if a_deja_donne == "Oui" and annee_dernier_don == datetime.now().year and mois_dernier_don > (datetime.now().month - 3):
                recommendations.append(
                    html.P([
                        html.I(className="fas fa-calendar-alt mr-2", style={'marginRight': '8px', 'color': '#e74c3c'}),
                        "Vous devez attendre au moins 3 mois entre deux dons. Réessayez plus tard."
                    ])
                )
                
            # Nouvelles recommandations basées sur les champs ajoutés
            if poids and poids < 50:
                recommendations.append(
                    html.P([
                        html.I(className="fas fa-weight mr-2", style={'marginRight': '8px', 'color': '#e74c3c'}),
                        "Un poids minimum de 50 kg est généralement recommandé pour le don de sang."
                    ])
                )
        else:
            recommendations.append(
                html.P([
                    html.I(className="fas fa-water mr-2", style={'marginRight': '8px', 'color': '#3498db'}),
                    "Hydratez-vous bien avant votre don."
                ])
            )
            recommendations.append(
                html.P([
                    html.I(className="fas fa-utensils mr-2", style={'marginRight': '8px', 'color': '#3498db'}),
                    "Prenez un repas équilibré dans les heures précédant votre don."
                ])
            )
        
        # Construire l'affichage du résultat
        if result.get("eligible", False):
            prediction_output = html.Div([
                html.Div([
                    html.I(className="fas fa-check-circle fa-3x", style={'color': 'green', 'marginRight': '10px'}),
                    html.H3("Éligible au don de sang", style={"color": "green", "display": "inline"})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div([
                    html.P(result.get("message", "Vous êtes éligible pour donner votre sang. Merci pour votre générosité !"), 
                           style={"fontSize": "16px", "marginTop": "10px"})
                ])
            ])
        else:
            prediction_output = html.Div([
                html.Div([
                    html.I(className="fas fa-times-circle fa-3x", style={'color': 'red', 'marginRight': '10px'}),
                    html.H3("Non éligible au don de sang", style={"color": "red", "display": "inline"})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div([
                    html.P(result.get("message", "Désolé, vous n'êtes pas éligible pour le don de sang à ce moment."), 
                           style={"fontSize": "16px", "marginTop": "10px"})
                ])
            ])
        
        recommendation_style = {'display': 'block', 'marginTop': '20px'} if recommendations else {'display': 'none'}
        
        return prediction_output, {"display": "block"}, gauge_fig, recommendation_style, recommendations, {'display': 'none'}
    
    except Exception as e:
        return html.Div([
            html.H3("Erreur lors de la prédiction", style={"color": "red"}),
            html.P(str(e))
        ]), {"display": "none"}, go.Figure(), {"display": "none"}, "", {'textAlign': 'center', 'marginBottom': '20px', 'display': 'block'}