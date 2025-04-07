import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

def page_about_us(theme, language='fr'):
    """
    Génère une page À propos élégante et professionnelle présentant l'équipe du projet.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark')
        language (str): La langue actuelle ('fr' ou 'en')
        
    Returns:
        html.Div: Composant Dash représentant la page À propos.
    """
    # Déterminer les couleurs selon le thème
    if theme == 'dark':
        bg_color = '#0f172a'
        card_bg = '#0A3160'
        text_color = 'white'
        card_shadow = '0 10px 20px rgba(0,0,0,0.7)'
        card_border = '1px solid rgba(255,255,255,0.1)'
        section_bg = 'rgba(15, 23, 42, 0.8)'
        accent_color = '#ff5757'
        light_accent = 'rgba(255, 87, 87, 0.1)'
        highlight_color = '#60a5fa'
    else:
        bg_color = '#f8f9fa'
        card_bg = 'white'
        text_color = '#333'
        card_shadow = '0 10px 20px rgba(0,0,0,0.1)'
        card_border = '1px solid rgba(0,0,0,0.08)'
        section_bg = 'rgba(255, 255, 255, 0.9)'
        accent_color = '#c42e2e'
        light_accent = 'rgba(196, 46, 46, 0.05)'
        highlight_color = '#3A7AB9'
    
    # Traductions améliorées et complétées
    translations = {
        'fr': {
            'about_title': 'Notre Équipe',
            'about_subtitle': 'Les artisans derrière ce tableau de bord sur le don de sang',
            'profile_title': 'Ingénieur Statisticien Économiste',
            'connect': 'Connectez-vous',
            'back_button': 'Retour au tableau de bord',
            'mission_title': 'Notre Mission',
            'mission_text': "Nous nous engageons à favoriser la transparence et l'accessibilité des données sur le don de sang. Notre tableau de bord vise à informer, sensibiliser et encourager les dons à travers des visualisations interactives et des analyses statistiques de qualité.",
            'project_title': 'Le Projet',
            'project_text': "Ce tableau de bord est le fruit d'une collaboration, combinant expertise statistique, data science et développement web pour créer un outil intuitif et informatif.",
            'skills': 'Compétences',
            'years_exp': 'ans d\'expérience',
            'view_profile': 'Voir le profil complet',
            'team_description': 'Une équipe passionnée avec des compétences complémentaires',
            'contact_us': 'Contactez-nous',
            'email_us': 'Envoyez-nous un courriel'
        },
        'en': {
            'about_title': 'Our Team',
            'about_subtitle': 'The experts behind this blood donation dashboard',
            'profile_title': 'Statistical Engineer Economist',
            'connect': 'Connect',
            'back_button': 'Back to dashboard',
            'mission_title': 'Our Mission',
            'mission_text': "We are committed to promoting transparency and accessibility of blood donation data. Our dashboard aims to inform, raise awareness, and encourage donations through interactive visualizations and quality statistical analysis.",
            'project_title': 'The Project',
            'project_text': "This dashboard is the result of a collaboration, combining statistical expertise, data science, and web development to create an intuitive and informative tool.",
            'skills': 'Skills',
            'years_exp': 'years of experience',
            'view_profile': 'View full profile',
            'team_description': 'A passionate team with complementary skills',
            'contact_us': 'Contact Us',
            'email_us': 'Email us'
        }
    }
    
    # Utiliser les traductions selon la langue
    t = translations[language]
    
    # Définition des données des membres de l'équipe avec des informations enrichies
    team_members = [
        {
            'name': 'NGOULOU NGOUBILI Irch',
            'image': '/assets/image_proj/team_member1.jpg',
            'linkedin': 'https://www.linkedin.com/in/marie-dupont/',
            'description': "Spécialisée en analyse de données et en modélisation statistique appliquée",
            'skills': ['Data Analysis', 'Python', 'R', 'Machine Learning'],
            'experience': 1,
            'email': 'irch.ngoulou@ensae-dakar.org'
        },
        {
            'name': 'GAKPETO Komi Hénoc',
            'image': '/assets/image_proj/team_member2.jpg',
            'linkedin': 'https://www.linkedin.com/in/jean-koffi/',
            'description': "Expert en visualisation de données et en développement d'applications interactives.",
            'skills': ['Data Visualization', 'Dash', 'JavaScript', 'D3.js'],
            'experience': 1,
            'email': 'komi.gakpeto@ensae-dakar.org'
        },
        {
            'name': 'BANZOUZI Herman',
            'image': '/assets/image_proj/team_member3.jpg',
            'linkedin': 'https://www.linkedin.com/in/aisha-ndiaye/',
            'description': "Spécialiste en Intelligence Artificielle",
            'skills': ['AI', 'Deep Learning', 'NLP', 'TensorFlow'],
            'experience': 2,
            'email': 'herman.banzouzi@ensae-dakar.org'
        },
        {
            'name': 'KOULOU Crepin',
            'image': '/assets/image_proj/team_member4.jpg',
            'linkedin': 'https://www.linkedin.com/in/moussa-diallo/',
            'description': "Data Scientist fullstack",
            'skills': ['Full Stack', 'Data Engineering', 'Cloud', 'DevOps'],
            'experience': 1,
            'email': 'crepin.koulou@ensae-dakar.org'
        }
    ]
    
    # Création des badges de compétences
    def create_skill_badges(skills):
        colors = ['primary', 'info', 'success', 'warning']
        return html.Div([
            dbc.Badge(
                skill, 
                color=colors[i % len(colors)], 
                className="me-1 mb-1",
                style={
                    'fontSize': '0.7rem', 
                    'padding': '5px 10px',
                    'borderRadius': '12px',
                    'fontWeight': 'normal'
                }
            ) for i, skill in enumerate(skills)
        ], className="mt-2 mb-2")
    
    # Création des cartes pour chaque membre de l'équipe avec un design amélioré
    team_cards = []
    for member in team_members:
        team_cards.append(
            dbc.Col(
                dbc.Card([
                    # Overlay gradient sur l'image
                    html.Div([
                        dbc.CardImg(src=member['image'], top=True, className="team-member-img", 
                                  style={'height': '220px', 'objectFit': 'cover', 'borderTopLeftRadius': '12px', 'borderTopRightRadius': '12px'}),
                        html.Div(style={
                            'position': 'absolute',
                            'top': '0',
                            'left': '0',
                            'width': '100%',
                            'height': '100%',
                            'background': 'linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0.7))',
                            'borderTopLeftRadius': '12px',
                            'borderTopRightRadius': '12px'
                        })
                    ], style={'position': 'relative'}),
                    
                    # Contenu de la carte
                    dbc.CardBody([
                        # En-tête avec nombre d'années d'expérience
                        html.Div([
                            html.Span(f"{member['experience']} {t['years_exp']}", 
                                     style={
                                         'background': accent_color, 
                                         'color': 'white', 
                                         'padding': '3px 10px', 
                                         'borderRadius': '20px', 
                                         'fontSize': '0.7rem',
                                         'fontWeight': 'bold'
                                     })
                        ], style={'position': 'absolute', 'top': '-15px', 'right': '15px'}),
                        
                        # Nom et titre
                        html.H4(member['name'], className="card-title mb-0", 
                               style={
                                   'color': accent_color, 
                                   'fontWeight': 'bold', 
                                   'fontSize': '1.2rem',
                                   'fontFamily': '"Poppins", sans-serif'
                               }),
                        
                        html.Div(
                            html.H6(
                                t['profile_title'], 
                                className="card-subtitle mt-1", 
                                style={
                                    'color': text_color, 
                                    'opacity': '0.8', 
                                    'fontSize': '0.85rem',
                                    'fontStyle': 'italic'
                                }
                            ),
                            style={'marginBottom': '10px'}
                        ),
                        
                        # Description
                        html.P(
                            member['description'], 
                            className="card-text", 
                            style={
                                'fontSize': '0.9rem', 
                                'color': text_color, 
                                'marginBottom': '12px',
                                'lineHeight': '1.4'
                            }
                        ),
                        
                        # Séparateur élégant
                        html.Hr(style={
                            'margin': '12px 0',
                            'opacity': '0.2',
                            'background': 'linear-gradient(to right, transparent, ' + text_color + ', transparent)'
                        }),
                        
                        # Compétences
                        html.H6(
                            t['skills'], 
                            style={
                                'fontSize': '0.85rem', 
                                'color': highlight_color, 
                                'marginBottom': '5px'
                            }
                        ),
                        
                        # Badges de compétences
                        create_skill_badges(member['skills']),
                        
                        # Boutons d'action
                        html.Div([
                            # Bouton LinkedIn
                            dbc.Button([
                                DashIconify(
                                    icon="mdi:linkedin",
                                    width=16,
                                    height=16,
                                    style={"marginRight": "5px"}
                                ),
                                t['connect']
                            ], 
                            href=member['linkedin'], 
                            target="_blank", 
                            color="primary", 
                            size="sm",
                            style={
                                'background': 'linear-gradient(90deg, #0077b5 0%, #0e6795 100%)', 
                                'border': 'none',
                                'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
                                'borderRadius': '20px',
                                'paddingLeft': '15px',
                                'paddingRight': '15px',
                                'marginRight': '10px'
                            }
                            ),
                            
                            # Bouton Email
                            dbc.Button([
                                DashIconify(
                                    icon="mdi:email-outline",
                                    width=16,
                                    height=16,
                                    style={"marginRight": "5px"}
                                ),
                                "Email"
                            ], 
                            href=f"mailto:{member['email']}", 
                            color="secondary",
                            size="sm",
                            style={
                                'background': 'transparent', 
                                'border': f'1px solid {accent_color}',
                                'color': accent_color,
                                'borderRadius': '20px',
                                'paddingLeft': '15px',
                                'paddingRight': '15px'
                            }
                            )
                        ], className="d-flex mt-3 justify-content-center")
                    ], style={
                        'backgroundColor': card_bg,
                        'padding': '20px',
                        'position': 'relative'
                    })
                ], 
                style={
                    'maxWidth': '320px', 
                    'margin': 'auto',
                    'backgroundColor': card_bg,
                    'boxShadow': card_shadow,
                    'border': card_border,
                    'borderRadius': '12px',
                    'transition': 'all 0.3s ease',
                    'height': '100%',
                    'overflow': 'hidden'
                },
                className="mb-4 team-card"
                ),
                md=3,
                sm=6,
                xs=12,
                className="mb-4"
            )
        )

    # Création de la section mission avec un design moderne
    mission_section = html.Div([
        dbc.Row([
            # Colonne de mission
            dbc.Col([
                html.Div([
                    html.Div([
                        DashIconify(
                            icon="mdi:target",
                            width=32,
                            height=32,
                            style={"color": accent_color, "marginBottom": "10px"}
                        ),
                        html.H3(t['mission_title'], 
                               style={
                                   'fontSize': '1.5rem', 
                                   'fontWeight': 'bold',
                                   'marginBottom': '15px',
                                   'color': accent_color
                               }),
                        html.P(t['mission_text'], 
                              style={
                                  'fontSize': '1rem',
                                  'lineHeight': '1.6',
                                  'color': text_color
                              }),
                    ], style={
                        'backgroundColor': light_accent,
                        'borderRadius': '12px',
                        'padding': '25px',
                        'height': '100%',
                        'boxShadow': '0 5px 15px rgba(0,0,0,0.05)',
                        'border': f'1px solid {card_border}'
                    })
                ])
            ], md=6, className="mb-4"),
            
            # Colonne de projet
            dbc.Col([
                html.Div([
                    html.Div([
                        DashIconify(
                            icon="mdi:chart-bubble",
                            width=32,
                            height=32,
                            style={"color": highlight_color, "marginBottom": "10px"}
                        ),
                        html.H3(t['project_title'], 
                               style={
                                   'fontSize': '1.5rem', 
                                   'fontWeight': 'bold',
                                   'marginBottom': '15px',
                                   'color': highlight_color
                               }),
                        html.P(t['project_text'], 
                              style={
                                  'fontSize': '1rem',
                                  'lineHeight': '1.6',
                                  'color': text_color
                              }),
                    ], style={
                        'backgroundColor': 'rgba(96, 165, 250, 0.05)',  # Light blue background
                        'borderRadius': '12px',
                        'padding': '25px',
                        'height': '100%',
                        'boxShadow': '0 5px 15px rgba(0,0,0,0.05)',
                        'border': f'1px solid {card_border}'
                    })
                ])
            ], md=6, className="mb-4")
        ])
    ], style={'marginBottom': '40px'})
    
    # Section de contact élégante
    contact_section = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    DashIconify(
                        icon="mdi:email-newsletter",
                        width=32,
                        height=32,
                        style={"color": accent_color, "marginRight": "15px"}
                    ),
                    html.Div([
                        html.H4(t['contact_us'], style={
                            'fontSize': '1.3rem',
                            'fontWeight': 'bold',
                            'marginBottom': '5px',
                            'color': accent_color
                        }),
                        html.P("support@blood-dashboard.org", style={
                            'fontSize': '1rem',
                            'color': text_color
                        })
                    ])
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'padding': '20px',
                    'backgroundColor': light_accent,
                    'borderRadius': '12px',
                    'marginBottom': '20px'
                }),
                
                dbc.Button([
                    DashIconify(
                        icon="mdi:email-fast",
                        width=20,
                        height=20,
                        style={"marginRight": "10px"}
                    ),
                    t['email_us']
                ], 
                href="mailto:support@blood-dashboard.org", 
                color="primary", 
                style={
                    'background': 'linear-gradient(90deg, #c42e2e 0%, #9e2b2b 100%)', 
                    'border': 'none',
                    'boxShadow': '0 4px 10px rgba(196, 46, 46, 0.3)',
                    'width': '100%',
                    'fontSize': '1rem',
                    'padding': '12px',
                    'borderRadius': '8px',
                    'marginTop': '10px'
                }),
            ], md=6, className="mx-auto text-center")
        ])
    ], style={
        'marginTop': '40px',
        'marginBottom': '40px',
        'padding': '20px',
        'backgroundColor': section_bg,
        'borderRadius': '12px',
        'boxShadow': card_shadow
    })
    
    # Création du layout de la page avec un design amélioré
    return html.Div([
        # Suppression de la ligne problématique html.Style(card_animation)
        # Ces styles sont maintenant dans about_us.css
        
        # Bannière sophistiquée en haut
        html.Div([
            # Couches de design pour la bannière
            html.Div([
                html.Div(className="blood-drop-1"),
                html.Div(className="blood-drop-2"),
                html.Div(className="blood-drop-3"),
            ], className="banner-bg-effects"),
            
            # Contenu de la bannière
            html.Div([
                html.H1(t['about_title'], className="display-4", style={
                    'color': 'white', 
                    'fontWeight': 'bold',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.5)',
                    'marginBottom': '20px',
                    'fontSize': '3rem',
                    'fontFamily': '"Montserrat", sans-serif'
                }),
                html.Div([
                    DashIconify(
                        icon="healthicons:blood-drop",
                        width=36,
                        height=36,
                        style={"color": "white", "marginRight": "15px", "marginLeft": "15px"}
                    ),
                ], style={
                    'margin': '5px auto 25px auto',
                    'opacity': '0.9'
                }),
                html.P(t['about_subtitle'], className="lead", style={
                    'color': 'white',
                    'fontSize': '1.3rem',
                    'maxWidth': '800px',
                    'margin': '0 auto',
                    'opacity': '0.9',
                    'fontWeight': '300'
                }),
                html.P(t['team_description'], style={
                    'color': 'white',
                    'marginTop': '10px',
                    'fontSize': '1rem',
                    'fontStyle': 'italic',
                    'opacity': '0.7'
                }),
            ], style={
                'position': 'relative',
                'zIndex': '2',
                'padding': '10px'
            })
        ], style={
            'background': 'linear-gradient(135deg, #c42e2e 0%, #9e2b2b 100%)',
            'padding': '70px 20px',
            'textAlign': 'center',
            'borderRadius': '12px',
            'marginBottom': '50px',
            'boxShadow': '0 10px 30px rgba(196, 46, 46, 0.3)',
            'position': 'relative',
            'overflow': 'hidden'
        }),
        
        # Sections principales
        html.Div([
            # Section Mission & Projet
            mission_section,
            
            # Séparateur élégant
            html.Div([
                html.Hr(style={
                    'width': '100px',
                    'margin': '0 auto 50px',
                    'border': 'none',
                    'height': '4px',
                    'background': 'linear-gradient(to right, transparent, ' + accent_color + ', transparent)',
                    'opacity': '0.7'
                })
            ], className="text-center"),
            
            # Section des membres de l'équipe
            html.Div([
                dbc.Row(team_cards, className="g-4 justify-content-center")
            ], style={
                'backgroundColor': section_bg,
                'padding': '40px 30px',
                'borderRadius': '12px',
                'boxShadow': card_shadow,
                'marginBottom': '40px'
            }),
            
            # Section de contact
            contact_section,
            
            # Bouton de retour avec style amélioré
            html.Div([
                dbc.Button([
                    DashIconify(
                        icon="mdi:arrow-left",
                        width=18,
                        height=18,
                        style={"marginRight": "10px"}
                    ),
                    t['back_button']
                ], 
                href="/repartition-geographique", 
                color="secondary", 
                className="mt-3",
                style={
                    'background': 'rgba(108, 117, 125, 0.8)',
                    'border': 'none',
                    'boxShadow': '0 4px 10px rgba(0,0,0,0.15)',
                    'padding': '12px 25px',
                    'fontSize': '1rem',
                    'borderRadius': '30px',
                    'transition': 'all 0.3s ease'
                })
            ], style={'textAlign': 'center', 'marginTop': '30px', 'marginBottom': '50px'})
            
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 20px'
        })
        
    ], style={
        'backgroundColor': bg_color,
        'color': text_color,
        'padding': '30px 20px',
        'minHeight': '100vh',
        'fontFamily': '"Roboto", "Helvetica Neue", Arial, sans-serif',
        'borderRadius': '0',
        'transition': 'all 0.3s ease'
    })