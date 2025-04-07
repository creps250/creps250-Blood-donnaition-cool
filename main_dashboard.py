import dash
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify as Icon
from pages.pge_repartition_geo import *
from pages.pge_analyse_elgibillite import *
from pages.pge_evolution_temporelle import *
from pages.pge_analyse_predictives import *
from pages.pge_authentication import page_authentification 
from app import *
import os
import base64
import google.generativeai as genai
import random
import markdown2
import json
from utilss.functionality import *
from about_us import page_about_us
from utilss.auth_utils import *
from pages.pge_administration import *


print("py")
# Configuration de l'API Gemini
GEMINI_API_KEY = 'AIzaSyC_0t7ijizDdZpR_riH4bftsKDQSCOgjrA'
genai.configure(api_key=GEMINI_API_KEY)
auth_st = {'authenticated': False, 'is_admin': False}

# Initialisation du modèle Gemini
model = genai.GenerativeModel('models/gemini-2.0-flash-thinking-exp-01-21')


    
    
    
# Conserver les routes de navigation originales mais SANS les pages About Us et Administration
PAGES = {
    "fr": {
        "/": {"name": "Se connecter au Dashboard", "icon": "carbon:map"},
        "/repartition-geographique": {"name": "Répartition Géographique", "icon": "carbon:map"},
        "/analyse-elegibilite": {"name": "Analyse d'Éligibilité", "icon": "carbon:chart-evaluation"},
        "/evolution-temporelle": {"name": "Efficacite des campagnes", "icon": "carbon:chart-line"},
        "/analyse-predictive": {"name": "Analyse Prédictive", "icon": "carbon:forecast-lightning"}
        # Retiré les entrées "/about-us" et "/administration" pour qu'elles n'apparaissent pas dans la navigation
    },
    "en": {
        "/": {"name": "connection to Dashboard", "icon": "carbon:map"},
        "/repartition-geographique": {"name": "Geographic Distribution", "icon": "carbon:map"},
        "/analyse-elegibilite": {"name": "Eligibility Analysis", "icon": "carbon:chart-evaluation"},
        "/evolution-temporelle": {"name": "Campaign Effectiveness", "icon": "carbon:chart-line"},
        "/analyse-predictive": {"name": "Predictive Analysis", "icon": "carbon:forecast-lightning"}
        # Retiré les entrées "/about-us" et "/administration" pour qu'elles n'apparaissent pas dans la navigation
    }
}

with open("Translation/traduction_main_dashboard.json", "r", encoding="utf-8") as fichier:
    TRANSLATIONS = json.load(fichier)

dark_blue_theme = {
    'backgroundColor': '#0f172a',  
    'color': 'white',
    'headerBg': 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)',  
    'headerColor': 'white',
    'footerBg': '#0f172a',
    'footerColor': '#cccccc',
    'cardShadow': '0 4px 6px rgba(0,0,0,0.3)',
    'cardBorder': '1px solid rgba(255,255,255,0.1)',
    'highlightColor': '#ff5757',  # Rouge pour les valeurs importantes
    'accentColor': '#60a5fa',  # Bleu clair pour les accents
    'successColor': '#4ade80',  # Vert pour les indicateurs positifs
    'warningColor': '#fbbf24',  # Jaune/Orange pour les avertissements
    'chartLine': '#ff5757',  # Couleur de la ligne du graphique
    'chartGrid': '#334155',  # Couleur de la grille du graphique
    'cardBg': '#0A3160',
    'textColor':'white',
    'accentColor':'white'
}

# Conserver la fonction originale des boutons de navigation
def create_nav_buttons(current_path, language='fr'):
    """
    Crée les boutons de navigation avec un style dégradé et des icônes.

    Args:
        current_path (str): Le chemin URL actuel qui détermine quel bouton doit être mis en évidence.
        language (str): La langue actuelle ('fr' ou 'en') pour traduire les noms des pages.

    Returns:
        list: Une liste de boutons dbc.Button stylisés pour la barre de navigation.
    """
    buttons = []
    for path, info in list(PAGES[language].items())[1:]:  # Commence à 1 pour sauter l'élément "/"
        is_active = path == current_path
        
        # Style plus professionnel et apaisant
        button_style = {
            'background': 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)' if is_active else 'white',
            'color': 'white' if is_active else '#9e2b2b',
            'border': '1px solid #9e2b2b',
            'marginRight': '5px',
            'fontWeight': '500',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)' if is_active else 'none',
            'transition': 'all 0.3s ease',
            'borderRadius': '4px',
            'display': 'flex',
            'alignItems': 'center',
            'textColor':'black'
        }
        
        # Traduction du nom de la page
        page_name = TRANSLATIONS[language].get(info["name"], info["name"])
        
        # Création du bouton avec icône
        button = dbc.Button(
            [
                Icon(
                    icon=info["icon"],
                    width=16,
                    height=16,
                    style={"marginRight": "5px"}
                ),
                page_name
            ],
            style=button_style,
            size="sm",
            className="mx-1",
            href=path,
            id=f"btn-{path.replace('/', '')}"
        )
        buttons.append(button)
    return buttons

# Conserver le thème original pour les boutons et le header
light_theme = {
    'backgroundColor': 'lightgray',
    'color': 'black',
    'cardBg': 'white',
    'headerBg': 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)',  # Dégradé rouge plus doux
    'headerColor': 'white',
    'footerBg': 'lightgray',
    'footerColor': 'black',
    'cardShadow': '0 2px 5px rgba(0,0,0,0.1)',
    'textColor':'black',
    'accentColor':'black'
}

# Créer un écran de chargement créatif avec animation pour les transitions entre pages
def create_loading_screen(theme, language="fr"):
    """
    Crée un écran de chargement créatif avec une animation sur le thème du don de sang.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        language (str): La langue actuelle ('fr' ou 'en').
        
    Returns:
        html.Div: Composant Dash représentant l'écran de chargement.
    """
    translations = TRANSLATIONS[language]
    
    # Sélectionner aléatoirement un message pour l'affichage lors du chargement
    loading_messages = [
        translations["Chargement des données..."],
        translations["Préparation de votre visualisation..."],
        translations["Analyse en cours..."],
        translations["Un instant, nous préparons votre vue..."]
    ]
    
    # Messages inspirants sur le don de sang
    inspirational_messages = [
        translations["Votre sang est précieux"],
        translations["Votre don peut sauver des vies"],
        translations["Chaque goutte compte"],
        translations["Donnez du sang, donnez la vie"]
    ]
    
    bg_color = '#0f172a' if theme == 'dark' else 'white'
    text_color = 'white' if theme == 'dark' else '#c42e2e'
    
    return html.Div([
        html.Div([
            # Animation d'une goutte de sang
            html.Div([
                # Goutte principale
                html.Div(className="blood-drop"),
                
                # Petites gouttes d'éclaboussure
                html.Div(className="blood-splash splash1"),
                html.Div(className="blood-splash splash2"),
                html.Div(className="blood-splash splash3"),
                html.Div(className="blood-splash splash4"),
                html.Div(className="blood-splash splash5"),
            ], className="blood-container"),
            
            # Texte de chargement
            html.H3(id="loading-main-text", 
                    children=random.choice(loading_messages),
                    style={"color": text_color, "marginTop": "20px", "textAlign": "center"}),
            
            # Message inspirant
            html.Div(id="loading-inspirational-text",
                     children=random.choice(inspirational_messages),
                     style={"color": text_color, "opacity": "0.8", "fontSize": "1.2rem", 
                            "marginTop": "10px", "textAlign": "center", "fontStyle": "italic"})
        ], className="loading-content")
    ], id="loading-overlay", style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "100%",
        "height": "100%",
        "backgroundColor": bg_color,
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "zIndex": "9999",
        "opacity": "0",  # Commence invisible
        "transition": "opacity 0.3s ease-in-out",
        "pointerEvents": "none"  # Ne bloque pas les clics quand invisible
    })

## Layout - Conserver le header et les marges originales
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    dcc.Store(id='theme-store', data='dark'),
    dcc.Store(id='language-store', data='fr'),
    dcc.Store(id='loading-state', data={'is_loading': False, 'from': None, 'to': None}),
    dcc.Store(id='previous-url', data=None),
    dcc.Store(id='auth-state', data={'authenticated': False, 'email': None, 'is_admin': False}),

    # Nouveau composant Store pour le suivi de la traduction
    dcc.Store(id='translation-status', data={'initiated': False, 'completed': False}),

    # Nouveaux composants pour la gestion de l'animation
    dcc.Interval(id='language-change-interval', interval=700, n_intervals=0, disabled=True),
    dcc.Store(id='translation-progress', data={'current': 0, 'total': 10, 'messages': []}),
    
    # Nouvel écran de chargement créatif
    html.Div(id='loading-container'),
    
    # Interval pour simuler un temps minimal de chargement
    dcc.Interval(id='loading-interval', interval=1200, n_intervals=0, disabled=True),
    
    # Header - Conservé tel quel
    html.Div([
        html.Div([
            html.Div([
                # Icône à gauche
                html.Img(
                    src="/assets/image_proj/blood_donation_icon.png",  # Ajoutez cette image dans un dossier 'assets'
                    height="40px",
                    style={'marginRight': '15px', 'display': 'inline-block', 'verticalAlign': 'middle'}
                ),
                html.H1(id="page-title", className="mb-0", style={'fontWeight': '600', 'display': 'inline-block', 'verticalAlign': 'middle'})
            ], className="col-md-6 d-flex align-items-center"),
            
            html.Div([
                html.Div([
                    html.Div(id="nav-buttons", className="d-flex justify-content-end align-items-center"),
                    
                    html.Div([
                        dbc.Button(
                            [
                                Icon(
                                    id="theme-icon",
                                    icon="ph:moon",
                                    width=16,
                                    height=16,
                                    style={"marginRight": "5px"}
                                ),
                                html.Span(id="theme-text")
                            ],
                            id="theme-toggle",
                            className="ml-2",
                            size="sm",
                            style={'marginLeft': '10px', 'marginRight': '10px', 'background': 'transparent', 'color': 'white', 'border': '1px solid rgba(255,255,255,0.5)', 'borderRadius': '4px'}
                        ),
                        #Bouton de langue
                        dbc.Button(
                            [
                                Icon(
                                    id="language-icon",
                                    icon="mdi:translate",
                                    width=16,
                                    height=16,
                                    style={"marginRight": "5px"}
                                ),
                                html.Span(id="language-text", children="FR")
                            ],
                            id="language-toggle",
                            className="ml-2",
                            size="sm",
                            style={'background': 'transparent', 'color': 'white', 'border': '1px solid rgba(255,255,255,0.5)', 'borderRadius': '4px'}
                        ),
                        html.A(
                        html.Button(
                            Icon(
                                icon="mdi:download",  # Download icon
                                width=24,
                                height=24,
                                style={
                                    'color': 'white'
                                }
                            ),
                            id='download-btn', 
                            style={
                                'position': 'fixed',
                                'bottom': '200px',  # Positioned above the Excel upload button
                                'right': '20px',
                                'zIndex': '1000',
                                'backgroundColor': '#6c757d',  # Neutral gray color
                                'borderRadius': '50%',
                                'width': '50px',
                                'height': '50px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'border': 'none',
                                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                                'cursor': 'pointer'
                            },title='Telecharger le rapport'
                        ),
                        target='_self',
                        href='/assets/rapport.pdf',
                        download='rapport.pdf',
                        id='download-link',
                    ),
                        
                        # New File Upload Button
                    dcc.Upload(
                        id='upload-excel',
                        children=html.Button(
                            Icon(
                                icon="mdi:file-excel-outline",  # Excel file icon
                                width=24,
                                height=24,
                                style={
                                    'color': 'white'
                                }
                            ),
                            style={
                                'position': 'fixed',
                                'bottom': '140px',  # Positioned above the other buttons
                                'right': '20px',
                                'zIndex': '1000',
                                'backgroundColor': '#217346',  # Excel green color
                                'borderRadius': '50%',
                                'width': '50px',
                                'height': '50px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'border': 'none',
                                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                                'cursor': 'pointer'
                            },title='mettre a jour la base de donnees'
                        ),
                        multiple=False,  # Allow only single file upload
                        accept='.xlsx, .xls, .csv'  # Limit to Excel file types
                    ),
                    
                    html.A(
                    html.Button(
                        Icon(
                            icon="mdi:file-document-edit-outline",  # Icône de formulaire
                            width=24,
                            height=24,
                            style={
                                'color': 'white'
                            }
                        ),
                        id='form-btn', 
                        style={
                            'position': 'fixed',
                            'bottom': '80px',  # Décalé de 60px par rapport au bouton de chatbot
                            'right': '20px',
                            'zIndex': '1000',
                            'backgroundColor': '#28a745',  # Vert pour différencier du bouton de chatbot
                            'borderRadius': '50%',
                            'width': '50px',
                            'height': '50px',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'border': 'none',
                            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                            'cursor': 'pointer'
                        }
                    ),
                    href='https://ee.kobotoolbox.org/x/V0ByU4TJ',
                    target='_blank' , # Ouvre dans un nouvel onglet
                    title='Formulaire de don de sang'
                ),
                    
                html.Button(
                    Icon(
                        icon="mdi:robot-outline",  # Une icône de robot/IA
                        width=24,
                        height=24,
                        style={
                            'color': 'white'
                        }
                    ),
                    id='open-ai-frame-btn', 
                    n_clicks=0,
                    style={
                        'position': 'fixed',
                        'bottom': '20px', 
                        'right': '20px',
                        'zIndex': '1000',
                        'backgroundColor': '#007bff',
                        'borderRadius': '50%',
                        'width': '50px',
                        'height': '50px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'border': 'none',
                        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                        'cursor': 'pointer'
                    },
                    title='Ouvrir le chatbot IA'
                ),
                    
                ], className="d-flex align-items-center ml-3")
            ], className="d-flex justify-content-end align-items-center h-100")
        ], className="col-md-6"),
        html.Div(
            id='custom-modal',
            style={
                'position': 'fixed',
                'top': '50%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'backgroundColor': 'white',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'zIndex': '1100',
                'display': 'none',
                'textAlign': 'center',
                'width': '300px'
            },
            children=[
                html.Div(id='modal-content', style={'marginBottom': '15px'}),
                html.Button(
                    'OK', 
                    id='modal-close-btn', 
                    style={
                        'backgroundColor': '#28a745',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'borderRadius': '5px',
                        'cursor': 'pointer'
                    }
                )
            ]
        ),
        
        # Modal pour la confirmation de changement de langue
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="language-confirm-title")),
                dbc.ModalBody(id="language-confirm-body"),
                dbc.ModalFooter([
                    dbc.Button(
                        id="language-confirm-no", 
                        className="ms-auto", 
                        n_clicks=0
                    ),
                    dbc.Button(
                        id="language-confirm-yes", 
                        color="primary", 
                        n_clicks=0
                    ),
                ]),
            ],
            id="language-confirm-modal",
            is_open=False,
        ),
        
        # Modal de chargement pour le changement de langue - VERSION AMÉLIORÉE
        dbc.Modal(
            [
                dbc.ModalBody([
                    html.Div(
                        [
                            # Animation personnalisée pour le changement de langue
                            html.Div([
                                html.Div(className="translation-globe"),
                                html.Div(className="translation-particles particle1"),
                                html.Div(className="translation-particles particle2"),
                                html.Div(className="translation-particles particle3"),
                                html.Div(className="translation-particles particle4"),
                            ], className="translation-animation"),
                            
                            html.P(id="language-loading-text", className="mt-3 mb-3"),
                            
                            # Barre de progression
                            dbc.Progress(id="translation-progress-bar", value=0, className="mb-3", 
                                        style={"height": "10px", "borderRadius": "5px"}),
                            
                            # Message de statut qui change
                            html.P(id="translation-status-message", className="fst-italic text-muted")
                        ],
                        className="text-center"
                    )
                ]),
            ],
            id="language-loading-modal",
            is_open=False,
            backdrop="static",
            keyboard=False,
            centered=True,
        )
        
    ], className="row align-items-center")
    ], id='header', style={'padding': '15px', 'position': 'fixed', 'top': '0', 'width': '100%', 'zIndex': '1000'}),
    
    
    html.Div(id="header-spacer", style={'height': '80px'}),
    
    # Contenu principal - Conserver le container original
    html.Div(id="page-content", className="container mt-4"),
    
    # Footer
    html.Div(id="footer", className="mt-5 py-4", style={
        'width': '100%',
        'position': 'relative',
        'bottom': '0',
        'textAlign': 'center'
    }),
    
    # Cadre IA
    html.Div([
        html.Div([
            html.H2('NK-STAT Assistant IA ', style={'color': '#333', 'borderBottom': '2px solid #007bff', 'paddingBottom': '10px'}),
            
            html.Div(
                id='conversation-container', 
                style={
                    'height': '400px', 
                    'overflowY': 'auto', 
                    'marginBottom': '10px',
                    'border': '1px solid #ddd',
                    'padding': '10px',
                    'backgroundColor': '#f9f9f9'
                }
            ),
            
            html.Div([
                dcc.Input(
                    id='user-input', 
                    type='text', 
                    placeholder='Posez votre question...',
                    style={
                        'width': '80%', 
                        'marginRight': '10px',
                        'padding': '8px',
                        'borderRadius': '4px',
                        'border': '1px solid #ddd'
                    }
                ),
                
                html.Button('Envoyer', id='send-btn', n_clicks=0, style={
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'border': 'none',
                    'padding': '8px 15px',
                    'borderRadius': '4px'
                })
            ], style={'display': 'flex'})
        ], style={
            'background': 'white', 
            'padding': '20px', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'width': '600px'
        })
    ], id='ai-frame', style={
    'display': 'none',
    'position': 'fixed',
    'top': '50%',
    'right': '5%',  # 5% depuis le bord droit
    'transform': 'translateY(-50%)',
    'zIndex': '1000'
})
    
], id='main-container', style={'fontFamily': 'Arial, sans-serif', 'display': 'flex', 'flexDirection': 'column', 'minHeight': '100vh'})

# Ajouter du CSS personnalisé pour les animations
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Animation de traduction */
            .translation-animation {
                position: relative;
                width: 120px;
                height: 120px;
                margin: 0 auto 20px;
            }
            
            .translation-globe {
                position: absolute;
                top: 10px;
                left: 10px;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: linear-gradient(45deg, #c42e2e, #3a7ab9);
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
                animation: pulse 2s infinite alternate;
            }
            
            .translation-globe:before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background: linear-gradient(transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
            }
            
            .translation-particles {
                position: absolute;
                background-color: #fff;
                border-radius: 50%;
                opacity: 0.8;
                animation: orbit 4s infinite linear;
            }
            
            .particle1 {
                width: 18px;
                height: 18px;
                top: 10px;
                left: 50px;
                animation-delay: 0s;
                background-color: #f7a93b;
            }
            
            .particle2 {
                width: 12px;
                height: 12px;
                top: 60px;
                left: 10px;
                animation-delay: 0.5s;
                background-color: #3a7ab9;
            }
            
            .particle3 {
                width: 15px;
                height: 15px;
                top: 90px;
                left: 50px;
                animation-delay: 1s;
                background-color: #48b95e;
            }
            
            .particle4 {
                width: 10px;
                height: 10px;
                top: 60px;
                left: 90px;
                animation-delay: 1.5s;
                background-color: #e74c3c;
            }
            
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 15px rgba(255, 255, 255, 0.5); }
                100% { transform: scale(1.05); box-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }
            }
            
            @keyframes orbit {
                0% { transform: rotate(0deg) translateX(45px) rotate(0deg); }
                100% { transform: rotate(360deg) translateX(45px) rotate(-360deg); }
            }
            
            /* Styles pour l'animation de goutte de sang */
            .blood-container {
                position: relative;
                width: 120px;
                height: 160px;
                margin: 0 auto;
            }
            
            .blood-drop {
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 60px;
                background-color: #c42e2e;
                border-radius: 50%;
                animation: drop 1.5s ease-in infinite, pulse 1.5s ease-in-out infinite alternate;
                box-shadow: 0 0 10px rgba(196, 46, 46, 0.5);
            }
            
            .blood-drop:before {
                content: '';
                position: absolute;
                top: 50%;
                left: 0;
                width: 100%;
                height: 60px;
                background-color: #c42e2e;
                border-radius: 50%;
                animation: drip 1.5s ease-in infinite;
            }
            
            .blood-splash {
                position: absolute;
                bottom: 15px;
                width: 15px;
                height: 15px;
                background-color: #c42e2e;
                border-radius: 50%;
                opacity: 0;
                animation: splash 1.5s ease-out infinite;
            }
            
            .splash1 { left: 10%; animation-delay: 1.3s; }
            .splash2 { left: 30%; animation-delay: 1.5s; }
            .splash3 { left: 50%; transform: translateX(-50%); animation-delay: 1.4s; }
            .splash4 { right: 30%; animation-delay: 1.6s; }
            .splash5 { right: 10%; animation-delay: 1.5s; }
            
            @keyframes drop {
                0% { transform: translateX(-50%) translateY(-40px) scale(0.8); }
                80% { transform: translateX(-50%) translateY(100px) scale(1); }
                100% { transform: translateX(-50%) translateY(100px) scale(1); }
            }
            
            @keyframes drip {
                0% { height: 0; top: 30px; border-radius: 50% 50% 50% 50%; }
                30% { height: 40px; top: 30px; border-radius: 50% 50% 40% 40%; }
                60% { height: 60px; top: 0; border-radius: 40% 40% 30% 30%; }
                100% { height: 0; top: 0; border-radius: 50% 50% 50% 50%; }
            }
            
            @keyframes splash {
                0% { transform: scale(0); opacity: 0; }
                10% { transform: scale(0.3); opacity: 0.8; }
                50% { transform: scale(1.2); opacity: 0.5; }
                100% { transform: scale(1.5); opacity: 0; }
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 5px rgba(196, 46, 46, 0.5); }
                100% { box-shadow: 0 0 20px rgba(196, 46, 46, 0.8); }
            }
            
            /* Styles pour le texte inspirant qui pulse */
            #loading-inspirational-text {
                animation: textPulse 2s ease-in-out infinite alternate;
            }
            
            @keyframes textPulse {
                0% { opacity: 0.6; transform: scale(0.98); }
                100% { opacity: 1; transform: scale(1.02); }
            }
            
            /* Styles pour la transition de l'écran de chargement */
            #loading-overlay {
                transition: opacity 0.5s ease;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback pour ouvrir le modal de confirmation du changement de langue
@app.callback(
    [
        Output('language-confirm-modal', 'is_open'),
        Output('language-confirm-title', 'children'),
        Output('language-confirm-body', 'children'),
        Output('language-confirm-yes', 'children'),
        Output('language-confirm-no', 'children')
    ],
    [Input('language-toggle', 'n_clicks')],
    [State('language-store', 'data')],
    prevent_initial_call=True
)
def open_language_confirm_modal(n_clicks, current_lang):
    """Ouvre le modal de confirmation du changement de langue."""
    if n_clicks:
        translations = TRANSLATIONS[current_lang]
        target_lang = 'en' if current_lang == 'fr' else 'fr'
        confirm_title = translations.get("Confirmer le changement de langue", "Confirmer le changement de langue")
        
        if current_lang == 'fr':
            confirm_body = translations.get("Êtes-vous sûr de vouloir passer en anglais?", "Êtes-vous sûr de vouloir passer en anglais?")
        else:
            confirm_body = translations.get("Êtes-vous sûr de vouloir passer en français?", "Êtes-vous sûr de vouloir passer en français?")
        
        yes_text = translations.get("Oui", "Oui")
        no_text = translations.get("Non", "Non")
        
        return True, confirm_title, confirm_body, yes_text, no_text
    
    return False, "", "", "", ""

# Callback pour fermer le modal de confirmation si l'utilisateur clique sur "Non"
@app.callback(
    Output('language-confirm-modal', 'is_open', allow_duplicate=True),
    [Input('language-confirm-no', 'n_clicks')],
    prevent_initial_call=True
)
def close_language_confirm_modal(n_clicks):
    """Ferme le modal de confirmation du changement de langue."""
    if n_clicks:
        return False
    return dash.no_update

# Callback pour initialiser le processus de traduction
@app.callback(
    [
        Output('language-loading-modal', 'is_open'),
        Output('language-loading-text', 'children'),
        Output('translation-status', 'data'),
        Output('language-store', 'data'),
        Output('language-confirm-modal', 'is_open', allow_duplicate=True),
        Output('language-change-interval', 'disabled'),
        Output('translation-progress', 'data')
    ],
    [Input('language-confirm-yes', 'n_clicks')],
    [State('language-store', 'data'),
     State('translation-status', 'data')],
    prevent_initial_call=True
)
def start_language_translation_process(n_clicks, current_lang, status):
    """Initialise le processus de traduction et affiche le modal de chargement."""
    if n_clicks:
        translations = TRANSLATIONS[current_lang]
        loading_text = translations.get("Changement de langue en cours...", "Changement de langue en cours...")
        
        new_lang = 'en' if current_lang == 'fr' else 'fr'
        
        # Messages variés pour l'animation de chargement
        if new_lang == 'fr':
            progress_messages = [
                "Traduction de l'interface...",
                "Mise à jour des graphiques...",
                "Adaptation des menus...",
                "Chargement des titres...",
                "Traduction des légendes...",
                "Préparation des données...",
                "Finalisation des textes...",
                "Actualisation des paramètres...",
                "Optimisation de l'affichage...",
                "Derniers ajustements..."
            ]
        else:
            progress_messages = [
                "Translating interface...",
                "Updating charts...",
                "Adapting menus...",
                "Loading titles...",
                "Translating legends...",
                "Preparing data...",
                "Finalizing texts...",
                "Updating parameters...",
                "Optimizing display...",
                "Final adjustments..."
            ]
        
        # Initialiser l'état de la traduction
        status = {'initiated': True, 'completed': False}
        
        # Initialiser les données de progression
        progress_data = {
            'current': 0,
            'total': 10,
            'messages': progress_messages
        }
        
        # Activer l'intervalle pour l'animation de progression
        return True, loading_text, status, new_lang, False, False, progress_data
    
    return False, "", status, dash.no_update, dash.no_update, True, {'current': 0, 'total': 10, 'messages': []}

# Callback pour mettre à jour l'animation de progression pendant la traduction
@app.callback(
    [
        Output('translation-progress-bar', 'value'),
        Output('translation-status-message', 'children'),
        Output('translation-progress', 'data', allow_duplicate=True)
    ],
    [Input('language-change-interval', 'n_intervals')],
    [State('translation-progress', 'data')],
    prevent_initial_call=True
)
def update_translation_progress(n_intervals, progress_data):
    """Met à jour la barre de progression et les messages pendant la traduction."""
    if n_intervals is None or progress_data is None:
        return 0, "", dash.no_update
    
    current = progress_data['current']
    total = progress_data['total']
    messages = progress_data['messages']
    
    # Calculer la progression actuelle
    if current < total:
        current += 1
        progress_percentage = (current / total) * 100
        
        # Sélectionner le message correspondant à l'étape actuelle
        current_message = messages[min(current - 1, len(messages) - 1)]
        
        # Mettre à jour les données de progression
        updated_progress = {
            'current': current,
            'total': total,
            'messages': messages
        }
        
        return progress_percentage, current_message, updated_progress
    
    return 100, "Traduction terminée!", progress_data

# Callback pour fermer le modal une fois la traduction terminée
@app.callback(
    [
        Output('language-loading-modal', 'is_open', allow_duplicate=True),
        Output('language-change-interval', 'disabled', allow_duplicate=True),
        Output('translation-status', 'data', allow_duplicate=True)
    ],
    [Input('translation-progress', 'data')],
    [State('translation-status', 'data')],
    prevent_initial_call=True
)
def complete_translation_process(progress_data, status):
    """Ferme le modal de chargement une fois que la traduction est terminée."""
    if progress_data and progress_data['current'] >= progress_data['total'] and status['initiated']:
        # Marquer la traduction comme terminée
        status['completed'] = True
        return False, True, status
    
    return dash.no_update, dash.no_update, dash.no_update

# Callback pour créer l'écran de chargement basé sur le thème actuel
@app.callback(
    Output('loading-container', 'children'),
    [Input('theme-store', 'data'),
     Input('language-store', 'data')],
)
def update_loading_screen(theme, language):
    """Met à jour l'écran de chargement en fonction du thème et de la langue."""
    return create_loading_screen(theme, language)

# Callback pour suivre les changements d'URL et déclencher l'animation de chargement
@app.callback(
    [Output('loading-state', 'data'),
     Output('previous-url', 'data'),
     Output('loading-interval', 'disabled')],
    [Input('url', 'pathname')],
    [State('previous-url', 'data'),
     State('loading-state', 'data')],
    prevent_initial_call=True
)
def track_url_changes(pathname, previous_pathname, loading_state):
    """
    Surveille les changements d'URL et déclenche l'état de chargement.
    """
    # Si c'est le premier chargement ou si l'URL n'a pas changé
    if previous_pathname is None or pathname == previous_pathname:
        return loading_state, pathname, True
    
    # Si l'URL a changé, déclencher le chargement
    updated_loading_state = {
        'is_loading': True,
        'from': previous_pathname,
        'to': pathname
    }
    
    # Activer l'intervalle pour gérer le temps de chargement minimal
    return updated_loading_state, pathname, False

# Callback pour afficher/masquer l'écran de chargement
@app.callback(
    Output('loading-overlay', 'style'),
    [Input('loading-state', 'data'),
     Input('loading-interval', 'n_intervals')],
    [State('loading-overlay', 'style')],
    prevent_initial_call=True
)
def toggle_loading_overlay(loading_state, n_intervals, current_style):
    """
    Affiche ou masque l'écran de chargement en fonction de l'état de chargement.
    """
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Style de base
    base_style = current_style.copy() if current_style else {}
    
    # Si le déclencheur est le changement d'état de chargement
    if trigger_id == 'loading-state' and loading_state.get('is_loading', False):
        # Afficher l'écran de chargement
        base_style['opacity'] = '1'
        base_style['pointerEvents'] = 'auto'
        return base_style
    
    # Si le déclencheur est l'intervalle (le délai minimum est écoulé)
    elif trigger_id == 'loading-interval' and n_intervals is not None and n_intervals > 0:
        # Masquer l'écran de chargement
        base_style['opacity'] = '0'
        base_style['pointerEvents'] = 'none'
        return base_style
    
    # Par défaut, ne pas changer
    return dash.no_update

# Callback pour mettre à jour l'indicateur de chargement et le réinitialiser
@app.callback(
    [Output('loading-interval', 'n_intervals', allow_duplicate=True),
     Output('loading-state', 'data', allow_duplicate=True)],
    [Input('loading-interval', 'n_intervals')],
    [State('loading-state', 'data')],
    prevent_initial_call=True
)
def reset_loading_after_interval(n_intervals, loading_state):
    """Réinitialise l'état de chargement après l'intervalle."""
    if n_intervals is not None and n_intervals > 0:
        updated_loading_state = loading_state.copy()
        updated_loading_state['is_loading'] = False
        return 0, updated_loading_state
    
    return dash.no_update, dash.no_update

# MODIFICATION 1: Mise à jour du callback de navigation pour masquer les boutons sur la page d'authentification
@app.callback(
    [Output('page-title', 'children'),
     Output('nav-buttons', 'children'),
     Output('header-spacer', 'style')],
    [Input('url', 'pathname'),
     Input('page-title', 'children'),
     Input('language-store', 'data')]
)
def update_navigation(pathname, current_title, language):
    """
    Met à jour le titre de la page et les boutons de navigation en fonction de l'URL.

    Args:
        pathname (str): Le chemin URL actuel.
        current_title (str): Le titre actuel de la page.
        language (str): La langue actuelle ('fr' ou 'en').

    Returns:
        tuple: Un tuple contenant:
            - Le titre de la page (str)
            - Les boutons de navigation (list)
            - Le style de l'espacement d'en-tête (dict)
    """
    # Si pathname est None (au chargement initial), utilisez "/"
    if pathname is None or pathname == "":
        pathname = "/"
        
    # Obtenir le titre de la page
    # Si le pathname est "/about-us" ou "/administration", qui ne sont plus dans PAGES
    if pathname == "/about-us":
        page_title = "À propos de nous" if language == "fr" else "About Us"
    elif pathname == "/administration":
        page_title = "Administration"
    else:
        # Sinon, utiliser le dictionnaire PAGES
        page_title = PAGES[language].get(pathname, PAGES[language]["/"]).get("name")
    
    translated_title = TRANSLATIONS[language].get(page_title, page_title)
    
    # Si on est sur la page d'authentification, ne pas afficher les boutons de navigation
    if pathname == "/":
        nav_buttons = []
    else:
        # Créer les boutons de navigation avec le bouton actif mis en évidence
        nav_buttons = create_nav_buttons(pathname, language)
    
    # Plus le titre est long, plus il risque de prendre de place sur mobile
    title_length = len(page_title)
    spacer_height = '80px' if title_length < 25 else '100px'
    
    return translated_title, nav_buttons, {'height': spacer_height}

# MODIFICATION 2: Ajouter un nouveau callback pour masquer les boutons spéciaux
@app.callback(
    [Output('download-link', 'style'),
     Output('upload-excel', 'style'),
     Output('form-btn', 'style'),
     Output('open-ai-frame-btn', 'style')],
    [Input('url', 'pathname')]
)
def toggle_special_buttons(pathname):
    """
    Affiche ou masque les boutons spéciaux en fonction de l'URL.
    """
    # Si on est sur la page d'authentification, masquer les boutons
    if pathname == "/" or pathname is None or pathname == "":
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    
    # Sinon, afficher les boutons avec leur style par défaut
    download_style = {
        'position': 'fixed',
        'bottom': '200px',
        'right': '20px',
        'zIndex': '1000',
        'backgroundColor': '#6c757d',
        'borderRadius': '50%',
        'width': '50px',
        'height': '50px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'border': 'none',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'cursor': 'pointer'
    }
    
    upload_style = {
        'position': 'fixed',
        'bottom': '140px',
        'right': '20px',
        'zIndex': '1000',
        'backgroundColor': '#217346',
        'borderRadius': '50%',
        'width': '50px',
        'height': '50px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'border': 'none',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'cursor': 'pointer'
    }
    
    form_style = {
        'position': 'fixed',
        'bottom': '80px',
        'right': '20px',
        'zIndex': '1000',
        'backgroundColor': '#28a745',
        'borderRadius': '50%',
        'width': '50px',
        'height': '50px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'border': 'none',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'cursor': 'pointer'
    }
    
    chatbot_style = {
        'position': 'fixed',
        'bottom': '20px', 
        'right': '20px',
        'zIndex': '1000',
        'backgroundColor': '#007bff',
        'borderRadius': '50%',
        'width': '50px',
        'height': '50px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'border': 'none',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'cursor': 'pointer'
    }
    
    return download_style, upload_style, form_style, chatbot_style

# Callback pour mettre à jour l'apparence du bouton de thème
@app.callback(
    [Output('theme-text', 'children'),
     Output('theme-icon', 'icon')],
    [Input('theme-store', 'data'),
     Input('language-store', 'data')]
)
def update_theme_button(theme, language):
    """
    Met à jour l'apparence du bouton de thème en fonction du thème actuel et de la langue.

    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        language (str): La langue actuelle ('fr' ou 'en').

    Returns:
        tuple: Un tuple contenant:
            - Le texte à afficher sur le bouton (str)
            - L'icône à afficher sur le bouton (str)
    """
    if theme == 'light':
        return TRANSLATIONS[language]["Mode sombre"], "ph:moon"
    else:
        return TRANSLATIONS[language]["Mode clair"], "ph:sun"
# Callback pour basculer le thème - Mise à jour pour utiliser le thème bleu foncé par défaut
@app.callback(
    [Output('theme-store', 'data'),
     Output('main-container', 'style'),
     Output('header', 'style'),
     Output('page-content', 'style'),
     Output('footer', 'style')],
    [Input('theme-toggle', 'n_clicks')],
    [State('theme-store', 'data')]
)
def toggle_theme(n_clicks, current_theme):
    """
    Bascule entre les thèmes clair et sombre de l'application.

    Args:
        n_clicks (int): Le nombre de clics sur le bouton de basculement de thème.
        current_theme (str): Le thème actuel ('light' ou 'dark').

    Returns:
        tuple: Un tuple contenant:
            - Le nouveau thème (str)
            - Le style du conteneur principal (dict)
            - Le style de l'en-tête (dict)
            - Le style du contenu de la page (dict)
            - Le style du pied de page (dict)
    """
    if n_clicks is None:
        # Premier chargement, appliquer le thème sombre comme par défaut
        theme_props = dark_blue_theme
        new_theme = 'dark'
    else:
        # Basculer le thème
        if current_theme == 'light':
            theme_props = dark_blue_theme
            new_theme = 'dark'
        else:
            theme_props = light_theme
            new_theme = 'light'
    
    # Styles à appliquer
    main_style = {
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': theme_props['backgroundColor'],
        'color': theme_props['color'],
        'minHeight': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'transition': 'background-color 0.3s ease, color 0.3s ease'
    }
    
    header_style = {
        'background': theme_props['headerBg'],
        'color': theme_props['headerColor'],
        'padding': '15px',
        'position': 'fixed',
        'top': '0',
        'width': '100%',
        'zIndex': '1000',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
        'transition': 'background 0.3s ease'
    }
    
    content_style = {
        'backgroundColor': theme_props['backgroundColor'],
        'color': theme_props['color'],
        'paddingTop': '20px',
        'paddingBottom': '40px',
        'flex': '1',
        'transition': 'background-color 0.3s ease, color 0.3s ease'
    }
    
    footer_style = {
        'backgroundColor': theme_props['footerBg'],
        'color': theme_props['footerColor'],
        'width': '100%',
        'padding': '20px 0',
        'textAlign': 'center',
        'marginTop': 'auto',
        'transition': 'background-color 0.3s ease, color 0.3s ease'
    }
    
    return new_theme, main_style, header_style, content_style, footer_style


# Callback pour mettre à jour le contenu de la page
# Callback pour mettre à jour le contenu de la page
@app.callback(
    [Output('page-content', 'children'),
     Output('footer', 'children')],
    [Input('url', 'pathname'),
     Input('theme-store', 'data'),
     Input('language-store', 'data'),
     Input('auth-state', 'data')]  # L'état d'authentification est un input important
)
def display_page(pathname, theme, language="fr", auth_state=auth_st):
    """
    Affiche le contenu de la page en fonction de l'URL et du thème.

    Args:
        pathname (str): Le chemin URL actuel qui détermine quelle page afficher.
        theme (str): Le thème actuel ('light' ou 'dark') qui détermine les couleurs à utiliser.
        language (str): La langue actuelle ('fr' ou 'en').
        auth_state (dict): État d'authentification de l'utilisateur.

    Returns:
        tuple: Un tuple contenant:
            - Le contenu de la page (dash component)
            - Le contenu du pied de page (dash component)
    """
    
    # Vérifier si l'utilisateur est authentifié et est administrateur
    is_authenticated = auth_st['authenticated']
    is_admin = auth_st['is_admin']
    
    # Choisir les couleurs du thème pour les graphiques
    if theme == 'dark':
        # Utiliser des couleurs adaptées au thème bleu foncé
        plot_bg = 'rgba(15, 23, 42, 0.8)'  # Bleu foncé semi-transparent
        plot_paper_bg = '#0f172a'
        plot_font_color = 'white'
        plot_grid_color = '#334155'
        card_bg = dark_blue_theme['cardBg']
        card_shadow = dark_blue_theme['cardShadow']
        text_color = 'white'
    else:
        plot_bg = 'white'
        plot_paper_bg = 'white'
        plot_font_color = 'black'
        plot_grid_color = '#eee'
        card_bg = light_theme['cardBg']
        card_shadow = light_theme['cardShadow']
        text_color = 'black'
    
    # Créer le contenu du footer en fonction de la page
    if pathname == "/" or pathname is None or pathname == "":
        # Footer simplifié pour la page d'authentification (sans les boutons)
        footer_content = html.Div([
            html.Hr(style={'width': '80%', 'margin': 'auto', 'marginBottom': '20px', 'opacity': '0.2'}),
            # Contenu du footer sans les boutons
            html.Div([
                Icon(
                    icon="healthicons:blood-donation",
                    width=24,
                    height=24,
                    style={"marginRight": "10px", "verticalAlign": "middle"}
                ),
                html.Span(TRANSLATIONS[language]["Dashboard Don de Sang © 2025"], style={"verticalAlign": "middle"})
            ], className="mb-1"),
            html.P("NK-STAT-CONSULTING", className="mb-1")
        ])
    else:
        # Footer avec boutons pour les autres pages
        footer_content = html.Div([
            html.Hr(style={'width': '80%', 'margin': 'auto', 'marginBottom': '20px', 'opacity': '0.2'}),
            
            # Container pour les liens du footer
            html.Div([
                # Bouton À propos de nous
                dbc.Button([
                    Icon(
                        icon="carbon:group",
                        width=20,
                        height=20,
                        style={"marginRight": "8px"}
                    ),
                    "À propos de nous" if language == "fr" else "About Us"
                ], 
                href="/about-us", 
                color="link", 
                className="mx-2",
                style={
                    'color': '#c42e2e',
                    'textDecoration': 'none',
                    'border': 'none',
                    'background': 'none',
                    'fontWeight': 'bold'
                }),
                
                # Bouton Administration (visible pour tous mais vérifié à l'accès)
                dbc.Button([
                    Icon(
                        icon="carbon:user-admin",
                        width=20,
                        height=20,
                        style={"marginRight": "8px"}
                    ),
                    "Administration" if language == "fr" else "Administration"
                ], 
                href="/administration", 
                color="link", 
                className="mx-2",
                style={
                    'color': '#c42e2e',
                    'textDecoration': 'none',
                    'border': 'none',
                    'background': 'none',
                    'fontWeight': 'bold'
                })
            ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '15px'}),
            
            # Contenu existant du footer
            html.Div([
                Icon(
                    icon="healthicons:blood-donation",
                    width=24,
                    height=24,
                    style={"marginRight": "10px", "verticalAlign": "middle"}
                ),
                html.Span(TRANSLATIONS[language]["Dashboard Don de Sang © 2025"], style={"verticalAlign": "middle"})
            ], className="mb-1"),
            html.P("NK-STAT-CONSULTING", className="mb-1")
        ])
    
    # Sélection des pages
    if pathname == "/" or pathname is None or pathname == "":
        return page_authentification(theme, language=language), footer_content
    
    elif pathname == "/repartition-geographique":
        return page_une(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme, language=language), footer_content
    
    elif pathname == "/analyse-elegibilite":
        return page_deux(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme,language=language), footer_content
    
    elif pathname == "/evolution-temporelle":
        return page_trois(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme, language=language), footer_content
    
    elif pathname == "/analyse-predictive":
        return page_quatre(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme, language=language), footer_content
    
    elif pathname == "/about-us":
        return page_about_us(theme, language), footer_content
    
    # Page d'administration - Vérifier les droits d'accès
    elif pathname == "/administration":
        # Si l'utilisateur est administrateur, afficher la page d'administration
        if is_admin:
            return page_administration(theme, language=language), footer_content
        # Sinon, afficher la page d'accès refusé
        else:
            return access_denied_page(theme, language), footer_content
    
    # Si l'URL n'est pas reconnue, rediriger vers la page d'authentification
    return page_authentification(theme, language=language), footer_content


# Fonction pour créer un style de carte adapté au thème actuel
def create_card_style(theme):
    """
    Crée un style de carte qui s'adapte au thème actuel.
    
    Cette fonction génère un dictionnaire de style pour les cartes de l'interface utilisateur,
    en fonction du thème actuel (clair ou sombre).
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        
    Returns:
        dict: Un dictionnaire contenant les propriétés de style CSS pour les cartes.
    """
    if theme == 'dark':
        return {
            'backgroundColor': dark_blue_theme['cardBg'],
            'color': dark_blue_theme['color'],
            'boxShadow': dark_blue_theme['cardShadow'],
            'borderRadius': '8px',
            'padding': '15px',
            'marginBottom': '20px',
            'border': dark_blue_theme['cardBorder']
        }
    else:
        return {
            'backgroundColor': light_theme['cardBg'],
            'color': light_theme['color'],
            'boxShadow': light_theme['cardShadow'],
            'borderRadius': '5px',
            'padding': '15px',
            'marginBottom': '20px'
        }



# Callback pour afficher/masquer le cadre d'IA
@app.callback(
    Output('ai-frame', 'style'),
    [Input('open-ai-frame-btn', 'n_clicks')]
)
def toggle_ai_frame(n_clicks):
    """
    Toggle the visibility of the AI frame based on the number of button clicks.

    Args:
        n_clicks (int): The number of times the button to open the AI frame has been clicked.

    Returns:
        dict: A dictionary containing the CSS style properties to either display or hide the AI frame.
              If the number of clicks is odd, the AI frame is displayed, otherwise, it is hidden.
    """

    if n_clicks % 2 == 1:
        return {
            'display': 'block', 
            'position': 'fixed', 
            'top': '50%', 
            'left': '50%', 
            'transform': 'translate(-50%, -50%)', 
            'zIndex': '1000'
        }
    return {'display': 'none'}


CONTEXT = """
Tu es un assistant spécialisé dans l'analyse des dons de sang. 
Tu peux aider à comprendre :
- Les statistiques de dons
- L'éligibilité au don
- L'importance du don de sang
- Les informations médicales liées aux dons
tu peux dans tes reponses utiliser le pdf:
 -assets/rapport.pdf pour extraire des informations 
ne  mentionne pas a l utilisateur que tu utilises ce pdf
"""

# Callback pour générer la réponse de l'IA
@app.callback(
    [Output('conversation-container', 'children'),
     Output('user-input', 'value')],
    [Input('send-btn', 'n_clicks')],
    [State('user-input', 'value'),
     State('conversation-container', 'children')]
)
def generate_ai_response(n_clicks, user_input, current_conversation):
    """
    Génère une réponse de l'IA en fonction de l'input de l'utilisateur.

    Cette fonction est un callback Dash qui prend en entrée le nombre de clics sur le bouton
    d'envoi de message, l'input de l'utilisateur et l'historique de conversation actuel.
    Elle renvoie la nouvelle conversation mise à jour et un champ d'input vide.
    
    Si l'utilisateur n'a pas envoyé de message ou si l'IA n'a pas pu générer de réponse,
    la fonction renvoie l'historique de conversation actuel et un champ d'input vide.
    
    Si l'IA a pu générer une réponse, la fonction ajoute le message de l'utilisateur et
    la réponse de l'IA à l'historique de conversation et renvoie la nouvelle conversation.
    """
    
    if not n_clicks or not user_input:
        return current_conversation or [], ''
    
    if not current_conversation:
        current_conversation = []
    
    # Message de l'utilisateur
    user_message = html.Div([
        html.Strong('Vous : ', style={'color': '#495057'}), 
        html.Span(user_input, style={'color': '#212529'})
    ], style={
        'marginBottom': '10px', 
        'textAlign': 'right',
        'padding': '8px',
        'backgroundColor': '#e9ecef',
        'borderRadius': '5px'
    })
    
    user_input = f"{CONTEXT}\n\nQuestion de l'utilisateur : {user_input}"
    # Génération de la réponse de l'IA
    try:
        response = model.generate_content(user_input)
        
        # Convertir le markdown en un paragraphe unique
        formatted_children = safe_markdown_to_children(response.text)
        
        ai_message = html.Div([
            # Suite du fichier main_dashboard.py

            html.Strong('IA : ', style={'color': '#007bff'}), 
            html.Div(
                formatted_children,
                style={'backgroundColor': '#f1f3f5', 'padding': '10px', 'borderRadius': '5px'}
            )
        ], style={'marginBottom': '10px', 'textAlign': 'left'})
        
        # Mettre à jour l'historique de conversation
        updated_conversation = current_conversation + [user_message, ai_message]
        
        return updated_conversation, ''
    
    except Exception as e:
        error_message = html.Div([
            html.Strong('Erreur : ', style={'color': 'red'}), 
            html.Span(str(e), style={'color': '#721c24'})
        ], style={
            'backgroundColor': '#f8d7da', 
            'padding': '10px', 
            'borderRadius': '5px',
            'marginBottom': '10px'
        })
        
        return current_conversation + [user_message, error_message], ''




# Définir le dossier de destination pour les uploads
UPLOAD_DIRECTORY = "./dataset"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# Callback pour gérer l'upload et le modal
@app.callback(
    [Output('custom-modal', 'style'),
     Output('modal-content', 'children')],
    [Input('upload-excel', 'contents'),
     Input('modal-close-btn', 'n_clicks')],
    [State('upload-excel', 'filename'),
     State('language-store', 'data')],
    prevent_initial_call=True
)
def handle_file_upload(contents, close_clicks, filename, language):
    """
    Gère l'upload de fichier Excel et affiche un modal de confirmation ou d'erreur.
    
    Args:
        contents (str): Le contenu du fichier uploadé.
        close_clicks (int): Le nombre de clics sur le bouton de fermeture du modal.
        filename (str): Le nom du fichier uploadé.
        language (str): La langue actuelle ('fr' ou 'en').
    
    Returns:
        tuple: Un tuple contenant le style CSS du modal et son contenu.
    """
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Récupérer les traductions
    translations = TRANSLATIONS[language]
    
    # Style de base pour masquer/afficher le modal
    base_style = {
        'position': 'fixed',
        'top': '50%',
        'left': '50%',
        'transform': 'translate(-50%, -50%)',
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'zIndex': '1100',
        'textAlign': 'center',
        'width': '300px'
    }
    
    # Logique d'upload de fichier
    if trigger_id == 'upload-excel' and contents is not None:
        try:
            # Décoder et sauvegarder le fichier
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            # Nom de fichier fixe
            fixed_filename = "Challenge dataset.xlsx"
            file_path = os.path.join(UPLOAD_DIRECTORY, fixed_filename)
            
            # Supprimer le fichier existant s'il existe
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Sauvegarder le fichier avec le nouveau nom
            with open(file_path, 'wb') as file:
                file.write(decoded)
            
            # Afficher le modal de succès
            success_style = base_style.copy()
            success_style['display'] = 'block'
            send_upload_notification_email(fixed_filename, language,maill=auth_st['email'])
            modifier_ligne('main_dashboard.py', 24, 'print("py")')
            
            return success_style, html.Div([
                html.H4(translations["Fichier Uploader avec Succes"], style={'color': 'green'}),
                html.P(f"{translations['Le fichier a été uploadé sous le nom']} {fixed_filename}")
            ])
        
        except Exception as e:
            # Afficher le modal d'erreur
            error_style = base_style.copy()
            error_style['display'] = 'block'
            
            return error_style, html.Div([
                html.H4(translations["Erreur d'Upload"], style={'color': 'red'}),
                html.P(f"{translations['Une erreur est survenue']} : {str(e)}")
            ])
    
    # Fermer le modal
    if trigger_id == 'modal-close-btn':
        close_style = base_style.copy()
        close_style['display'] = 'none'
        return close_style, []
    
    # Style par défaut (masqué)
    default_style = base_style.copy()
    default_style['display'] = 'none'
    return default_style, []    

@app.callback(
    [Output('download-link', 'href'),
     Output('download-link', 'download')],
    [Input('language-store', 'data')]
)
def update_download_link(language):
    """
    Met à jour le lien de téléchargement en fonction de la langue sélectionnée.
    
    Args:
        language (str): La langue actuelle ('fr' ou 'en').
        
    Returns:
        tuple: Un tuple contenant le nouveau href et le nom de fichier pour le téléchargement.
    """
    if language == 'en':
        return '/assets/report_en.pdf', 'report_en.pdf'
    else:
        return '/assets/rapport.pdf', 'rapport.pdf'



# Callback pour vérifier les identifiants et gérer l'authentification
@app.callback(
    [
        Output('redirect-id', 'pathname'),
        Output('auth-error-message', 'children'),
        Output('auth-error-message', 'style'),
        Output('auth-state', 'data')
    ],
    [Input('login-button', 'n_clicks')],
    [
        State('email-input', 'value'),
        State('password-input', 'value'),
        State('error-message-store', 'data'),
        State('auth-error-message', 'style')
    ],
    prevent_initial_call=True
)
def validate_login(n_clicks, email, password, error_message, current_error_style):
    """
    Valide les identifiants de connexion en vérifiant dans la base de données SQLite.
    Redirige vers la page principale si les identifiants sont valides, 
    ou affiche un message d'erreur si les identifiants sont invalides.
    """
    
    global auth_st 
    # Style de base pour les messages d'erreur (toujours visible quand nécessaire)
    base_error_style = {
        'color': '#ffffff',
        'backgroundColor': 'rgba(220, 53, 69, 0.8)',
        'padding': '15px',
        'borderRadius': '6px',
        'marginBottom': '20px',
        'textAlign': 'center',
        'fontWeight': '500',
        'border': '1px solid #dc3545',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.2)'
    }
    
    # Vérifier si le callback a été déclenché par un clic
    if n_clicks is None:
        # Ne rien changer au début
        hidden_style = current_error_style.copy() if current_error_style else base_error_style.copy()
        hidden_style['display'] = 'none'
        return None, "", hidden_style, {'authenticated': False}
    
    # Vérifier si les champs ne sont pas vides
    if not email or not password:
        error_style = base_error_style.copy()
        error_style['display'] = 'block'  # S'assurer que c'est visible
        
        return None, "Veuillez remplir tous les champs", error_style, {'authenticated': False}
    
    # Vérifier les identifiants dans la base de données
    if verify_credentials(email, password):
        # Authentification réussie
        # Récupérer toutes les informations de l'utilisateur
        user_info_dict = get_connected_user_info(email)
        
        # Cacher le message d'erreur en cas de succès
        hidden_style = base_error_style.copy()
        hidden_style['display'] = 'none'
        
        if user_info_dict:
            # Créer un état d'authentification complet
            auth_state = {
                'authenticated': True,
                'email': email,
                'is_admin': user_info_dict.get('is_admin', False),
                'user_id': user_info_dict.get('id'),
                'last_login': user_info_dict.get('last_login'),
            }
            auth_st = auth_state
            
            return "/repartition-geographique", "", hidden_style, auth_state
        else:
            # Cas improbable: utilisateur authentifié mais infos non trouvées
            basic_auth_state = {
                'authenticated': True,
                'email': email,
                'is_admin': False  # Valeur par défaut
            }
            auth_st = basic_auth_state
            return "/repartition-geographique", "", hidden_style, basic_auth_state
    else:
        # Authentification échouée - s'assurer que le message d'erreur est affiché
        error_style = base_error_style.copy()
        error_style['display'] = 'block'  # S'assurer que c'est visible
        
        # Message d'erreur amélioré
        error_message_content = html.Div([
            html.Strong("Identifiants incorrects", style={'fontSize': '16px', 'color': '#ffd7d7'}),
            html.Br(),
            html.Span("Votre email ou mot de passe est incorrect.", style={'fontSize': '14px'}),
            html.Br(),
            html.Span("Pour récupérer vos accès, veuillez contacter l'administrateur : "),
            html.Br(),
            html.A(get_admin_email(), 
                   href=f"mailto:{get_admin_email()}", 
                   style={'color': '#ffbdbd', 'textDecoration': 'underline', 'fontWeight': 'bold'})
        ])
        
        return None, error_message_content, error_style, {'authenticated': False, 'email': email, 'is_admin': False}



# Callback pour charger la liste des utilisateurs
@app.callback(
    [Output('users-data', 'data'),
     Output('user-list-container', 'children')],
    [Input('url', 'pathname'),
     Input('add-user-button', 'n_clicks')],
    [State('language-store', 'data'),
     State('theme-store', 'data')]
)
def load_users(pathname, n_clicks, language, theme):
    """
    Charge la liste des utilisateurs et l'affiche dans un tableau.
    """
    # Récupérer les traductions
    labels = {
        'fr': {
            'user_id': 'ID',
            'user_email': 'Email',
            'user_role': 'Rôle',
            'admin': 'Admin',
            'user': 'Utilisateur',
            'actions': 'Actions',
            'delete': 'Supprimer'
        },
        'en': {
            'user_id': 'ID',
            'user_email': 'Email',
            'user_role': 'Role',
            'admin': 'Admin',
            'user': 'User',
            'actions': 'Actions',
            'delete': 'Delete'
        }
    }
    text = labels[language]
    
    # Définir les styles en fonction du thème
    if theme == 'dark':
        text_color = 'dark'
        bg_color = '#0A3160'  # Bleu sombre pour le fond de la carte
        table_bg_color = '#0A3160'  # Bleu encore plus sombre pour le tableau
        border_color = 'rgba(255, 255, 255, 0.1)'
    else:
        text_color = 'black'
        bg_color = 'white'
        table_bg_color = 'white'
        border_color = 'rgba(0, 0, 0, 0.1)'
    
    # Si on n'est pas sur la page d'administration, ne rien faire
    if pathname != "/administration":
        return [], []
    
    # Récupérer la liste des utilisateurs
    users = get_all_users()
    
    # Créer le tableau des utilisateurs
    table_header = [
        html.Thead(html.Tr([
            html.Th(text['user_id'], style={'color': text_color}),
            html.Th(text['user_email'], style={'color': text_color}),
            html.Th(text['user_role'], style={'color': text_color}),
            html.Th(text['actions'], style={'color': text_color})
        ]))
    ]
    
    table_rows = []
    for user in users:
        role = text['admin'] if user['is_admin'] else text['user']
        row = html.Tr([
            html.Td(user['id'], style={'color': text_color}),
            html.Td(user['email'], style={'color': text_color}),
            html.Td(role, style={'color': text_color}),
            html.Td(
                dbc.Button(
                    text['delete'],
                    id={'type': 'delete-user-button', 'index': user['id']},
                    color="danger",
                    size="sm",
                    className="mr-1",
                    style={'fontSize': '0.8rem'}
                ),
                style={'color': text_color}
            )
        ])
        table_rows.append(row)
    
    table_body = [html.Tbody(table_rows)]
    
    table = dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        style={
            'backgroundColor': table_bg_color,  # Utiliser la couleur du tableau spécifique
            'color': text_color,
            'border': f'1px solid {border_color}'
        }
    )
    
    return users, table

# Callback pour ajouter un nouvel utilisateur
@app.callback(
    [Output('admin-message', 'children'),
     Output('admin-message', 'style'),
     Output('new-user-email', 'value'),
     Output('new-user-password', 'value'),
     Output('new-user-confirm-password', 'value'),
     Output('new-user-is-admin', 'value'),
     Output('add-user-button', 'n_clicks')],
    [Input('add-user-button', 'n_clicks')],
    [State('new-user-email', 'value'),
     State('new-user-password', 'value'),
     State('new-user-confirm-password', 'value'),
     State('new-user-is-admin', 'value'),
     State('language-store', 'data'),
     State('theme-store', 'data')]
)
def add_new_user(n_clicks, email, password, confirm_password, is_admin, language, theme):
    """
    Ajoute un nouvel utilisateur à la base de données.
    """
    # Initialisation des styles
    if theme == 'dark':
        success_bg = 'rgba(25, 135, 84, 0.2)'
        success_color = '#4ade80'
        error_bg = 'rgba(220, 53, 69, 0.2)'
        error_color = '#ff6b6b'
    else:
        success_bg = 'rgba(25, 135, 84, 0.1)'
        success_color = '#198754'
        error_bg = 'rgba(220, 53, 69, 0.1)'
        error_color = '#dc3545'
    
    # Traductions
    labels = {
        'fr': {
            'success_message': 'Utilisateur ajouté avec succès',
            'error_message': 'Une erreur est survenue',
            'passwords_not_match': 'Les mots de passe ne correspondent pas',
            'email_exists': 'Cet email existe déjà',
            'missing_fields': 'Tous les champs sont obligatoires'
        },
        'en': {
            'success_message': 'User added successfully',
            'error_message': 'An error occurred',
            'passwords_not_match': 'Passwords do not match',
            'email_exists': 'This email already exists',
            'missing_fields': 'All fields are required'
        }
    }
    text = labels[language]
    
    # Si le callback n'est pas déclenché par un clic
    if n_clicks is None:
        return "", {'display': 'none'}, "", "", "", True, None
    
    # Vérifier que tous les champs sont remplis
    if not email or not password or not confirm_password:
        return text['missing_fields'], {
            'display': 'block',
            'backgroundColor': error_bg,
            'color': error_color,
            'padding': '10px',
            'borderRadius': '5px'
        }, email, password, confirm_password, is_admin, n_clicks
    
    # Vérifier que les mots de passe correspondent
    if password != confirm_password:
        return text['passwords_not_match'], {
            'display': 'block',
            'backgroundColor': error_bg,
            'color': error_color,
            'padding': '10px',
            'borderRadius': '5px'
        }, email, password, confirm_password, is_admin, n_clicks
    
    # Ajouter l'utilisateur
    result = add_user(email, password, is_admin)
    
    if result:
        # Succès
        return text['success_message'], {
            'display': 'block',
            'backgroundColor': success_bg,
            'color': success_color,
            'padding': '10px',
            'borderRadius': '5px'
        }, "", "", "", True, n_clicks
    else:
        # Échec
        return text['email_exists'], {
            'display': 'block',
            'backgroundColor': error_bg,
            'color': error_color,
            'padding': '10px',
            'borderRadius': '5px'
        }, email, password, confirm_password, is_admin, n_clicks

# Callback pour supprimer un utilisateur
@app.callback(
    Output('users-data', 'data', allow_duplicate=True),
    [Input({'type': 'delete-user-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'delete-user-button', 'index': ALL}, 'id')],
    prevent_initial_call=True
)
def delete_user_callback(n_clicks_list, button_ids):
    """
    Supprime un utilisateur de la base de données.
    """
    ctx = callback_context
    
    # Si aucun bouton n'a été cliqué
    if not ctx.triggered:
        return dash.no_update
    
    # Récupérer l'ID du bouton qui a été cliqué
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    user_id = json.loads(button_id)['index']
    
    # Supprimer l'utilisateur
    success = delete_user(user_id)
    
    # Récupérer la liste mise à jour des utilisateurs
    updated_users = get_all_users()
    
    return updated_users






# Lancer l'application
if __name__ == '__main__':
    
    app.run_server(debug=True)