import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from utilss.auth_utils import get_admin_email

def page_authentification(theme, language='fr'):
    """
    Crée une page d'authentification avec formulaire d'email et mot de passe.
    Les identifiants sont vérifiés dans une base de données SQLite.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        language (str): La langue actuelle ('fr' ou 'en').
        
    Returns:
        html.Div: Le contenu de la page d'authentification.
    """
    # Définir les couleurs en fonction du thème
    if theme == 'dark':
        bg_color = '#0f172a'
        card_bg = '#0A3160'
        text_color = 'white'
        gradient = 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)'
        error_bg = 'rgba(220, 53, 69, 0.3)'  # Plus opaque pour mieux voir
        error_color = '#ff6b6b'
    else:
        bg_color = 'white'
        card_bg = 'white'
        text_color = 'black'
        gradient = 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)'
        error_bg = 'rgba(220, 53, 69, 0.2)'  # Plus opaque pour mieux voir
        error_color = '#dc3545'
    
    # Traductions
    labels = {
        'fr': {
            'title': 'Connexion',
            'email': 'Email',
            'password': 'Mot de passe',
            'button': 'Se connecter',
            'placeholder_email': 'Entrez votre email',
            'placeholder_password': 'Entrez votre mot de passe',
            'welcome': 'Bienvenue sur la plateforme de don de sang',
            'subtitle': 'Veuillez vous connecter pour accéder au tableau de bord',
            'error_message': f'Connexion impossible, veuillez faire appel à l\'administrateur au mail {get_admin_email()} pour être ajouté dans la liste des administrateurs du dashboard'
        },
        'en': {
            'title': 'Login',
            'email': 'Email',
            'password': 'Password',
            'button': 'Log in',
            'placeholder_email': 'Enter your email',
            'placeholder_password': 'Enter your password',
            'welcome': 'Welcome to the blood donation platform',
            'subtitle': 'Please log in to access the dashboard',
            'error_message': f'Connection not possible, please contact the administrator at {get_admin_email()} to be added to the dashboard administrators list'
        }
    }
    
    # Utiliser la traduction correspondante
    text = labels[language]
    
    # Style de message d'erreur amélioré
    error_message_style = {
        'color': error_color,
        'backgroundColor': error_bg,
        'padding': '12px 15px',
        'borderRadius': '4px',
        'marginBottom': '20px',
        'textAlign': 'center',
        'display': 'none',  # Initialement caché
        'fontWeight': '500',
        'border': f'1px solid {error_color}',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'
    }
    
    return html.Div([
        # Logo et titre en haut
        html.Div([
            html.Img(
                src="/assets/image_proj/blood_donation_icon.png",
                height="80px",
                style={
                    'marginBottom': '20px'
                }
            ),
            html.H1(
                text['welcome'],
                style={
                    'color': text_color,
                    'textAlign': 'center',
                    'marginBottom': '10px',
                    'fontWeight': '600'
                }
            ),
            html.P(
                text['subtitle'],
                style={
                    'color': text_color,
                    'textAlign': 'center',
                    'opacity': '0.8',
                    'marginBottom': '30px'
                }
            )
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),
        
        # Carte du formulaire avec animation subtile
        dbc.Card([
            dbc.CardBody([
                html.H2(
                    text['title'],
                    className="text-center mb-4",
                    style={
                        'color': text_color,
                        'fontWeight': '600'
                    }
                ),
                
                # Dans la fonction page_authentification, modifiez le div du message d'erreur pour inclure directement le message
                html.Div(
                    id="auth-error-message",
                    className="auth-error-pulse",
                    children=html.Div([
                        html.Strong("Identifiants incorrects", style={'fontSize': '16px', 'color': '#ffd7d7'}),
                        html.Br(),
                        html.Span("Votre email ou mot de passe est incorrect.", style={'fontSize': '14px'}),
                        html.Br(),
                        html.Span("Pour récupérer vos accès, veuillez contacter l'administrateur : "),
                        html.Br(),
                        html.A(
                            f"{get_admin_email()}", 
                            href=f"mailto:{get_admin_email()}", 
                            style={'color': '#ffbdbd', 'textDecoration': 'underline', 'fontWeight': 'bold'}
                        )
                    ]),
                    style={
                        'color': 'white',
                        'backgroundColor': 'rgba(220, 53, 69, 0.8)',
                        'padding': '15px',
                        'borderRadius': '6px',
                        'marginBottom': '20px',
                        'textAlign': 'center',
                        'fontWeight': '500',
                        'display': 'none',  # Initialement caché
                        'border': '1px solid #dc3545',
                        'boxShadow': '0 4px 8px rgba(0,0,0,0.2)',
                        'maxWidth': '100%',
                        'wordBreak': 'break-word',
                        'position': 'relative',
                        'zIndex': '1000'
                    }
                ),
                # Champ d'email
                dbc.Row([
                    dbc.Col([
                        dbc.Label(text['email'], html_for="email-input", style={'color': text_color}),
                        dbc.Input(
                            type="email",
                            id="email-input",
                            placeholder=text['placeholder_email'],
                            className="mb-4",
                            style={
                                'backgroundColor': 'rgba(255, 255, 255, 0.1)' if theme == 'dark' else 'white',
                                'color': text_color,
                                'border': '1px solid rgba(255, 255, 255, 0.2)' if theme == 'dark' else '1px solid #ced4da',
                                'borderRadius': '4px',
                                'padding': '10px 15px'
                            }
                        )
                    ])
                ], className="mb-3"),
                
                # Champ de mot de passe
                dbc.Row([
                    dbc.Col([
                        dbc.Label(text['password'], html_for="password-input", style={'color': text_color}),
                        dbc.Input(
                            type="password",
                            id="password-input",
                            placeholder=text['placeholder_password'],
                            className="mb-4",
                            style={
                                'backgroundColor': 'rgba(255, 255, 255, 0.1)' if theme == 'dark' else 'white',
                                'color': text_color,
                                'border': '1px solid rgba(255, 255, 255, 0.2)' if theme == 'dark' else '1px solid #ced4da',
                                'borderRadius': '4px',
                                'padding': '10px 15px'
                            }
                        )
                    ])
                ], className="mb-3"),
                
                # Bouton de connexion
                dbc.Button(
                    text['button'],
                    id="login-button",
                    className="mt-3 w-100",
                    style={
                        'background': gradient,
                        'border': 'none',
                        'borderRadius': '4px',
                        'padding': '12px',
                        'fontWeight': '500',
                        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                        'transition': 'all 0.3s ease'
                    }
                ),
                
                # Store pour stocker le message d'erreur localisé
                dcc.Store(id='error-message-store', data=text['error_message']),
                
                # Composant invisible pour la redirection
                dcc.Location(id='redirect-id', refresh=True)
            ])
        ], style={
            'maxWidth': '450px',
            'width': '100%',
            'margin': '0 auto',
            'backgroundColor': card_bg,
            'borderRadius': '8px',
            'boxShadow': '0 4px 20px rgba(0,0,0,0.15)' if theme == 'light' else '0 4px 20px rgba(0,0,0,0.3)',
            'border': 'none',
            'animation': 'fadeIn 0.5s ease-in-out',
            'overflow': 'hidden'
        }),
        
    ], className="d-flex flex-column justify-content-center align-items-center", style={
        'minHeight': 'calc(100vh - 160px)',  # Pour centrer verticalement, ajuster en fonction de l'en-tête/pied de page
        'backgroundColor': bg_color,
        'padding': '20px'
    })