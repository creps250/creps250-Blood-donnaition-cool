import dash
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from app import *
from datetime import datetime
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Input, Output, State
import requests
import time
from dash_iconify import DashIconify
import json
import plotly.express as px
import numpy as np
from utilss.functionality import *


with open("Translation/traduction_prediction.json", "r", encoding="utf-8") as fichier:
    TRANSLATIONS = json.load(fichier)


# Fonction utilitaire pour créer des icônes avec animations et effets
def page_quatre(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme, language="fr"):
    """
    Génère la page d'analyse prédictive avec des améliorations esthétiques significatives.
    
    Args:
        theme (str): Le thème actuel ('light' ou 'dark')
        plot_font_color (str): Couleur du texte pour les graphiques
        plot_bg (str): Couleur d'arrière-plan pour les graphiques
        plot_paper_bg (str): Couleur d'arrière-plan pour les graphiques
        plot_grid_color (str): Couleur de la grille pour les graphiques
        light_theme (dict): Thème clair
        dark_theme (dict): Thème sombre
        language (str): Langue ('fr' ou 'en')
        
    Returns:
        html.Div: La page d'analyse prédictive
    """
    # Thèmes et styles améliorés
    translations = TRANSLATIONS[language]
    is_dark = theme == 'dark'
    
    # Palette de couleurs sophistiquée
    colors = {
        'primary': '#e74c3c',  # Rouge sang
        'secondary': '#3498db', # Bleu
        'success': '#2ecc71',  # Vert
        'warning': '#f39c12',  # Orange
        'danger': '#c0392b',   # Rouge foncé
        'info': '#1abc9c',     # Turquoise
        'light': '#f5f5f5',    # Gris très clair
        'dark': '#2c3e50',     # Bleu foncé
        'background': dark_theme['cardBg'] if is_dark else 'white',
        'text': 'white' if is_dark else '#333',
        'border': '#4a5568' if is_dark else '#e2e8f0',
        'accent1': '#8e44ad',  # Violet
        'accent2': '#16a085',  # Vert-bleu
        'accent3': '#d35400',  # Orange foncé
        'blood': '#c0392b',    # Rouge sang foncé
    }
    
    footer_style = {
        'marginTop': '40px',
        'textAlign': 'center',
        'paddingTop': '25px',
        'paddingBottom': '15px',
        'borderTop': f'1px solid {colors["border"]}',
        'borderRadius': '0 0 15px 15px',
        'color': 'rgba(255,255,255,0.7)' if is_dark else 'rgba(0,0,0,0.6)',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'gap': '10px',
        'background': 'linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.05) 100%)'
    }
    
    # Fonds avec dégradés élégants
    gradients = {
        'primary': 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
        'primary_light': 'linear-gradient(135deg, #e57373 0%, #e74c3c 100%)',
        'secondary': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
        'secondary_light': 'linear-gradient(135deg, #64b5f6 0%, #3498db 100%)',
        'success': 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)',
        'success_light': 'linear-gradient(135deg, #81c784 0%, #2ecc71 100%)',
        'warning': 'linear-gradient(135deg, #f39c12, #e67e22 100%)',
        'warning_light': 'linear-gradient(135deg, #ffb74d, #f39c12 100%)',
        'danger': 'linear-gradient(135deg, #c0392b, #922b21 100%)',
        'danger_light': 'linear-gradient(135deg, #e74c3c, #c0392b 100%)',
        'card': 'linear-gradient(135deg, #2c3e50, #1a252f)' if is_dark else 'linear-gradient(135deg, #ffffff, #f9f9f9)',
        'section_header': 'linear-gradient(135deg, #c0392b, #e74c3c)' if is_dark else 'linear-gradient(135deg, #e74c3c, #e67e22)',
        'section_header_alt': 'linear-gradient(135deg, #2980b9, #3498db)' if is_dark else 'linear-gradient(135deg, #3498db, #2980b9)',
        'eligible': 'linear-gradient(135deg, #2ecc71, #27ae60)',
        'temp_ineligible': 'linear-gradient(135deg, #f39c12, #e67e22)',
        'def_ineligible': 'linear-gradient(135deg, #e74c3c, #c0392b)',
        'female': 'linear-gradient(135deg, #9b59b6, #8e44ad)',
    }
    
    # Styles avec ombres, dégradés et arrondis
    card_style = {
        'backgroundColor': colors['background'],
        'borderRadius': '16px',
        'boxShadow': '0 10px 25px rgba(0, 0, 0, 0.15)' if not is_dark else '0 10px 25px rgba(0, 0, 0, 0.3)',
        'border': f'1px solid {colors["border"]}',
        'padding': '0',
        'marginBottom': '30px',
        'color': colors['text'],
        'overflow': 'hidden',
        'transition': 'all 0.3s ease',
        'position': 'relative',
        'transform': 'translateZ(0)'
    }
    
    card_header_style = {
        'background': gradients['section_header'],
        'color': 'white',
        'padding': '18px 22px',
        'fontWeight': 'bold',
        'borderTopLeftRadius': '15px',
        'borderTopRightRadius': '15px',
        'display': 'flex',
        'alignItems': 'center',
        'borderBottom': '0',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'position': 'relative',
        'overflow': 'hidden'
    }
    
    # Ajouter un effet de "glow" pour le thème sombre
    if is_dark:
        card_header_style['boxShadow'] += ', 0 0 15px rgba(231, 76, 60, 0.3)'
        
    female_header_style = {**card_header_style, 'background': gradients['female']}
    alternate_header_style = {**card_header_style, 'background': gradients['section_header_alt']}
    
    card_body_style = {
        'padding': '25px 22px',
        'backgroundColor': colors['background'],  
        'color': colors['text'], 
        'borderBottomLeftRadius': '15px',
        'borderBottomRightRadius': '15px',
        'position': 'relative',
        'zIndex': '1'
    }
    
    section_title_style = {
        'color': 'white',
        'marginBottom': '0',
        'fontWeight': 'bold',
        'fontSize': '1.25rem',
        'display': 'flex',
        'alignItems': 'center',
        'letterSpacing': '0.5px',
        'textShadow': '1px 1px 2px rgba(0, 0, 0, 0.2)'
    }
    
    label_style = {
        'fontWeight': '600', 
        'marginBottom': '10px',
        'color': light_theme['textColor'] if theme == 'light' else 'rgba(255, 255, 255, 0.9)',
        'fontSize': '0.95rem',
        'display': 'flex',
        'alignItems': 'center',
        'gap': '8px',
        'transition': 'all 0.2s ease'
    }
    
    input_style = {
        'width': '100%', 
        'padding': '12px 15px', 
        'borderRadius': '10px', 
        'border': f'1px solid {colors["border"]}',
        'backgroundColor': 'rgba(0,0,0,0.05)' if theme == 'dark' else 'white',
        'color': colors['text'],
        'boxShadow': 'inset 0 2px 4px rgba(0,0,0,0.05)',
        'transition': 'all 0.3s ease',
        'fontSize': '1rem',
        'fontFamily': 'inherit',
        'outline': 'none',
        '&:focus': {
            'borderColor': colors['primary'],
            'boxShadow': f'0 0 0 3px rgba(231, 76, 60, 0.2)'
        }
    }
    
    dropdown_style = {
        'borderRadius': '10px',
        'border': f'1px solid {colors["border"]}',
        'color': colors['text'] if theme == 'light' else "black",
        'backgroundColor': 'rgba(0,0,0,0.05)' if theme == 'dark' else 'white',
        'fontFamily': 'inherit',
        '&:hover': {
            'borderColor': colors['primary']
        }
    }
    
    button_style = {
        'background': gradients['primary'],
        'color': 'white',
        'border': 'none',
        'borderRadius': '12px',
        'padding': '15px 30px',
        'fontSize': '18px',
        'fontWeight': 'bold',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'boxShadow': '0 4px 15px rgba(231, 76, 60, 0.4), 0 8px 10px -5px rgba(231, 76, 60, 0.2)',
        'width': '100%',
        'marginTop': '10px',
        'textTransform': 'uppercase',
        'letterSpacing': '1px',
        'position': 'relative',
        'overflow': 'hidden',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'gap': '10px',
        '&:hover': {
            'transform': 'translateY(-2px)',
            'boxShadow': '0 7px 20px rgba(231, 76, 60, 0.5), 0 10px 10px -5px rgba(231, 76, 60, 0.3)'
        },
        '&:active': {
            'transform': 'translateY(1px)',
            'boxShadow': '0 3px 10px rgba(231, 76, 60, 0.4), 0 6px 8px -8px rgba(231, 76, 60, 0.2)'
        }
    }
    
    reset_button_style = {
        'background': 'transparent',
        'color': colors['text'],
        'border': f'1px solid {colors["border"]}',
        'borderRadius': '12px',
        'padding': '12px 20px',
        'fontSize': '16px',
        'fontWeight': 'bold',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'boxShadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
        'width': 'auto',
        'marginTop': '10px',
        'textTransform': 'uppercase',
        'letterSpacing': '1px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'gap': '5px',
        '&:hover': {
            'background': 'rgba(0, 0, 0, 0.05)',
            'transform': 'translateY(-1px)',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.15)'
        }
    }
    
    # Créer des options pour les sliders
    hemoglobin_slider_marks = {i: {'label': f'{i}', 'style': {'color': colors['text']}} for i in range(8, 21, 2)}
    
    # Ajouter un style CSS personnalisé pour les animations et les effets
    """
    custom_css = html.Style('''
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }
        
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-5px);
            }
        }
        
        @keyframes spin {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }
        
        @keyframes floatUp {
            0% {
                transform: translateY(0) rotate(0);
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                transform: translateY(-20px) rotate(10deg);
                opacity: 0;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.8s ease-out forwards;
        }
        
        .fade-in-up {
            animation: fadeInUp 0.8s ease-out forwards;
        }
        
        .fade-in-scale {
            animation: fadeInScale 0.5s ease-out forwards;
        }
        
        .fade-in-delay {
            animation: fadeIn 0.8s ease-out 0.3s forwards;
            opacity: 0;
        }
        
        .icon-pulse {
            animation: pulse 2s infinite ease-in-out;
        }
        
        .icon-bounce {
            animation: bounce 2s infinite ease-in-out;
        }
        
        .icon-spin {
            animation: spin 10s linear infinite;
        }
        
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
        }
        
        .custom-scrollbar::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.05);
            border-radius: 10px;
        }
        
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(172, 67, 54, 0.4);
            border-radius: 10px;
        }
        
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(172, 67, 54, 0.6);
        }
        
        .hover-scale {
            transition: transform 0.3s ease;
        }
        
        .hover-scale:hover {
            transform: scale(1.02);
        }
        
        .blood-btn {
            position: relative;
            overflow: hidden;
        }
        
        .blood-btn::before {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            background: radial-gradient(circle, rgba(231, 76, 60, 0.2) 0%, rgba(231, 76, 60, 0) 70%);
            transform: scale(0);
            transition: transform 0.5s;
            z-index: -1;
        }
        
        .blood-btn:hover::before {
            transform: scale(1);
        }
        
        .blood-drop {
            width: 8px;
            height: 8px;
            background-color: rgba(231, 76, 60, 0.7);
            border-radius: 50% 50% 50% 0;
            position: absolute;
            transform: rotate(-45deg);
            animation: floatUp 3s linear infinite;
        }
        
        @media (max-width: 768px) {
            .flex-container {
                flex-direction: column;
            }
            
            .reasons-box, .recommendations-box {
                margin-right: 0 !important;
                margin-bottom: 20px;
            }
        }
        
        .radio-button-custom input[type='radio'] {
            appearance: none;
            width: 18px;
            height: 18px;
            border: 2px solid #ccc;
            border-radius: 50%;
            outline: none;
            transition: border 0.3s ease;
        }
        
        .radio-button-custom input[type='radio']:checked {
            border: 5px solid #e74c3c;
        }
        
        .slider-custom {
            height: 10px;
            border-radius: 5px;
        }
        
        .slider-custom .rc-slider-track {
            background-color: #e74c3c;
            height: 10px;
            border-radius: 5px;
        }
        
        .slider-custom .rc-slider-handle {
            border: solid 2px #e74c3c;
            margin-top: -5px;
            width: 20px;
            height: 20px;
            background-color: white;
        }
        
        .tooltip-container {
            position: relative;
            display: inline-block;
        }
        
        .tooltip-content {
            visibility: hidden;
            width: 220px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -110px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 12px;
            line-height: 1.5;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        
        .tooltip-container:hover .tooltip-content {
            visibility: visible;
            opacity: 1;
        }
        
        .tooltip-content::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #555 transparent transparent transparent;
        }
        
        .info-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(231, 76, 60, 0.15);
            color: #e74c3c;
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 8px;
            cursor: default;
            transition: all 0.3s ease;
        }
        
        .info-badge:hover {
            background: rgba(231, 76, 60, 0.25);
        }
        
        .shimmer {
            position: relative;
            overflow: hidden;
        }
        
        .shimmer::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                to right,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.1) 50%,
                rgba(255, 255, 255, 0) 100%
            );
            transform: rotate(30deg);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% {
                transform: translateX(-100%) rotate(30deg);
            }
            100% {
                transform: translateX(100%) rotate(30deg);
            }
        }
    ''')
    """
    # Affichage du profil et des statistiques basiques
    bmi_preview = html.Div([
        html.Div([
            html.H5([
                get_icon("mdi:calculator", 18, colors['info']),
                html.Span(translations.get("BMI approximatif", "BMI approximatif"), style={'marginLeft': '5px'})
            ], style={
                'fontSize': '1rem',
                'fontWeight': 'bold',
                'color': colors['info'],
                'display': 'flex',
                'alignItems': 'center',
                'marginBottom': '10px'
            }),
            html.Div(id="bmi-display", style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'padding': '15px',
                'backgroundColor': 'rgba(26, 188, 156, 0.1)',
                'borderRadius': '10px',
                'marginTop': '5px',
                'height': '100px',
                'position': 'relative'
            }, className="hover-scale")
        ], style={
            'padding': '15px',
            'backgroundColor': 'rgba(0, 0, 0, 0.02)',
            'borderRadius': '12px',
            'marginTop': '15px',
            'marginBottom': '10px',
            'transition': 'all 0.3s ease'
        })
    ])
    
    # Ajouter une note de confidentialité
    privacy_notice = html.Div([
        html.Div([
            html.Div([
                get_icon("mdi:shield-check", 20, colors['info']),
                html.Span(translations.get("Vos informations sont protégées", "Vos informations sont protégées"), style={
                    'fontWeight': 'bold',
                    'fontSize': '14px',
                    'color': colors['info'],
                    'marginLeft': '8px'
                })
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'marginBottom': '5px'
            }),
            html.P("Vos données personnelles ne sont pas stockées. Elles sont utilisées uniquement pour la prédiction.", 
                  style={
                      'fontSize': '12px',
                      'margin': 0,
                      'color': 'rgba(26, 188, 156, 0.8)'
                  })
        ], style={
            'padding': '10px 15px',
            'backgroundColor': 'rgba(26, 188, 156, 0.1)',
            'borderRadius': '10px',
            'marginTop': '15px',
            'marginBottom': '0px',
            'borderLeft': '3px solid rgba(26, 188, 156, 0.6)'
        })
    ])
    
    # Ajouter des bulles de sang décoratifs pour le design
    blood_decorations = html.Div([
        # Ces bulles apparaîtront uniquement pour les clients avec JS activé
        html.Div(className="blood-drop", style={'left': '5%', 'top': '30%', 'animationDelay': '0s'}),
        html.Div(className="blood-drop", style={'left': '10%', 'top': '40%', 'animationDelay': '0.5s'}),
        html.Div(className="blood-drop", style={'left': '15%', 'top': '50%', 'animationDelay': '1s'}),
        html.Div(className="blood-drop", style={'left': '20%', 'top': '60%', 'animationDelay': '1.5s'}),
        html.Div(className="blood-drop", style={'left': '25%', 'top': '70%', 'animationDelay': '2s'}),
        html.Div(className="blood-drop", style={'left': '90%', 'top': '30%', 'animationDelay': '0.3s'}),
        html.Div(className="blood-drop", style={'left': '85%', 'top': '40%', 'animationDelay': '0.8s'}),
        html.Div(className="blood-drop", style={'left': '80%', 'top': '50%', 'animationDelay': '1.3s'}),
        html.Div(className="blood-drop", style={'left': '75%', 'top': '60%', 'animationDelay': '1.8s'}),
        html.Div(className="blood-drop", style={'left': '70%', 'top': '70%', 'animationDelay': '2.3s'})
    ], style={
        'position': 'absolute',
        'width': '100%',
        'height': '100%',
        'zIndex': '0',
        'overflow': 'hidden',
        'pointerEvents': 'none'
    })
    
    
    
    # Interface utilisateur principale
    return html.Div([
        #custom_css,  # Styles CSS personnalisés pour les animations
        dbc.Row([
            # Bannière supérieure avec message informatif
            dbc.Col([
                html.Div([
                    get_icon("mdi:blood-bag", 24, "white", with_animation=True),
                    html.H3(translations.get("Simuler votre éligibilité", "Simuler votre éligibilité"), 
                           style={
                               'color': 'white',
                               'margin': '0 0 0 10px',
                               'fontWeight': 'bold',
                               'fontSize': '1.3rem',
                               'letterSpacing': '0.5px',
                               'textShadow': '1px 1px 3px rgba(0, 0, 0, 0.2)'
                           })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'background': gradients['primary'],
                    'padding': '15px 20px',
                    'borderRadius': '12px',
                    'marginBottom': '25px',
                    'boxShadow': '0 4px 10px rgba(231, 76, 60, 0.3)',
                    'position': 'relative',
                    'overflow': 'hidden'
                }, className="shimmer")
            ], width=12, className="fade-in-up")
        ], className="mb-4"),
        
        dbc.Row([
            # Colonne 1: Formulaire (Données démographiques et médicales générales)
            dbc.Col([
                # Données démographiques avec une carte améliorée
                html.Div([
                    html.Div([
                        html.Div([
                            get_icon("mdi:account-details", 24, "white"),
                            html.H3(translations["Données Démographiques"], style=section_title_style)
                        ])
                    ], style=card_header_style),
                    
                    html.Div([
                        # Première ligne: Genre et Âge
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:gender-male-female", 18),
                                    translations["Genre"],
                                    html.Span("*", style={'color': colors['primary'], 'marginLeft': '3px'})
                                ], style=label_style),
                                html.Div([
                                    dcc.Dropdown(
                                        id="genre",
                                        options=[
                                            {"label": translations["Homme"], "value": "Homme"},
                                            {"label": translations["Femme"], "value": "Femme"}
                                        ],
                                        value="Homme",
                                        style={**dropdown_style, 'width': '100%'},
                                        className="mb-3"
                                    )
                                ], style={'position': 'relative'})
                            ], width=6),
                            
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:cake-variant", 18),
                                    translations["Âge"],
                                    html.Span("*", style={'color': colors['primary'], 'marginLeft': '3px'}),
                                    html.Div([
                                        html.Span("18-65", className="info-badge")
                                    ], className="tooltip-container", style={'display': 'inline-block', 'marginLeft': '10px'})
                                ], style=label_style),
                                dcc.Input(
                                    id="age",
                                    type="number",
                                    placeholder=f"{translations['Âge']}",
                                    min=18,
                                    max=65,
                                    value=30,
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Deuxième ligne: Niveau d'études et Situation Matrimoniale
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:school", 18),
                                    translations["Niveau d'études"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="niveau_etude",
                                    options=[
                                        {"label": translations["Primaire"], "value": "Primaire"},
                                        {"label": translations["Secondaire"], "value": "Secondaire"},
                                        {"label": translations["Universitaire"], "value": "Universitaire"},
                                        {"label": translations["Pas Précisé"], "value": "Pas Précisé"},
                                        {"label": translations["Aucun"], "value": "Aucun"}
                                    ],
                                    value="Secondaire",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:ring", 18),
                                    translations["Situation Matrimoniale"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="situation_matrimoniale",
                                    options=[
                                        {"label": translations["Célibataire"], "value": "Célibataire"},
                                        {"label": translations["Marié (e)"], "value": "Marié (e)"},
                                        {"label": translations["Divorcé(e)"], "value": "Divorcé(e)"},
                                        {"label": translations["veuf (veuve)"], "value": "veuf (veuve)"},
                                    ],
                                    value="Célibataire",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Troisième ligne: Religion et Profession
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:church", 18),
                                    translations["Religion"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="religion",
                                    options=[
                                        {"label": translations["Chrétien (Catholique)"], "value": "chrétien (catholique)"},
                                        {"label": translations["Chrétien (Protestant)"], "value": "chrétien (protestant)"},
                                        {"label": translations["Musulman"], "value": "Musulman"},
                                        {"label": translations["Pas Précisé"], "value": "Pas Précisé"}
                                    ],
                                    value="chrétien (catholique)",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:briefcase", 18),
                                    translations["Profession"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="profession",
                                    options = [
                                        {"label": translations["Agent de sécurité"], "value": "Agent de sécurité"},
                                        {"label": translations["Agent immobilier"], "value": "Agent immobilier"},
                                        {"label": translations["Assistant administratif"], "value": "Assistant administratif"},
                                        {"label": translations["Commerçant"], "value": "Commerçant"},
                                        {"label": translations["Conducteur"], "value": "Conducteur"},
                                        {"label": translations["Électricien"], "value": "Électricien"},
                                        {"label": translations["Enseignant"], "value": "Enseignant"},
                                        {"label": translations["Étudiant-Eleve"], "value": "Étudiant-Eleve"},
                                        {"label": translations["Informaticien"], "value": "Informaticien"},
                                        {"label": translations["Infirmier"], "value": "Infirmier"},
                                        {"label": translations["Ingénieur"], "value": "Ingénieur"},
                                        {"label": translations["Personnel de santé"], "value": "Personnel de santé"},
                                        {"label": translations["Sans emploi"], "value": "Sans emploi"},
                                        {"label": translations["Technicien"], "value": "Technicien"},
                                        {"label": translations["Autres"], "value": "Autres"}
                                    ],
                                    placeholder=translations["Profession"],
                                    value="Étudiant-Eleve",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Quatrième ligne: Taille et Poids
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:human-male-height", 18),
                                    translations["Taille (cm)"],
                                    html.Span("*", style={'color': colors['primary'], 'marginLeft': '3px'})
                                ], style=label_style),
                                dcc.Input(
                                    id="taille",
                                    type="number",
                                    placeholder=f"{translations['Taille (cm)']}",
                                    min=140,
                                    max=220,
                                    value=170,
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:weight", 18),
                                    translations["Poids (kg)"],
                                    html.Span("*", style={'color': colors['primary'], 'marginLeft': '3px'})
                                ], style=label_style),
                                dcc.Input(
                                    id="poids",
                                    type="number",
                                    placeholder=f"{translations['Poids (kg)']}",
                                    min=45,
                                    max=150,
                                    value=70,
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Affichage de l'IMC
                        bmi_preview,
                        
                        # Cinquième ligne: Arrondissement et Quartier
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:map-marker", 18),
                                    translations["Arrondissement de résidence"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="arrondissement_de_residence",
                                    options = [
                                        {"label": "Douala 1", "value": "douala 1"},
                                        {"label": "Douala 2", "value": "douala 2"},
                                        {"label": "Douala 3", "value": "douala 3"},
                                        {"label": "Douala 4", "value": "douala 4"},
                                        {"label": "Douala 5", "value": "douala 5"},
                                        {"label": "Yaoundé", "value": "Yaoundé"},
                                        {"label": "Autres", "value": "Autres"}
                                    ],
                                    placeholder="Arrondissement",
                                    value="douala 3",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:home-city", 18),
                                    translations["Quartier de résidence"]
                                ], style=label_style),
                                dcc.Input(
                                    id="quartier_residence",
                                    type="text",
                                    placeholder=f"{translations['Quartier de résidence']}",
                                    value="Makepe",
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
                        # Sixième ligne: Nationalité
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:flag", 18),
                                    translations["Nationalité"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="nationalite",
                                    options = [
                                        {"label": translations["Camerounaise"], "value": "Camerounaise"},
                                        {"label": translations["Etranger"], "value": "Etranger"}
                                    ],
                                    value="Camerounaise",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=12)
                        ]),
                    ], style=card_body_style)
                ], style=card_style, className="mb-4 hover-scale fade-in"),
                
                # Données médicales générales
                html.Div([
                    html.Div([
                        html.Div([
                            get_icon("mdi:medical-bag", 24, "white"),
                            html.H3(translations["Données de santé"], style=section_title_style)
                        ])
                    ], style=alternate_header_style),
                    
                    html.Div([
                        # Taux d'hémoglobine avec slider amélioré
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:water", 18),
                                    translations["Taux d'hémoglobine (g/dL)"],
                                    html.Div([
                                        html.Span(translations.get("Important", "Important"), className="info-badge"),
                                        html.Div(className="tooltip-content", children=[
                                            html.P("Les valeurs normales sont généralement comprises entre 13-17 g/dL pour les hommes et 12-15 g/dL pour les femmes.", 
                                                  style={'margin': '0 0 5px 0'}),
                                            html.P("Un taux inférieur à 12.5 g/dL peut être un facteur d'inéligibilité temporaire.",
                                                 style={'margin': '0'})
                                        ])
                                    ], className="tooltip-container", style={'display': 'inline-block', 'marginLeft': '8px'})
                                ], style=label_style),
                                html.Div([
                                    html.Div(id="hemoglobin-value-display", style={
                                        'textAlign': 'center',
                                        'fontWeight': 'bold',
                                        'color': colors['primary'],
                                        'fontSize': '1.2rem',
                                        'margin': '0 0 10px 0'
                                    }),
                                    dcc.Slider(
                                        id="taux_hemoglobine",
                                        min=8,
                                        max=20,
                                        step=0.1,
                                        value=13.5,
                                        marks=hemoglobin_slider_marks,
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        className="mb-4 slider-custom",
                                    )
                                ], style={
                                    'padding': '10px 15px',
                                    'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                    'borderRadius': '10px',
                                    'marginBottom': '15px'
                                })
                            ], width=12)
                        ]),
                        
                        # A déjà donné le sang
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:history", 18),
                                    translations["A déjà donné le sang"]
                                ], style=label_style),
                                dcc.RadioItems(
                                    id="a_deja_donne",
                                    options=[
                                        {"label": translations["Oui"], "value": "Oui"},
                                        {"label": translations["Non"], "value": "Non"}
                                    ],
                                    value="Non",
                                    style={
                                        'display': 'flex', 
                                        'gap': '30px',
                                        'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                        'padding': '10px 20px',
                                        'borderRadius': '10px'
                                    },
                                    className="mb-3 radio-button-custom",
                                    labelStyle={
                                        'display': 'flex', 
                                        'alignItems': 'center', 
                                        'gap': '8px',
                                        'cursor': 'pointer',
                                        'padding': '8px',
                                        'borderRadius': '4px',
                                        'transition': 'background-color 0.2s',
                                        'fontWeight': 'bold'
                                    }
                                )
                            ], width=12)
                        ]),
                        
                        # Date du dernier don (conditionnelle)
                        dbc.Row([
                            dbc.Col([
                                html.Div(id="date_dernier_don_container", style={"display": "none"}, children=[
                                    html.Label([
                                        get_icon("mdi:calendar", 18),
                                        translations["Date du dernier don"]
                                    ], style=label_style),
                                    html.Div([
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label(translations["Mois"], style={
                                                    'fontSize': '0.85rem', 
                                                    'marginBottom': '5px',
                                                    'fontWeight': 'bold'
                                                }),
                                                dcc.Dropdown(
                                                    id="mois_dernier_don",
                                                    options=[{"label": m, "value": i+1} for i, m in enumerate([
                                                        translations["Janvier"], translations["Février"], translations["Mars"], 
                                                        translations["Avril"], translations["Mai"], translations["Juin"], 
                                                        translations["Juillet"], translations["Août"], translations["Septembre"], 
                                                        translations["Octobre"], translations["Novembre"], translations["Décembre"]
                                                    ])],
                                                    value=1,
                                                    style=dropdown_style,
                                                )
                                            ], width=6),
                                            dbc.Col([
                                                html.Label(translations["Année"], style={
                                                    'fontSize': '0.85rem', 
                                                    'marginBottom': '5px',
                                                    'fontWeight': 'bold'
                                                }),
                                                dcc.Dropdown(
                                                    id="annee_dernier_don",
                                                    options=[{"label": str(year), "value": year} for year in range(2020, 2026)],
                                                    value=2024,
                                                    style=dropdown_style,
                                                )
                                            ], width=6)
                                        ]),
                                        html.Div([
                                            get_icon("mdi:information-outline", 16, colors['info']),
                                            html.Span("Un délai minimum de 3 mois est recommandé entre deux dons", style={
                                                'fontSize': '0.8rem',
                                                'color': colors['info'],
                                                'marginLeft': '5px'
                                            })
                                        ], style={
                                            'marginTop': '8px',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'backgroundColor': 'rgba(52, 152, 219, 0.1)',
                                            'padding': '5px 10px',
                                            'borderRadius': '5px'
                                        })
                                    ], style={
                                        'padding': '15px',
                                        'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                        'borderRadius': '10px',
                                        'marginTop': '10px',
                                        'marginBottom': '15px',
                                        'animation': 'fadeIn 0.5s',
                                        'border': '1px solid rgba(231, 76, 60, 0.2)'
                                    }, className="fade-in")
                                ])
                            ], width=12)
                        ]),
                        
                        # Est sous anti-biothérapie / IST récente
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:pill", 18),
                                    translations["Est sous anti-biothérapie"]
                                ], style=label_style),
                                dcc.RadioItems(
                                    id="anti_biotherapie",
                                    options=[
                                        {"label": translations["oui"], "value": "oui"},
                                        {"label": translations["non"], "value": "non"}
                                    ],
                                    value="non",
                                    style={
                                        'display': 'flex', 
                                        'gap': '20px',
                                        'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                        'padding': '8px 15px',
                                        'borderRadius': '8px'
                                    },
                                    className="mb-3 radio-button-custom",
                                    labelStyle={
                                        'display': 'flex', 
                                        'alignItems': 'center', 
                                        'gap': '5px',
                                        'cursor': 'pointer',
                                        'padding': '5px',
                                        'borderRadius': '4px',
                                        'transition': 'background-color 0.2s',
                                        'fontWeight': 'bold'
                                    }
                                )
                            ], width=6),
                            
                            # IST récente
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:virus", 18),
                                    translations["IST récente"]
                                ], style=label_style),
                                dcc.RadioItems(
                                    id="ist_recente",
                                    options=[
                                        {"label": translations["oui"], "value": "oui"},
                                        {"label": translations["non"], "value": "non"}
                                    ],
                                    value="non",
                                    style={
                                        'display': 'flex', 
                                        'gap': '20px',
                                        'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                        'padding': '8px 15px',
                                        'borderRadius': '8px'
                                    },
                                    className="mb-3 radio-button-custom",
                                    labelStyle={
                                        'display': 'flex', 
                                        'alignItems': 'center', 
                                        'gap': '5px',
                                        'cursor': 'pointer',
                                        'padding': '5px',
                                        'borderRadius': '4px',
                                        'transition': 'background-color 0.2s',
                                        'fontWeight': 'bold'
                                    }
                                )
                            ], width=6)
                        ]),
                        
                        # Note sur la confidentialité
                        privacy_notice
                    ], style=card_body_style)
                ], style=card_style, className="hover-scale fade-in"),
            ], md=6, className="mb-4"),
            
            # Colonne 2: Antécédents et conditions spécifiques
            dbc.Col([
                # Antécédents médicaux
                html.Div([
                    html.Div([
                        html.Div([
                            get_icon("mdi:heart-pulse", 24, "white"),
                            html.H3(translations["Antécédents et Conditions Médicales"], style=section_title_style)
                        ])
                    ], style=card_header_style),
                    
                    html.Div([
                        dbc.Row([
                            # Première colonne d'antécédents
                            dbc.Col([
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:blood-bag", 16),
                                        translations["Antécédent de transfusion"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="antecedent_transfusion",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:shield-cross", 16),
                                        translations["Porteur (HIV, Hbs, Hcv)"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="porteur_hiv",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:hospital-building", 16),
                                        translations["Opéré récemment"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="opere_recemment",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:dna", 16),
                                        translations["Drépanocytaire"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="drepanocytaire",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:diabetes", 16),
                                        translations["Diabétique"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="diabetique",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3")
                            ], width=6),
                            
                            # Deuxième colonne d'antécédents
                            dbc.Col([
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:blood-pressure", 16),
                                        translations["Hypertendu"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="hypertendu",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:lungs", 16),
                                        translations["Asthmatique"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="asthmatique",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:heart", 16),
                                        translations["Cardiaque"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="cardiaque",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:draw-pen", 16),
                                        translations["Tatoué"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="tatoue",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                                
                                html.Div([
                                    html.Label([
                                        get_icon("mdi:knife", 16),
                                        translations["Scarifié"]
                                    ], style=label_style),
                                    dcc.RadioItems(
                                        id="scarifie",
                                        options=[
                                            {"label": translations["oui"], "value": "oui"},
                                            {"label": translations["non"], "value": "non"}
                                        ],
                                        value="non",
                                        style={
                                            'display': 'flex', 
                                            'gap': '20px',
                                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                                            'padding': '8px 15px',
                                            'borderRadius': '8px'
                                        },
                                        className="mb-3 radio-button-custom",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '5px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ], className="mb-3"),
                            ], width=6)
                        ]),
                    ], style=card_body_style)
                ], style=card_style, className="mb-4 hover-scale fade-in"),
                
                # Section spécifique femmes avec des styles améliorés et des animations
                html.Div(
                    html.Div([
                        html.Div([
                            html.Div([
                                get_icon("mdi:human-female", 24, "white"),
                                html.H3(translations["Section Femmes"], style=section_title_style)
                            ])
                        ], style=female_header_style),
                        
                        html.Div([
                            dbc.Row([
                                # Première colonne
                                dbc.Col([
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:calendar-today", 16),
                                            translations["DDR <14 jours avant le don"],
                                            html.Div([
                                                html.Span(translations.get("Informations supplémentaires", "Informations supplémentaires"), className="info-badge"),
                                                html.Div(className="tooltip-content", children=[
                                                    html.P("DDR = Date des Dernières Règles. Si vos dernières règles datent de moins de 14 jours, cela peut affecter votre éligibilité temporairement.", 
                                                        style={'margin': '0'})
                                                ])
                                            ], className="tooltip-container", style={'display': 'inline-block', 'marginLeft': '8px'})
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="ddr_recent",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={
                                                'display': 'flex', 
                                                'gap': '20px',
                                                'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                                                'padding': '8px 15px',
                                                'borderRadius': '8px'
                                            },
                                            className="mb-3 radio-button-custom",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '5px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ], className="mb-3 fade-in"),
                                    
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:baby-bottle-outline", 16),
                                            translations["Allaitement"]
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="allaitement",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={
                                                'display': 'flex', 
                                                'gap': '20px',
                                                'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                                                'padding': '8px 15px',
                                                'borderRadius': '8px'
                                            },
                                            className="mb-3 radio-button-custom",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '5px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ], className="mb-3 fade-in"),
                                ], width=6),
                                
                                # Deuxième colonne
                                dbc.Col([
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:baby-face-outline", 16),
                                            translations["Accouchement récent"]
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="accouchement_recent",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={
                                                'display': 'flex', 
                                                'gap': '20px',
                                                'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                                                'padding': '8px 15px',
                                                'borderRadius': '8px'
                                            },
                                            className="mb-3 radio-button-custom",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '5px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ], className="mb-3 fade-in"),
                                    
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:medical-bag", 16),
                                            translations["Interruption de grossesse récente"]
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="interruption_grossesse",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={
                                                'display': 'flex', 
                                                'gap': '20px',
                                                'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                                                'padding': '8px 15px',
                                                'borderRadius': '8px'
                                            },
                                            className="mb-3 radio-button-custom",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '5px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ], className="mb-3 fade-in"),
                                ], width=6)
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:human-pregnant", 16),
                                            translations["Enceinte"],
                                            html.Div([
                                                html.Span("Important", className="info-badge"),
                                                html.Div(className="tooltip-content", children=[
                                                    html.P("La grossesse est une contre-indication temporaire au don de sang pour protéger la santé de la mère et du fœtus.", 
                                                        style={'margin': '0'})
                                                ])
                                            ], className="tooltip-container", style={'display': 'inline-block', 'marginLeft': '8px'})
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="enceinte",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={
                                                'display': 'flex', 
                                                'gap': '20px',
                                                'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                                                'padding': '8px 15px',
                                                'borderRadius': '8px'
                                            },
                                            className="mb-3 radio-button-custom",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '5px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                                'fontWeight': 'bold'
                                            }
                                        )
                                    ], className="mb-3 fade-in"),
                                ], width=12)
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.Label([
                                        get_icon("mdi:file-document-edit", 16),
                                        translations["Autre raison d'indisponibilité (femme)"]
                                    ], style=label_style),
                                    dcc.Input(
                                        id="autre_raison_indispo_femme",
                                        type="text",
                                        placeholder="Précisez si autre raison (facultatif)",
                                        style={
                                            **input_style,
                                            'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                                            'border': '1px solid rgba(155, 89, 182, 0.3)'
                                        },
                                        className="mb-3"
                                    )
                                ], width=12, className="fade-in")
                            ])
                        ], style=card_body_style)
                    ], style={
                        **card_style,
                        'boxShadow': '0 10px 25px rgba(155, 89, 182, 0.2)' if not is_dark else '0 10px 25px rgba(155, 89, 182, 0.3)',
                        'borderColor': 'rgba(155, 89, 182, 0.3)'
                    }),
                    id="section-femmes",
                    style={"display": "none"}
                ),
                
                # Autre raison d'inéligibilité (pour tous)
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:file-document-edit", 18),
                                    translations["Autre raison d'inéligibilité"]
                                ], style=label_style),
                                dcc.Input(
                                    id="autre_raison_ineligible",
                                    type="text",
                                    placeholder="Précisez si autre raison d'inéligibilité (facultatif)",
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=12)
                        ])
                    ], style=card_body_style)
                ], style=card_style, className="mb-4 hover-scale fade-in"),
                
                # Boutons d'action avec effet et animations
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            # Bouton de réinitialisation
                            dbc.Button(
                                [
                                    get_icon("mdi:refresh", 16, colors['text']),
                                    translations.get("Réinitialiser", "Réinitialiser")
                                ],
                                id="reset-button",
                                style=reset_button_style,
                                className="mr-2"
                            )
                        ], width=4),
                        dbc.Col([
                            # Bouton de prédiction principal avec chargement
                            dcc.Loading(
                                id="loading-prediction",
                                type="circle",
                                color=colors['primary'],
                                children=[
                                    dbc.Button(
                                        [
                                            get_icon("mdi:calculator-check", 20, "white", with_animation=True),
                                            html.Span(translations["Prédire l'éligibilité"], style={'marginLeft': '8px'})
                                        ],
                                        id="predict-button",
                                        className="blood-btn mt-3 mb-4",
                                        style=button_style,
                                        n_clicks=0
                                    )
                                ],
                                style={
                                    "position": "relative",
                                    "width": "100%",
                                    "display": "flex",
                                    "justifyContent": "center"
                                }
                            )
                        ], width=8)
                    ], className="d-flex align-items-center justify-content-between mb-3")
                ], style={'padding': '15px', 'borderRadius': '15px', 'backgroundColor': 'rgba(0,0,0,0.03)'}),
                
                html.Div([
                    html.Div([
                        html.Div([
                            get_icon("mdi:thumb-up", 18, colors['success'], with_animation=True),
                            html.Span(translations.get("Prêt à donner?", "Prêt à donner?"), style={
                                'fontWeight': 'bold',
                                'fontSize': '14px',
                                'color': colors['success'],
                                'marginLeft': '8px'
                            })
                        ], style={
                            'display': 'flex',
                            'alignItems': 'center',
                            'marginBottom': '8px'
                        }),
                        html.A(
                            [
                                get_icon("mdi:api", 16, colors['secondary']),
                                html.Span(translations["Visiter la documentation de l API"], style={'marginLeft': '5px'})
                            ],
                            href="https://api-blood-donnation.onrender.com/docs#/",
                            target="_blank",
                            style={
                                'textDecoration': 'none',
                                'color': colors['secondary'],
                                'fontWeight': '500',
                                'display': 'inline-flex',
                                'alignItems': 'center',
                                'transition': 'all 0.2s ease',
                                'padding': '8px 15px',
                                'borderRadius': '6px',
                                'border': f'1px solid {colors["secondary"]}',
                                'backgroundColor': 'rgba(52, 152, 219, 0.05)',
                                'margin': '10px 0'
                            }
                        )
                    ], style={
                        'textAlign': 'center'
                    })
                ], style=footer_style)
                
            ], md=6)
        ]),
        
        # Résultats de la prédiction avec élégance et animations
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        get_icon("mdi:chart-bell-curve-cumulative", 24, "white", with_animation=True),
                        html.H3(translations["Résultats de la Prédiction"], style=section_title_style)
                    ])
                ], style={
                    **card_header_style,
                    'background': gradients['success']  # On utilise le dégradé vert qui convient au résultat
                }),
                
                html.Div([
                    # Animation subtile de présentation
                    #html.Div(blood_decorations, className="fade-in"),
                    
                    # Conteneur du statut avec animation et bel aspect visuel
                    html.Div(
                        id="prediction-status-container"
                    ),
                    
                    # Conteneur en flex pour afficher côte à côte les jauges avec animation
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                #html.H5(translations["Probabilité par catégorie"], className="text-center mb-4"),
                                html.Div(id="probability-gauges", style={
                                    'display': 'flex',
                                    'justifyContent': 'space-between',
                                })
                            ], width=11)
                        ]),
                    ], id="probability-container", style={'display': 'none', 'marginTop': '10px'}),
                    
                    # Bouton pour afficher les détails avec effet hover
                    html.Div([
                        dbc.Button(
                            [
                                get_icon("mdi:information-outline", 16, "white"),
                                translations["Voir les détails"]
                            ],
                            id="toggle-details-btn",
                            color="info",
                            size="sm",
                            className="mt-3 hover-scale",
                            style={
                                'margin': '0 auto',
                                'display': 'flex',
                                'alignItems': 'center',
                                'gap': '5px',
                                'borderRadius': '20px',
                                'boxShadow': '0 3px 6px rgba(0, 0, 0, 0.1)',
                                'padding': '8px 16px',
                                'transition': 'all 0.3s ease',
                                'backgroundColor': colors['info'],
                                'border': 'none'
                            }
                        )
                    ], id="details-button-container", style={'textAlign': 'center', 'marginTop': '25px', 'display': 'none'}),
                    
                    # Container pour les raisons et recommandations avec amélioration
                    create_reasons_recommendations_display()
                ], style={
                    **card_body_style,
                    'padding': '25px 25px'
                })
            ], style={
                **card_style,
                'margin': '30px 0',
                'padding':'70px',
                'transform': 'translateY(0)',
                'transition': 'transform 0.5s ease, box-shadow 0.5s ease'
            }, id="results-card", className="mt-4 shadow-lg hover-scale")
        ], className="mt-4"),
        
        # Stockage de l'état de la prédiction
        dcc.Store(id="prediction-result"),
        dcc.Store(id="show-details", data=False)
        #blood_decorations
    ])
    
    # Callback pour afficher/masquer la section femmes en fonction du genre
@app.callback(
    Output("section-femmes", "style"),
    Input("genre", "value")
)
def toggle_women_section(genre):
    """Affiche la section femmes uniquement si le genre sélectionné est 'Femme'"""
    if genre == "Femme":
        return {"display": "block", "marginBottom": "20px", "animation": "fadeIn 0.5s"}
    return {"display": "none"}

# Callback pour afficher/masquer la section date du dernier don
@app.callback(
    Output("date_dernier_don_container", "style"),
    Input("a_deja_donne", "value")
)
def toggle_last_donation_date(a_deja_donne):
    """Affiche la section date du dernier don uniquement si l'utilisateur a déjà donné son sang"""
    if a_deja_donne == "Oui":
        return {"display": "block", "animation": "fadeIn 0.5s"}
    return {"display": "none"}

# Callback pour calculer et afficher l'IMC
@app.callback(
    Output("bmi-display", "children"),
    [Input("taille", "value"),
     Input("poids", "value"),
     Input("language-store", "data")]
)
def update_bmi_display(height, weight, language):
    """Calcule et affiche l'IMC en fonction de la taille et du poids"""
    translations = TRANSLATIONS[language]
    
    if not height or not weight or height <= 0 or weight <= 0:
        return html.Div([
            html.Span("--", style={
                'fontSize': '24px',
                'fontWeight': 'bold',
                'color': '#bbb'
            }),
            html.Div("", style={'fontSize': '14px', 'color': '#bbb', 'marginTop': '5px'})
        ])
    
    bmi = calculate_bmi(height, weight)
    category, color = get_bmi_category(bmi)
    
    return html.Div([
        html.Span(f"{bmi}", style={
            'fontSize': '24px',
            'fontWeight': 'bold',
            'color': color
        }),
        html.Div(category, style={'fontSize': '14px', 'color': color, 'marginTop': '5px'})
    ])

# Callback pour mettre à jour l'affichage de la valeur du taux d'hémoglobine
@app.callback(
    Output("hemoglobin-value-display", "children"),
    Input("taux_hemoglobine", "value")
)
def update_hemoglobin_display(value):
    """Affiche la valeur actuelle du taux d'hémoglobine"""
    color = "#e74c3c" if value < 12 else "#2ecc71"  # Rouge si inférieur à 12, vert sinon
    return f"{value} g/dL"

# Callback pour réinitialiser le formulaire
@app.callback(
    [Output("genre", "value"),
     Output("age", "value"),
     Output("niveau_etude", "value"),
     Output("situation_matrimoniale", "value"),
     Output("religion", "value"),
     Output("profession", "value"),
     Output("taille", "value"),
     Output("poids", "value"),
     Output("arrondissement_de_residence", "value"),
     Output("quartier_residence", "value"),
     Output("nationalite", "value"),
     Output("taux_hemoglobine", "value"),
     Output("a_deja_donne", "value"),
     Output("anti_biotherapie", "value"),
     Output("ist_recente", "value"),
     Output("ddr_recent", "value"),
     Output("allaitement", "value"),
     Output("accouchement_recent", "value"),
     Output("interruption_grossesse", "value"),
     Output("enceinte", "value"),
     Output("autre_raison_indispo_femme", "value"),
     Output("antecedent_transfusion", "value"),
     Output("porteur_hiv", "value"),
     Output("opere_recemment", "value"),
     Output("drepanocytaire", "value"),
     Output("diabetique", "value"),
     Output("hypertendu", "value"),
     Output("asthmatique", "value"),
     Output("cardiaque", "value"),
     Output("tatoue", "value"),
     Output("scarifie", "value"),
     Output("autre_raison_ineligible", "value")],
    Input("reset-button", "n_clicks"),
    prevent_initial_call=True
)
def reset_form(n_clicks):
    """Réinitialise tous les champs du formulaire à leurs valeurs par défaut"""
    if n_clicks:
        return ("Homme", 30, "Secondaire", "Célibataire", "chrétien (catholique)", 
                "Étudiant-Eleve", 170, 70, "douala 3", "Makepe", "Camerounaise", 
                13.5, "Non", "non", "non", "non", "non", "non", "non", "non", "", 
                "non", "non", "non", "non", "non", "non", "non", "non", "non", "non", "")
    return dash.no_update

# Callback pour effectuer la prédiction et afficher les résultats
@app.callback(
    [Output("prediction-result", "data"),
     Output("results-card", "style"),
     Output("prediction-status-container", "children"),
     Output("probability-container", "style"),
     Output("probability-gauges", "children"),
     Output("details-button-container", "style"),
     Output("reasons-container", "children"),
     Output("recommendations-container", "children")],
    Input("predict-button", "n_clicks"),
    [State("genre", "value"),
     State("age", "value"),
     State("niveau_etude", "value"),
     State("situation_matrimoniale", "value"),
     State("religion", "value"),
     State("profession", "value"),
     State("taille", "value"),
     State("poids", "value"),
     State("arrondissement_de_residence", "value"),
     State("quartier_residence", "value"),
     State("nationalite", "value"),
     State("taux_hemoglobine", "value"),
     State("a_deja_donne", "value"),
     State("mois_dernier_don", "value"),
     State("annee_dernier_don", "value"),
     State("anti_biotherapie", "value"),
     State("ist_recente", "value"),
     State("ddr_recent", "value"),
     State("allaitement", "value"),
     State("accouchement_recent", "value"),
     State("interruption_grossesse", "value"),
     State("enceinte", "value"),
     State("autre_raison_indispo_femme", "value"),
     State("antecedent_transfusion", "value"),
     State("porteur_hiv", "value"),
     State("opere_recemment", "value"),
     State("drepanocytaire", "value"),
     State("diabetique", "value"),
     State("hypertendu", "value"),
     State("asthmatique", "value"),
     State("cardiaque", "value"),
     State("tatoue", "value"),
     State("scarifie", "value"),
     State("autre_raison_ineligible", "value"),
     State("theme-store", "data"),
     State("language-store", "data")],
    prevent_initial_call=True
)
def predict_eligibility(n_clicks, genre, age, niveau_etude, situation_matrimoniale, religion, 
                        profession, taille, poids, arrondissement, quartier, nationalite, 
                        taux_hemoglobine, a_deja_donne, mois_dernier_don, annee_dernier_don, 
                        anti_biotherapie, ist_recente, ddr_recent, allaitement, 
                        accouchement_recent, interruption_grossesse, enceinte, 
                        autre_raison_indispo_femme, antecedent_transfusion, porteur_hiv, 
                        opere_recemment, drepanocytaire, diabetique, hypertendu, 
                        asthmatique, cardiaque, tatoue, scarifie, autre_raison_ineligible,
                        theme, language):
    """
    Effectue la prédiction d'éligibilité au don de sang en envoyant les données à l'API,
    puis formate et affiche les résultats obtenus.
    """
    if not n_clicks:
        # Valeurs par défaut
        default_style = {
            'display': 'none'
        }
        empty_children = []
        return None, default_style, empty_children, default_style, empty_children, default_style, empty_children, empty_children
    
    # Récupérer les traductions et couleurs du thème
    translations = TRANSLATIONS[language]
    is_dark = theme == 'dark'
    
    # Couleurs des graphiques selon le thème
    if is_dark:
        card_style = {
            'backgroundColor': '#0A3160',
            'color': 'white',
            'borderRadius': '16px',
            'boxShadow': '0 10px 25px rgba(0, 0, 0, 0.3)',
            'border': '1px solid rgba(255,255,255,0.1)',
            'padding': '0',
            'marginBottom': '30px',
            'overflow': 'hidden',
            'transition': 'all 0.3s ease',
            'position': 'relative',
            'transform': 'translateZ(0)'
        }
        gauge_text_color = 'white'
    else:
        card_style = {
            'backgroundColor': 'white',
            'borderRadius': '16px',
            'boxShadow': '0 10px 25px rgba(0, 0, 0, 0.15)',
            'border': '1px solid #e2e8f0',
            'padding': '0',
            'marginBottom': '30px',
            'color': '#333',
            'overflow': 'hidden',
            'transition': 'all 0.3s ease',
            'position': 'relative',
            'transform': 'translateZ(0)'
        }
        gauge_text_color = 'black'
    
    try:
        # Préparer la date du dernier don au format MM/YYYY si applicable
        date_dernier_don = None
        if a_deja_donne == "Oui" and mois_dernier_don and annee_dernier_don:
            date_dernier_don = f"{mois_dernier_don:02d}/{annee_dernier_don}"
        
        # Construire le payload pour l'API avec tous les champs du formulaire
        payload = {
            "Genre": genre,
            "Age": age,
            "Niveau_etude": niveau_etude,
            "Situation_Matrimoniale": situation_matrimoniale,
            "Religion": religion,
            "Profession": profession,
            "Taille": float(taille),
            "Poids": float(poids),
            "Arrondissement_de_residence": arrondissement,
            "Quartier_residence": quartier,
            "Nationalite": nationalite,
            "Taux_hemoglobine": float(taux_hemoglobine),
            "A_deja_donne": a_deja_donne,
            "Date_dernier_don": date_dernier_don,
            "Anti_biotherapie": anti_biotherapie,
            "Taux_hemoglobine_bas": "oui" if float(taux_hemoglobine) < 12.0 else "non",
            "IST_recente": ist_recente,
            "DDR_recent": ddr_recent if genre == "Femme" else None,
            "Allaitement": allaitement if genre == "Femme" else None,
            "Accouchement_recent": accouchement_recent if genre == "Femme" else None,
            "Interruption_grossesse_recente": interruption_grossesse if genre == "Femme" else None,
            "Enceinte": enceinte if genre == "Femme" else None,
            "Autre_raison_indispo_femme": autre_raison_indispo_femme if genre == "Femme" and autre_raison_indispo_femme else None,
            "Antecedent_transfusion": antecedent_transfusion,
            "Porteur_HIV_Hbs_Hcv": porteur_hiv,
            "Opere": opere_recemment,
            "Drepanocytaire": drepanocytaire,
            "Diabetique": diabetique,
            "Hypertendu": hypertendu,
            "Asthmatique": asthmatique,
            "Cardiaque": cardiaque,
            "Tatoue": tatoue,
            "Scarifie": scarifie,
            "Autre_raison_ineligible": autre_raison_ineligible if autre_raison_ineligible else None
        }
        
        # Appel à l'API pour obtenir la prédiction
        response = requests.post("https://api-blood-donnation.onrender.com/predict", json=payload)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Récupérer les données de la réponse
            api_response = response.json()
            
            # Extraire les données pertinentes de la réponse
            eligibility_class = api_response.get("statut", "")
            proba = api_response.get("probabilites", {})
            eligibility_factors = api_response.get("raisons", [])
            recommandations = api_response.get("recommandations", [])
            
            # Création des jauges pour chaque probabilité
            gauge_colors = {
                "Eligible": "#2ecc71",  # Vert
                "Temporairement Non-eligible": "#f39c12",  # Orange
                "Définitivement non-eligible": "#e74c3c"  # Rouge
            }
            
            gauge_translations = {
                "Eligible": translations.get("Eligible", "Eligible"),
                "Temporairement Non-eligible": translations.get("Temporairement Non-eligible", "Temporairement Non-eligible"),
                "Définitivement non-eligible": translations.get("Définitivement non-eligible", "Définitivement non-eligible")
            }
            
            gauges = []
            for status, probability in proba.items():
                fig = create_probability_gauge(
                    probability=probability,
                    title=gauge_translations.get(status, status),
                    color=gauge_colors[status],
                    plot_font_color=gauge_text_color,
                    animated=True
                )
                
                gauges.append(
                    dbc.Col(
                        dcc.Graph(
                            figure=fig,
                            config={'displayModeBar': False},
                            className="gauge-graph",
                            style={'height': '220px', 'width': '100%'}
                        ),
                        width=4,
                        className="gauge-col"
                    )
                )
            
            # Création du conteneur de statut
            status_display = None
            
            if eligibility_class == "Eligible":
                status_display = create_eligibility_status_container(
                    status=translations.get("Éligible au don de sang", "Éligible au don de sang"),
                    color_gradient="linear-gradient(135deg, #2ecc71, #27ae60)",
                    icon_name="mdi:check-circle",
                    animate=True
                )
            elif eligibility_class == "Temporairement Non-eligible":
                status_display = create_eligibility_status_container(
                    status=translations.get("Temporairement non éligible", "Temporairement non éligible"),
                    color_gradient="linear-gradient(135deg, #f39c12, #e67e22)",
                    icon_name="mdi:clock-time-four",
                    animate=True
                )
            else:
                status_display = create_eligibility_status_container(
                    status=translations.get("Définitivement non éligible", "Définitivement non éligible"),
                    color_gradient="linear-gradient(135deg, #e74c3c, #c0392b)",
                    icon_name="mdi:close-circle",
                    animate=True
                )
            
            # Mise à jour des conteneurs de raisons et de recommandations
            reasons_container = []
            if api_response.get("raisons"):
                for reason in api_response["raisons"]:
                    reasons_container.append(
                        html.Div([
                            get_icon("mdi:alert-circle", 16, "#f39c12"),
                            html.Span(reason, style={'marginLeft': '10px'})
                        ], style={
                            'padding': '8px 12px',
                            'marginBottom': '8px',
                            'backgroundColor': 'rgba(243, 156, 18, 0.1)',
                            'borderRadius': '8px',
                            'display': 'flex',
                            'alignItems': 'center'
                        })
                    )
            else:
                reasons_container.append(
                    html.Div([
                        get_icon("mdi:information-outline", 16, "#bbb"),
                        html.Span(translations.get("Aucune raison identifiée", "Aucune raison identifiée"), 
                                style={'marginLeft': '10px', 'color': '#bbb'})
                    ], style={
                        'padding': '8px 12px',
                        'backgroundColor': 'rgba(0, 0, 0, 0.05)',
                        'borderRadius': '8px',
                        'display': 'flex',
                        'alignItems': 'center'
                    })
                )
            
            recommendations_container = []
            if api_response.get("recommandations"):
                for recommendation in api_response["recommandations"]:
                    recommendations_container.append(
                        html.Div([
                            get_icon("mdi:lightbulb-on", 16, "#1abc9c"),
                            html.Span(recommendation, style={'marginLeft': '10px'})
                        ], style={
                            'padding': '8px 12px',
                            'marginBottom': '8px',
                            'backgroundColor': 'rgba(26, 188, 156, 0.1)',
                            'borderRadius': '8px',
                            'display': 'flex',
                            'alignItems': 'center'
                        })
                    )
            else:
                recommendations_container.append(
                    html.Div([
                        get_icon("mdi:information-outline", 16, "#bbb"),
                        html.Span(translations.get("Aucune recommandation disponible", "Aucune recommandation disponible"), 
                                style={'marginLeft': '10px', 'color': '#bbb'})
                    ], style={
                        'padding': '8px 12px',
                        'backgroundColor': 'rgba(0, 0, 0, 0.05)',
                        'borderRadius': '8px',
                        'display': 'flex',
                        'alignItems': 'center'
                    })
                )
            
            # Retourner tous les éléments mis à jour pour l'affichage des résultats
            return (
                api_response,  # Résultat de la prédiction dans le store
                card_style,  # Style de la carte de résultats
                status_display,  # Affichage du statut d'éligibilité
                {'display': 'block'},  # Visibilité du conteneur de probabilités
                gauges,  # Jauges des probabilités
                {'display': 'block', 'textAlign': 'center', 'marginTop': '25px'},  # Visibilité du bouton de détails
                reasons_container,  # Conteneur des raisons
                recommendations_container  # Conteneur des recommandations
            )
        else:
            # Gestion d'erreur pour les réponses non-200 de l'API
            error_message = f"Erreur de l'API (code {response.status_code}): {response.text}"
            
            error_container = html.Div([
                html.Div([
                    get_icon("mdi:alert-circle", 48, "#e74c3c", with_animation=True),
                    html.H3(translations.get("Erreur lors de la prédiction", "Erreur lors de la prédiction"), 
                          style={"color": "#e74c3c", "marginBottom": "10px"})
                ], style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'marginBottom': '15px'
                }),
                html.P(error_message, style={'textAlign': 'center', 'color': '#666'})
            ])
            
            return (
                None,  # Pas de résultat de prédiction
                card_style,  # Style de carte par défaut
                error_container,  # Message d'erreur
                {'display': 'none'},  # Cacher les probabilités
                [],  # Pas de jauges
                {'display': 'none'},  # Cacher le bouton de détails
                [],  # Pas de raisons
                []  # Pas de recommandations
            )
        
    except Exception as e:
        # Gestion d'erreur avec un message utilisateur convivial
        error_container = html.Div([
            html.Div([
                get_icon("mdi:alert-circle", 48, "#e74c3c", with_animation=True),
                html.H3(translations.get("Erreur lors de la prédiction", "Erreur lors de la prédiction"), 
                       style={"color": "#e74c3c", "marginBottom": "10px"})
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'marginBottom': '15px'
            }),
            html.P(str(e), style={'textAlign': 'center', 'color': '#666'})
        ])
        
        return (
            None,  # Pas de résultat de prédiction
            card_style,  # Style de carte par défaut
            error_container,  # Message d'erreur
            {'display': 'none'},  # Cacher les probabilités
            [],  # Pas de jauges
            {'display': 'none'},  # Cacher le bouton de détails
            [],  # Pas de raisons
            []  # Pas de recommandations
        )
# Callback pour afficher/cacher les détails des résultats
@app.callback(
    [Output("details-container", "style"),
     Output("toggle-details-btn", "children"),
     Output("show-details", "data")],
    [Input("toggle-details-btn", "n_clicks")],
    [State("show-details", "data"),
     State("language-store", "data")]
)
def toggle_details(n_clicks, show_details, language):
    """Affiche ou masque les détails des résultats de prédiction"""
    translations = TRANSLATIONS[language]
    
    if not n_clicks:
        return {'display': 'none'}, [
            get_icon("mdi:information-outline", 16, "white"),
            translations.get("Voir les détails", "Voir les détails")
        ], show_details
    
    if show_details:
        # Si les détails sont déjà affichés, les cacher
        return {'display': 'none'}, [
            get_icon("mdi:information-outline", 16, "white"),
            translations.get("Voir les détails", "Voir les détails")
        ], False
    else:
        # Si les détails sont cachés, les afficher
        return {'display': 'block'}, [
            get_icon("mdi:eye-off", 16, "white"),
            translations.get("Cacher les détails", "Cacher les détails")
        ], True
    
    
