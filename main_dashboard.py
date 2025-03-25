import dash
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify as Icon
from pages.pge_repartition_geo import *
from pages.pge_analyse_elgibillite import *
from pages.pge_evolution_temporelle import *
from pages.pge_analyse_predictives import *
from app import *
import os
import base64
import google.generativeai as genai
import markdown2
import re

#application Dash
# Configuration de l'API Gemini
GEMINI_API_KEY = 'AIzaSyBBedcqWYgt62f2zWrn-Tqm334HNXOd7vI'
genai.configure(api_key=GEMINI_API_KEY)


# Initialisation du modèle Gemini
model = genai.GenerativeModel('models/gemini-2.0-flash-thinking-exp-01-21')

def safe_markdown_to_children(text):
    """
    Convertit le markdown en un paragraphe unique Dash
    """
    # Convertir le markdown en HTML
    html_text = markdown2.markdown(text, extras=['fenced-code-blocks', 'tables'])
    
    # Supprimer les balises HTML tout en préservant la structure des paragraphes
    plain_text = re.sub(r'</?[^>]+>', ' ', html_text).strip()
    
    # Créer un paragraphe unique
    return html.P(
        plain_text, 
        style={
            'lineHeight': '1.6', 
            'color': '#333', 
            'fontSize': '16px'
        }
    )
    
    
    
# Conserver les routes de navigation originales
PAGES = {
    "/": {"name": "Répartition Géographique", "icon": "carbon:map"},
    "/repartition-geographique": {"name": "Répartition Géographique", "icon": "carbon:map"},
    "/analyse-elegibilite": {"name": "Analyse d'Éligibilité", "icon": "carbon:chart-evaluation"}, 
    "/evolution-temporelle": {"name": "Évolution Temporelle", "icon": "carbon:chart-line"}, 
    "/analyse-predictive": {"name": "Analyse predictive", "icon": "carbon:forecast-lightning"}
}


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
def create_nav_buttons(current_path):
    """
    Crée les boutons de navigation avec un style dégradé et des icônes.
    
    Cette fonction génère des boutons de navigation pour chaque page de l'application,
    en mettant en évidence le bouton correspondant à la page active.
    
    Args:
        current_path (str): Le chemin URL actuel qui détermine quel bouton doit être mis en évidence.
        
    Returns:
        list: Une liste de boutons dbc.Button stylisés pour la barre de navigation.
    """
    buttons = []
    for path, info in list(PAGES.items())[1:]:  # Commence à 1 pour sauter l'élément "/"
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
        
        # Création du bouton avec icône
        button = dbc.Button(
            [
                Icon(
                    icon=info["icon"],
                    width=16,
                    height=16,
                    style={"marginRight": "5px"}
                ),
                info["name"]
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

## Layout - Conserver le header et les marges originales
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    dcc.Store(id='theme-store', data='dark'),
    
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
                            style={'marginLeft': '10px', 'background': 'transparent', 'color': 'white', 'border': '1px solid rgba(255,255,255,0.5)', 'borderRadius': '4px'}
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
                                }
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
                        target='_blank'  # Ouvre dans un nouvel onglet
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
                        }
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
            html.H2('Assistant IA ', style={'color': '#333', 'borderBottom': '2px solid #007bff', 'paddingBottom': '10px'}),
            
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

# Conserver les callbacks originaux
@app.callback(
    [Output('page-title', 'children'),
     Output('nav-buttons', 'children'),
     Output('header-spacer', 'style')],
    [Input('url', 'pathname'),
     Input('page-title', 'children')]
)
def update_navigation(pathname, current_title):
    """
    Met à jour le titre de la page et les boutons de navigation en fonction de l'URL.
    
    Cette fonction callback est déclenchée lorsque l'URL change ou que le titre de la page est modifié.
    Elle met à jour le titre affiché et génère les boutons de navigation appropriés.
    
    Args:
        pathname (str): Le chemin URL actuel.
        current_title (str): Le titre actuel de la page.
        
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
    page_title = PAGES.get(pathname, PAGES["/"]).get("name")
    # Créer les boutons de navigation avec le bouton actif mis en évidence
    nav_buttons = create_nav_buttons(pathname)
    
    
    # Plus le titre est long, plus il risque de prendre de place sur mobile
    title_length = len(page_title)
    spacer_height = '80px' if title_length < 25 else '100px'
    
    return page_title, nav_buttons, {'height': spacer_height}

# Contenu principal


# Callback pour mettre à jour l'apparence du bouton de thème
@app.callback(
    [Output('theme-text', 'children'),
     Output('theme-icon', 'icon')],
    [Input('theme-store', 'data')]
)
def update_theme_button(theme):
    """
    Met à jour l'apparence du bouton de thème en fonction du thème actuel.
    
    Cette fonction callback change le texte et l'icône du bouton de basculement de thème
    selon que le thème actuel est clair ou sombre.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        
    Returns:
        tuple: Un tuple contenant:
            - Le texte à afficher sur le bouton (str)
            - L'icône à afficher sur le bouton (str)
    """
    if theme == 'light':
        return "Mode sombre", "ph:moon"
    else:
        return "Mode clair", "ph:sun"

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
    
    Cette fonction callback est déclenchée lorsque l'utilisateur clique sur le bouton de basculement de thème.
    Elle met à jour les styles de tous les éléments principaux de l'interface utilisateur.
    
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
@app.callback(
    [Output('page-content', 'children'),
     Output('footer', 'children')],
    [Input('url', 'pathname'),
     Input('theme-store', 'data')]
)
def display_page(pathname, theme):
    """
    Affiche le contenu de la page en fonction de l'URL et du thème.
    
    Cette fonction callback est déclenchée lorsque l'URL change ou que le thème est modifié.
    Elle détermine quelle page afficher et configure les couleurs des graphiques en fonction du thème.
    
    Args:
        pathname (str): Le chemin URL actuel qui détermine quelle page afficher.
        theme (str): Le thème actuel ('light' ou 'dark') qui détermine les couleurs à utiliser.
        
    Returns:
        tuple: Un tuple contenant:
            - Le contenu de la page (dash component)
            - Le contenu du pied de page (dash component)
    """
    # Choisir les couleurs du thème pour les graphiques
    if theme == 'dark':
        # Utiliser des couleurs adaptées au thème bleu foncé
        plot_bg = 'rgba(15, 23, 42, 0.8)'  # Bleu foncé semi-transparent
        plot_paper_bg = '#0f172a'
        plot_font_color = 'white'
        plot_grid_color = '#334155'
        card_bg = dark_blue_theme['cardBg']
        card_shadow = dark_blue_theme['cardShadow']
    else:
        plot_bg = 'white'
        plot_paper_bg = 'white'
        plot_font_color = 'black'
        plot_grid_color = '#eee'
        card_bg = light_theme['cardBg']
        card_shadow = light_theme['cardShadow']
    
    # Créer le contenu du footer
    footer_content = html.Div([
        html.Hr(style={'width': '80%', 'margin': 'auto', 'marginBottom': '20px', 'opacity': '0.2'}),
        html.Div([
            Icon(
                icon="healthicons:blood-donation",
                width=24,
                height=24,
                style={"marginRight": "10px", "verticalAlign": "middle"}
            ),
            html.Span("Dashboard Don de Sang © 2025", style={"verticalAlign": "middle"})
        ], className="mb-1"),
        html.P("NK-STAT-CONSULTING", className="mb-1")
    ])
    
    # Sélection des pages - utiliser les fonctions de page existantes avec le thème approprié
    if pathname == "/" or pathname is None or pathname == "":
        return page_une(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme), footer_content
    
    elif pathname == "/repartition-geographique":
        return page_une(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme), footer_content
    
    elif pathname == "/analyse-elegibilite":
        return page_deux(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme), footer_content
    
    elif pathname == "/evolution-temporelle":
        return page_trois(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme), footer_content
    
    elif pathname == "/analyse-predictive":
        return page_quatre(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_blue_theme), footer_content

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
    [State('upload-excel', 'filename')],
    prevent_initial_call=True
)
def handle_file_upload(contents, close_clicks, filename):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
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
            
            return success_style, html.Div([
                html.H4("Fichier Uploader avec  Succes", style={'color': 'green'}),
                html.P(f"Le fichier a été uploadé sous le nom {fixed_filename}")
            ])
        
        except Exception as e:
            # Afficher le modal d'erreur
            error_style = base_style.copy()
            error_style['display'] = 'block'
            
            return error_style, html.Div([
                html.H4("Erreur d'Upload", style={'color': 'red'}),
                html.P(f"Une erreur est survenue : {str(e)}")
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

# Lancer l'application
if __name__ == '__main__':
    
    app.run_server(debug=True)
