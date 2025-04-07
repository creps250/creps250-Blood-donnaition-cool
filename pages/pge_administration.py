import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from utilss.auth_utils import get_all_users, add_user, delete_user
import json
from utilss.auth_utils import get_admin_email

def page_administration(theme, language='fr'):
    """
    Crée une page d'administration permettant de gérer les utilisateurs.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        language (str): La langue actuelle ('fr' ou 'en').
        
    Returns:
        html.Div: Le contenu de la page d'administration.
    """
    # Définir les couleurs en fonction du thème
    if theme == 'dark':
        bg_color = '#0f172a'
        card_bg = '#0A3160'
        text_color = 'white'
        secondary_bg = 'rgba(255, 255, 255, 0.05)'
        gradient = 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)'
        success_bg = 'rgba(25, 135, 84, 0.2)'
        success_color = '#4ade80'
        error_bg = 'rgba(220, 53, 69, 0.2)'
        error_color = '#ff6b6b'
        border_color = 'rgba(255, 255, 255, 0.1)'
    else:
        bg_color = 'white'
        card_bg = 'white'
        text_color = 'black'
        secondary_bg = 'rgba(0, 0, 0, 0.03)'
        gradient = 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)'
        success_bg = 'rgba(25, 135, 84, 0.1)'
        success_color = '#198754'
        error_bg = 'rgba(220, 53, 69, 0.1)'
        error_color = '#dc3545'
        border_color = 'rgba(0, 0, 0, 0.1)'
    
    # Traductions
    labels = {
        'fr': {
            'title': 'Administration',
            'subtitle': 'Gérer les utilisateurs et les autorisations',
            'new_user': 'Nouvel utilisateur',
            'email': 'Email',
            'password': 'Mot de passe',
            'confirm_password': 'Confirmer le mot de passe',
            'is_admin': 'Est administrateur',
            'add_user': 'Ajouter utilisateur',
            'user_list': 'Liste des utilisateurs',
            'user_id': 'ID',
            'user_email': 'Email',
            'user_role': 'Rôle',
            'admin': 'Admin',
            'user': 'Utilisateur',
            'actions': 'Actions',
            'delete': 'Supprimer',
            'success_message': 'Utilisateur ajouté avec succès',
            'error_message': 'Une erreur est survenue',
            'passwords_not_match': 'Les mots de passe ne correspondent pas',
            'email_exists': 'Cet email existe déjà',
            'missing_fields': 'Tous les champs sont obligatoires',
            'admin_instructions': 'Utilisez ce formulaire pour ajouter de nouveaux administrateurs au tableau de bord.'
        },
        'en': {
            'title': 'Administration',
            'subtitle': 'Manage users and permissions',
            'new_user': 'New user',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm password',
            'is_admin': 'Is administrator',
            'add_user': 'Add user',
            'user_list': 'User list',
            'user_id': 'ID',
            'user_email': 'Email',
            'user_role': 'Role',
            'admin': 'Admin',
            'user': 'User',
            'actions': 'Actions',
            'delete': 'Delete',
            'success_message': 'User added successfully',
            'error_message': 'An error occurred',
            'passwords_not_match': 'Passwords do not match',
            'email_exists': 'This email already exists',
            'missing_fields': 'All fields are required',
            'admin_instructions': 'Use this form to add new administrators to the dashboard.'
        }
    }
    
    # Utiliser la traduction correspondante
    text = labels[language]
    
    return html.Div([
        # Titre de la page
        html.H1(
            text['title'],
            style={
                'color': text_color,
                'textAlign': 'center',
                'marginBottom': '10px',
                'marginTop': '20px',
                'fontWeight': '600'
            }
        ),
        html.P(
            text['subtitle'],
            style={
                'color': text_color,
                'textAlign': 'center',
                'marginBottom': '30px',
                'opacity': '0.8'
            }
        ),
        
        # Instructions
        dbc.Alert(
            text['admin_instructions'],
            color="info",
            className="mb-4",
            style={
                'backgroundColor': secondary_bg,
                'color': text_color,
                'border': f'1px solid {border_color}'
            }
        ),
        
        # Formulaire d'ajout d'utilisateur
        dbc.Card([
            dbc.CardHeader(
                html.H3(
                    text['new_user'], 
                    className="mb-0",
                    style={'color': text_color, 'fontWeight': '600'}
                ),
                style={'backgroundColor': secondary_bg, 'borderBottom': f'1px solid {border_color}'}
            ),
            dbc.CardBody([
                # Message de succès/erreur (initialement caché)
                html.Div(
                    id="admin-message",
                    children="",
                    style={
                        'display': 'none', 
                        'marginBottom': '15px', 
                        'padding': '10px', 
                        'borderRadius': '5px'
                    }
                ),
                
                # Formulaire
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(text['email'], html_for="new-user-email", style={'color': text_color}),
                            dbc.Input(
                                type="email",
                                id="new-user-email",
                                placeholder=text['email'],
                                required=True,
                                style={
                                    'backgroundColor': secondary_bg,
                                    'color': text_color,
                                    'border': f'1px solid {border_color}'
                                }
                            )
                        ], width=12, md=6),
                        
                        dbc.Col([
                            dbc.Label(text['password'], html_for="new-user-password", style={'color': text_color}),
                            dbc.Input(
                                type="password",
                                id="new-user-password",
                                placeholder=text['password'],
                                required=True,
                                style={
                                    'backgroundColor': secondary_bg,
                                    'color': text_color,
                                    'border': f'1px solid {border_color}'
                                }
                            )
                        ], width=12, md=6)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label(text['confirm_password'], html_for="new-user-confirm-password", style={'color': text_color}),
                            dbc.Input(
                                type="password",
                                id="new-user-confirm-password",
                                placeholder=text['confirm_password'],
                                required=True,
                                style={
                                    'backgroundColor': secondary_bg,
                                    'color': text_color,
                                    'border': f'1px solid {border_color}'
                                }
                            )
                        ], width=12, md=6),
                        
                        dbc.Col([
                            dbc.Checkbox(
                                id="new-user-is-admin",
                                label=text['is_admin'],
                                className="mt-4",
                                value=True,  # Coché par défaut
                                style={'color': text_color}
                            )
                        ], width=12, md=6, className="d-flex align-items-center")
                    ], className="mb-3"),
                    
                    dbc.Button(
                        text['add_user'],
                        id="add-user-button",
                        className="mt-3",
                        style={
                            'background': gradient,
                            'border': 'none',
                            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
                        }
                    )
                ])
            ])
        ], className="mb-4", style={
            'backgroundColor': card_bg,
            'color': text_color,
            'borderRadius': '8px',
            'overflow': 'hidden',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'border': 'none'
        }),
        
        # Liste des utilisateurs
        dbc.Card([
            dbc.CardHeader(
                html.H3(
                    text['user_list'], 
                    className="mb-0",
                    style={'color': text_color, 'fontWeight': '600'}
                ),
                style={'backgroundColor': secondary_bg, 'borderBottom': f'1px solid {border_color}'}
            ),
            dbc.CardBody([
                html.Div(id="user-list-container")
            ])
        ], style={
            'backgroundColor': card_bg,
            'color': text_color,
            'borderRadius': '8px',
            'overflow': 'hidden',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'border': 'none'
        }),
        
        # Store pour les données utilisateur
        dcc.Store(id="users-data")
        
    ], style={
        'backgroundColor': bg_color,
        'padding': '20px',
        'minHeight': 'calc(100vh - 200px)'
    })
    
    
def access_denied_page(theme, language='fr'):
    """
    Affiche une page d'accès refusé pour les utilisateurs non-administrateurs.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark').
        language (str): La langue actuelle ('fr' ou 'en').
        
    Returns:
        html.Div: La page d'accès refusé.
    """
    from dash import html
    import dash_bootstrap_components as dbc
    from dash_iconify import DashIconify as Icon
    
    # Traductions
    translations = {
        'fr': {
            'title': 'Accès refusé',
            'message': 'Vous n\'avez pas les droits d\'administrateur nécessaires pour accéder à cette page.',
            'contact': 'Si vous pensez que c\'est une erreur, veuillez contacter l\'administrateur:',
            'return': 'Retourner à la page principale'
        },
        'en': {
            'title': 'Access denied',
            'message': 'You do not have administrator rights to access this page.',
            'contact': 'If you believe this is an error, please contact the administrator:',
            'return': 'Return to main page'
        }
    }
    
    text = translations[language]
    
    # Définir le style en fonction du thème
    if theme == 'dark':
        bg_color = '#0f172a'
        text_color = 'white'
        card_bg = '#0A3160'
        border_color = 'rgba(255, 255, 255, 0.1)'
    else:
        bg_color = 'white'
        text_color = 'black'
        card_bg = 'white'
        border_color = 'rgba(0, 0, 0, 0.1)'
    
    return html.Div([
        html.Div([
            # Icône d'accès refusé
            html.Div([
                Icon(
                    icon="mdi:shield-lock-outline",
                    width=80,
                    height=80,
                    style={
                        'color': '#c42e2e',
                        'marginBottom': '20px'
                    }
                ),
                
                # Titre
                html.H2(text['title'], 
                        style={
                            'color': '#c42e2e',
                            'marginBottom': '20px',
                            'fontWeight': 'bold'
                        }),
                
                # Message
                html.P(text['message'], 
                       style={
                           'fontSize': '1.2rem',
                           'marginBottom': '15px'
                       }),
                
                # Message de contact
                html.P([
                    text['contact'],
                    html.Br(),
                    html.A(get_admin_email(), 
                           href=f"mailto:{get_admin_email()}", 
                           style={
                               'color': '#c42e2e',
                               'textDecoration': 'underline'
                           })
                ], style={'marginBottom': '30px'}),
                
                # Bouton de retour
                dbc.Button([
                    Icon(
                        icon="mdi:arrow-left",
                        width=20,
                        height=20,
                        style={"marginRight": "8px"}
                    ),
                    text['return']
                ], 
                href="/repartition-geographique", 
                color="danger", 
                className="mt-3")
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'textAlign': 'center',
                'padding': '30px',
                'backgroundColor': card_bg,
                'borderRadius': '10px',
                'border': f'1px solid {border_color}',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'color': text_color,
                'maxWidth': '600px',
                'margin': '0 auto'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'minHeight': '60vh'
        })
    ])    