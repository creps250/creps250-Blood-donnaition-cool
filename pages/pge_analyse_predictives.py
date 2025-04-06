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


TRANSLATIONS = {
    'fr': {
        # Page Title and Headers
        "Prédiction d'Éligibilité au Don de Sang": "Prédiction d'Éligibilité au Don de Sang",
        "Données Démographiques": "Données Démographiques",
        "Données Médicales": "Données Médicales",
        "Résultats de la Prédiction": "Résultats de la Prédiction",
        "Conseils et Recommandations": "Conseils et Recommandations",
        
        # Prediction Status
        "Eligible": "Eligible",
        "Temporairement Non-eligible": "Temporairement Non-eligible",
        "Définitivement non-eligible": "Définitivement non-eligible",
        
        # Statut messages
        "Éligible au don de sang": "Éligible au don de sang",
        "Temporairement non éligible": "Temporairement non éligible",
        "Définitivement non éligible": "Définitivement non éligible",
        
        # Demographics Section
        "Genre": "Genre",
        "Homme": "Homme",
        "Femme": "Femme",
        "Âge": "Âge",
        "Niveau d'études": "Niveau d'études",
        "Primaire": "Primaire",
        "Secondaire": "Secondaire",
        "Universitaire": "Universitaire",
        "Pas Précisé": "Pas Précisé",
        "Aucun": "Aucun",
        "Situation Matrimoniale": "Situation Matrimoniale",
        "Célibataire": "Célibataire",
        "Marié (e)": "Marié (e)",
        "Divorcé(e)": "Divorcé(e)",
        "veuf (veuve)": "veuf (veuve)",
        "Religion": "Religion",
        "Chrétien (Catholique)": "Chrétien (Catholique)",
        "Chrétien (Protestant)": "Chrétien (Protestant)",
        "Musulman": "Musulman",
        "Profession": "Profession",
        "Agent de sécurité": "Agent de sécurité",
        "Agent immobilier": "Agent immobilier",
        "Assistant administratif": "Assistant administratif",
        "Commerçant": "Commerçant",
        "Conducteur": "Conducteur",
        "Électricien": "Électricien",
        "Enseignant": "Enseignant",
        "Étudiant-Eleve": "Étudiant-Eleve",
        "Informaticien": "Informaticien",
        "Infirmier": "Infirmier",
        "Ingénieur": "Ingénieur",
        "Personnel de santé": "Personnel de santé",
        "Sans emploi": "Sans emploi",
        "Technicien": "Technicien",
        "Autres": "Autres",
        "Nationalité": "Nationalité",
        "Camerounaise": "Camerounaise",
        "Etranger": "Etranger",
        "Taille (cm)": "Taille (cm)",
        "Poids (kg)": "Poids (kg)",
        "Arrondissement de résidence": "Arrondissement de résidence",
        "Douala 1": "Douala 1",
        "Douala 2": "Douala 2",
        "Douala 3": "Douala 3",
        "Douala 4": "Douala 4",
        "Douala 5": "Douala 5",
        "Yaoundé": "Yaoundé",
        "Quartier de résidence": "Quartier de résidence",
        
        # Medical Data Section
        "Taux d'hémoglobine (g/dL)": "Taux d'hémoglobine (g/dL)",
        "A déjà donné le sang": "A déjà donné le sang",
        "Oui": "Oui",
        "Non": "Non",
        "oui": "oui",
        "non": "non",
        "Date du dernier don": "Date du dernier don",
        "Mois": "Mois",
        "Janvier": "Janvier",
        "Février": "Février",
        "Mars": "Mars",
        "Avril": "Avril",
        "Mai": "Mai",
        "Juin": "Juin",
        "Juillet": "Juillet",
        "Août": "Août",
        "Septembre": "Septembre",
        "Octobre": "Octobre",
        "Novembre": "Novembre",
        "Décembre": "Décembre",
        "Année": "Année",
        
        # New Medical Fields
        "Est sous anti-biothérapie": "Est sous anti-biothérapie",
        "Taux d'hémoglobine bas": "Taux d'hémoglobine bas",
        "IST récente": "IST récente (Exclu VIH, Hbs, Hcv)",
        "DDR <14 jours avant le don": "La DDR est mauvaise si <14 jours avant le don",
        "Allaitement": "Allaitement",
        "Accouchement récent": "A accouché ces 6 derniers mois",
        "Interruption de grossesse récente": "Interruption de grossesse ces 06 derniers mois",
        "Enceinte": "Est enceinte",
        "Antécédent de transfusion": "Antécédent de transfusion",
        "Porteur (HIV, Hbs, Hcv)": "Porteur (HIV, Hbs, Hcv)",
        "Opéré récemment": "Opéré",
        "Drépanocytaire": "Drépanocytaire",
        "Diabétique": "Diabétique",
        "Hypertendu": "Hypertendu",
        "Asthmatique": "Asthmatique",
        "Cardiaque": "Cardiaque",
        "Tatoué": "Tatoué",
        "Scarifié": "Scarifié",
        "Autre raison d'indisponibilité (femme)": "Autre raison d'indisponibilité (femme)",
        "Autre raison d'inéligibilité": "Autre raison d'inéligibilité",
        
        # Prediction Section
        "Probabilité d'éligibilité": "Probabilité d'éligibilité",
        "Vous êtes éligible pour donner votre sang. Merci pour votre générosité !": "Vous êtes éligible pour donner votre sang. Merci pour votre générosité !",
        "Désolé, vous n'êtes pas éligible pour le don de sang à ce moment.": "Désolé, vous n'êtes pas éligible pour le don de sang à ce moment.",
        "Erreur lors de la prédiction": "Erreur lors de la prédiction",
        "Voir les détails": "Voir les détails",
        "Probabilité par catégorie": "Probabilité par catégorie",
        
        # Buttons and Actions
        "Prédire l'éligibilité": "Prédire l'éligibilité",
        "Visiter la documentation de l API": "Visiter la documentation de l'API",
        
        # Recommendations
        "Améliorez votre taux d'hémoglobine en consommant des aliments riches en fer comme la viande rouge, les épinards et les lentilles.": "Améliorez votre taux d'hémoglobine en consommant des aliments riches en fer comme la viande rouge, les épinards et les lentilles.",
        "Vous devez attendre au moins 3 mois entre deux dons. Réessayez plus tard.": "Vous devez attendre au moins 3 mois entre deux dons. Réessayez plus tard.",
        "Un poids minimum de 50 kg est généralement recommandé pour le don de sang.": "Un poids minimum de 50 kg est généralement recommandé pour le don de sang.",
        "Hydratez-vous bien avant votre don.": "Hydratez-vous bien avant votre don.",
        "Prenez un repas équilibré dans les heures précédant votre don.": "Prenez un repas équilibré dans les heures précédant votre don.",
        
        # Conditions médicales
        "Section Femmes": "Section Femmes",
        "Antécédents et Conditions Médicales": "Antécédents et Conditions Médicales",
        
        # New content
        "Remplissez le formulaire et cliquez sur le bouton pour prédire votre éligibilité": "Remplissez le formulaire et cliquez sur le bouton pour prédire votre éligibilité",
        "Données de santé": "Données de santé",
        "Raisons": "Raisons",
        "Recommandations": "Recommandations"
    },
    'en': {
        # Page Title and Headers
        "Prédiction d'Éligibilité au Don de Sang": "Blood Donation Eligibility Prediction",
        "Données Démographiques": "Demographic Data",
        "Données Médicales": "Medical Data",
        "Résultats de la Prédiction": "Prediction Results",
        "Conseils et Recommandations": "Advice and Recommendations",
        
        # Prediction Status
        "Eligible": "Eligible",
        "Temporairement Non-eligible": "Temporarily Ineligible",
        "Définitivement non-eligible": "Permanently Ineligible",
        
        # Statut messages
        "Éligible au don de sang": "Eligible for blood donation",
        "Temporairement non éligible": "Temporarily ineligible",
        "Définitivement non éligible": "Permanently ineligible",
        
        # Demographics Section
        "Genre": "Gender",
        "Homme": "Male",
        "Femme": "Female",
        "Âge": "Age",
        "Niveau d'études": "Education Level",
        "Primaire": "Primary",
        "Secondaire": "Secondary",
        "Universitaire": "University",
        "Pas Précisé": "Not Specified",
        "Aucun": "None",
        "Situation Matrimoniale": "Marital Status",
        "Célibataire": "Single",
        "Marié (e)": "Married",
        "Divorcé(e)": "Divorced",
        "veuf (veuve)": "Widowed",
        "Religion": "Religion",
        "Chrétien (Catholique)": "Christian (Catholic)",
        "Chrétien (Protestant)": "Christian (Protestant)",
        "Musulman": "Muslim",
        "Profession": "Profession",
        "Agent de sécurité": "Security Guard",
        "Agent immobilier": "Real Estate Agent",
        "Assistant administratif": "Administrative Assistant",
        "Commerçant": "Merchant",
        "Conducteur": "Driver",
        "Électricien": "Electrician",
        "Enseignant": "Teacher",
        "Étudiant-Eleve": "Student",
        "Informaticien": "IT Professional",
        "Infirmier": "Nurse",
        "Ingénieur": "Engineer",
        "Personnel de santé": "Healthcare Professional",
        "Sans emploi": "Unemployed",
        "Technicien": "Technician",
        "Autres": "Others",
        "Nationalité": "Nationality",
        "Camerounaise": "Cameroonian",
        "Etranger": "Foreigner",
        "Taille (cm)": "Height (cm)",
        "Poids (kg)": "Weight (kg)",
        "Arrondissement de résidence": "District of Residence",
        "Douala 1": "Douala 1",
        "Douala 2": "Douala 2",
        "Douala 3": "Douala 3",
        "Douala 4": "Douala 4",
        "Douala 5": "Douala 5",
        "Yaoundé": "Yaoundé",
        "Quartier de résidence": "Neighborhood of Residence",
        
        # Medical Data Section
        "Taux d'hémoglobine (g/dL)": "Hemoglobin Level (g/dL)",
        "A déjà donné le sang": "Has Previously Donated Blood",
        "Oui": "Yes",
        "Non": "No",
        "oui": "yes",
        "non": "no",
        "Date du dernier don": "Date of Last Donation",
        "Mois": "Month",
        "Janvier": "January",
        "Février": "February",
        "Mars": "March",
        "Avril": "April",
        "Mai": "May",
        "Juin": "June",
        "Juillet": "July",
        "Août": "August",
        "Septembre": "September",
        "Octobre": "October",
        "Novembre": "November",
        "Décembre": "December",
        "Année": "Year",
        
        # New Medical Fields
        "Est sous anti-biothérapie": "Is under antibiotic therapy",
        "Taux d'hémoglobine bas": "Low hemoglobin level",
        "IST récente": "Recent STI (Excluding HIV, HBs, HCv)",
        "DDR <14 jours avant le don": "Last menstrual period <14 days before donation",
        "Allaitement": "Breastfeeding",
        "Accouchement récent": "Recent childbirth (last 6 months)",
        "Interruption de grossesse récente": "Recent pregnancy termination (last 6 months)",
        "Enceinte": "Is pregnant",
        "Antécédent de transfusion": "History of blood transfusion",
        "Porteur (HIV, Hbs, Hcv)": "Carrier (HIV, Hbs, Hcv)",
        "Opéré récemment": "Recent surgery",
        "Drépanocytaire": "Sickle cell disease",
        "Diabétique": "Diabetic",
        "Hypertendu": "Hypertensive",
        "Asthmatique": "Asthmatic",
        "Cardiaque": "Cardiac condition",
        "Tatoué": "Tattooed",
        "Scarifié": "Scarified",
        "Autre raison d'indisponibilité (femme)": "Other reason for unavailability (women)",
        "Autre raison d'inéligibilité": "Other reason for ineligibility",
        
        # Prediction Section
        "Probabilité d'éligibilité": "Eligibility Probability",
        "Vous êtes éligible pour donner votre sang. Merci pour votre générosité !": "You are eligible to donate blood. Thank you for your generosity!",
        "Désolé, vous n'êtes pas éligible pour le don de sang à ce moment.": "Sorry, you are not eligible for blood donation at this time.",
        "Erreur lors de la prédiction": "Error during prediction",
        "Voir les détails": "View details",
        "Probabilité par catégorie": "Probability by category",
        
        # Buttons and Actions
        "Prédire l'éligibilité": "Predict Eligibility",
        "Visiter la documentation de l API": "Visit API Documentation",
        
        # Recommendations
        "Améliorez votre taux d'hémoglobine en consommant des aliments riches en fer comme la viande rouge, les épinards et les lentilles.": "Improve your hemoglobin level by consuming iron-rich foods such as red meat, spinach, and lentils.",
        "Vous devez attendre au moins 3 mois entre deux dons. Réessayez plus tard.": "You must wait at least 3 months between two donations. Please try again later.",
        "Un poids minimum de 50 kg est généralement recommandé pour le don de sang.": "A minimum weight of 50 kg is generally recommended for blood donation.",
        "Hydratez-vous bien avant votre don.": "Stay well hydrated before your donation.",
        "Prenez un repas équilibré dans les heures précédant votre don.": "Have a balanced meal in the hours preceding your donation.",
        
        # Conditions médicales
        "Section Femmes": "Women's Section",
        "Antécédents et Conditions Médicales": "Medical History and Conditions",
        
        # New content
        "Remplissez le formulaire et cliquez sur le bouton pour prédire votre éligibilité": "Fill out the form and click the button to predict your eligibility",
        "Données de santé": "Health Data",
        "Raisons": "Reasons",
        "Recommandations": "Recommendations"
    }
}






def get_icon(name, size=20, color="#e74c3c"):
    """Helper function to create consistent icons"""
    return DashIconify(
        icon=name,
        width=size,
        height=size,
        color=color
    )

# Fonction pour créer un container pour chaque statut d'éligibilité
# Cette fonction est maintenant définie au niveau du module et non plus dans page_quatre
def create_eligibility_status_container(status, color_gradient, icon_name):
    """
    Crée un conteneur stylisé pour afficher le statut d'éligibilité.
    
    Args:
        status (str): Le texte du statut à afficher
        color_gradient (str): Le gradient de couleur CSS pour l'arrière-plan
        icon_name (str): Le nom de l'icône à afficher
    
    Returns:
        html.Div: Un div contenant l'affichage stylisé du statut
    """
    return html.Div([
        html.Div([
            html.Div([
                get_icon(icon_name, 48, "white"),
            ], style={'marginRight': '15px'}),
            html.H3(status, style={"color": "white", "marginBottom": "0px"})
        ], style={
            'display': 'flex', 
            'alignItems': 'center', 
            'justifyContent': 'center', 
            'marginBottom': '15px',
            'padding': '20px',
            'borderRadius': '10px',
            'background': color_gradient,
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ])

# Créer un indicateur de jauge amélioré pour l'éligibilité
def create_probability_gauge(probability, title, color, plot_font_color="black"):
    """
    Crée une jauge pour afficher la probabilité d'un statut d'éligibilité.
    
    Args:
        probability (float): La probabilité à afficher (entre 0 et 1)
        title (str): Le titre de la jauge
        color (str): La couleur de la jauge
        plot_font_color (str): La couleur du texte
    
    Returns:
        go.Figure: Une figure Plotly contenant la jauge de probabilité
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,  # Convertir en pourcentage
        title={
            'text': title, 
            'font': {'size': 18, 'color': plot_font_color, 'family': 'Arial, sans-serif'}
        },
        number={'suffix': '%', 'font': {'size': 24, 'color': plot_font_color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': plot_font_color, 'tickfont': {'color': plot_font_color, 'size': 14}},
            'bar': {'color': color},
            'bgcolor': "rgba(255, 255, 255, 0.1)" if probability < 30 else "rgba(240, 240, 240, 0.8)",
            'borderwidth': 2,
            'bordercolor': plot_font_color,
            'steps': [
                {'range': [0, 30], 'color': 'rgba(214, 39, 40, 0.15)'},
                {'range': [30, 70], 'color': 'rgba(255, 153, 51, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(50, 168, 82, 0.15)'},
            ],
            'threshold': {
                'line': {'color': plot_font_color, 'width': 4},
                'thickness': 0.8,
                'value': probability * 100
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': plot_font_color, 'family': 'Arial, sans-serif'},
        margin=dict(l=30, r=30, b=30, t=50),
        height=200
    )
    
    return fig

# Créer une fonction pour afficher les raisons et recommandations
def create_reasons_recommendations_display():
    """
    Crée une disposition pour afficher les raisons et recommandations.
    
    Returns:
        html.Div: Un div contenant la disposition pour les raisons et recommandations
    """
    return html.Div([
        html.Div([
            # Container pour les raisons
            html.Div([
                html.H4([
                    get_icon("mdi:alert-circle-outline", 24, "#f39c12"),
                    html.Span("Raisons", style={'marginLeft': '10px'})
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'color': '#f39c12',
                    'borderBottom': '1px solid rgba(243, 156, 18, 0.3)',
                    'paddingBottom': '10px',
                    'marginBottom': '15px'
                }),
                html.Div(id="reasons-container", style={
                    'maxHeight': '200px',
                    'overflowY': 'auto',
                    'padding': '10px',
                    'backgroundColor': 'rgba(255, 243, 224, 0.3)',
                    'borderRadius': '8px',
                    'border': '1px solid rgba(243, 156, 18, 0.3)'
                })
            ], style={'flex': '1', 'marginRight': '15px'}),
            
            # Container pour les recommandations
            html.Div([
                html.H4([
                    get_icon("mdi:lightbulb-on", 24, "#1abc9c"),
                    html.Span("Recommandations", style={'marginLeft': '10px'})
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'color': '#1abc9c',
                    'borderBottom': '1px solid rgba(26, 188, 156, 0.3)',
                    'paddingBottom': '10px',
                    'marginBottom': '15px'
                }),
                html.Div(id="recommendations-container", style={
                    'maxHeight': '200px',
                    'overflowY': 'auto',
                    'padding': '10px',
                    'backgroundColor': 'rgba(224, 255, 251, 0.3)',
                    'borderRadius': '8px',
                    'border': '1px solid rgba(26, 188, 156, 0.3)'
                })
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'marginTop': '20px', 'marginBottom': '20px'})
    ], id="details-container", style={'display': 'none'})

def page_quatre(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme, language="fr"):
    # Thèmes et styles améliorés
    translations = TRANSLATIONS[language]
    is_dark = theme == 'dark'
    
    
    # Palette de couleurs
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
    }
    
    footer_style = {
            'marginTop': '30px',
            'textAlign': 'center',
            'paddingTop': '20px',
            'borderTop': f'1px solid {colors["border"]}',
            'color': 'rgba(255,255,255,0.7)' if is_dark else 'rgba(0,0,0,0.5)',
        }
    
    # Fonds avec dégradés
    gradients = {
        'primary': 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
        'secondary': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
        'success': 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)',
        'warning': 'linear-gradient(135deg, #f39c12, #e67e22 100%)',
        'danger': 'linear-gradient(135deg, #c0392b, #922b21 100%)',
        'card': 'linear-gradient(135deg, #2c3e50, #1a252f)' if is_dark else 'white',
        'section_header': 'linear-gradient(135deg, #c0392b, #e74c3c)' if is_dark else 'linear-gradient(135deg, #e74c3c, #e67e22)',
        'eligible': 'linear-gradient(135deg, #2ecc71, #27ae60)',
        'temp_ineligible': 'linear-gradient(135deg, #f39c12, #e67e22)',
        'def_ineligible': 'linear-gradient(135deg, #e74c3c, #c0392b)',
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
    }
    
    card_header_style = {
        'background': gradients['section_header'],
        'color': 'white',
        'padding': '15px 20px',
        'fontWeight': 'bold',
        'borderTopLeftRadius': '15px',
        'borderTopRightRadius': '15px',
        'display': 'flex',
        'alignItems': 'center',
        'borderBottom': '0'
    }
    
    card_body_style = {
        'padding': '25px 20px',
        'backgroundColor': colors['background'],  
        'color': colors['text'], 
        'borderBottomLeftRadius': '15px',
        'borderBottomRightRadius': '15px'
    }
    
    section_title_style = {
        'color': 'white',
        'marginBottom': '0',
        'fontWeight': 'bold',
        'fontSize': '1.25rem',
        'display': 'flex',
        'alignItems': 'center'
    }
    
    label_style = {
        'fontWeight': '600', 
        'marginBottom': '10px',
        'color': light_theme['textColor'] if theme == 'light' else 'rgba(255, 255, 255, 0.9)',
        'fontSize': '0.95rem',
        'display': 'flex',
        'alignItems': 'center',
        'gap': '8px'
    }
    
    input_style = {
        'width': '100%', 
        'padding': '12px', 
        'borderRadius': '10px', 
        'border': f'1px solid {colors["border"]}',
        'backgroundColor': 'rgba(0,0,0,0.05)' if theme == 'dark' else 'white',
        'color': colors['text'],
        'boxShadow': 'inset 0 2px 4px rgba(0,0,0,0.05)',
        'transition': 'all 0.3s ease',
    }
    
    dropdown_style = {
        'borderRadius': '10px',
        'border': f'1px solid {colors["border"]}',
        'color': colors['text'] if theme == 'light' else "black",
        'backgroundColor': 'rgba(0,0,0,0.05)' if theme == 'dark' else 'white',
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
        'boxShadow': '0 4px 15px rgba(231, 76, 60, 0.4)',
        'width': '100%',
        'marginTop': '30px',
        'textTransform': 'uppercase',
        'letterSpacing': '1px'
    }
    
    # Interface utilisateur principale
    return html.Div([
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
                                    translations["Genre"]
                                ], style=label_style),
                                dcc.Dropdown(
                                    id="genre",
                                    options=[
                                        {"label": translations["Homme"], "value": "Homme"},
                                        {"label": translations["Femme"], "value": "Femme"}
                                    ],
                                    value="Homme",
                                    style=dropdown_style,
                                    className="mb-3"
                                )
                            ], width=6),
                            
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:cake-variant", 18),
                                    translations["Âge"]
                                ], style=label_style),
                                dcc.Input(
                                    id="age",
                                    type="number",
                                    placeholder="Âge",
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
                                    translations["Taille (cm)"]
                                ], style=label_style),
                                dcc.Input(
                                    id="taille",
                                    type="number",
                                    placeholder="Taille en cm",
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
                                    translations["Poids (kg)"]
                                ], style=label_style),
                                dcc.Input(
                                    id="poids",
                                    type="number",
                                    placeholder="Poids en kg",
                                    min=45,
                                    max=150,
                                    value=70,
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=6)
                        ]),
                        
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
                                    placeholder="Quartier",
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
                        ])
                    ], style=card_body_style)
                ], style=card_style, className="mb-4"),
                
                # Données médicales générales
                html.Div([
                    html.Div([
                        html.Div([
                            get_icon("mdi:medical-bag", 24, "white"),
                            html.H3(translations["Données de santé"], style=section_title_style)
                        ])
                    ], style=card_header_style),
                    
                    html.Div([
                        # Taux d'hémoglobine avec slider amélioré
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    get_icon("mdi:water", 18),
                                    translations["Taux d'hémoglobine (g/dL)"]
                                ], style=label_style),
                                dcc.Slider(
                                    id="taux_hemoglobine",
                                    min=8,
                                    max=20,
                                    step=0.1,
                                    value=13.5,
                                    marks={i: f'{i}' for i in range(8, 21, 2)},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    className="mb-4",
                                )
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
                                    style={'display': 'flex', 'gap': '20px'},
                                    className="mb-3",
                                    labelStyle={
                                        'display': 'flex', 
                                        'alignItems': 'center', 
                                        'gap': '5px',
                                        'cursor': 'pointer',
                                        'padding': '8px',
                                        'borderRadius': '4px',
                                        'transition': 'background-color 0.2s',
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
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label(translations["Mois"], style={'fontSize': '0.85rem', 'marginBottom': '5px'}),
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
                                            html.Label(translations["Année"], style={'fontSize': '0.85rem', 'marginBottom': '5px'}),
                                            dcc.Dropdown(
                                                id="annee_dernier_don",
                                                options=[{"label": str(year), "value": year} for year in range(2020, 2026)],
                                                value=2024,
                                                style=dropdown_style,
                                            )
                                        ], width=6)
                                    ])
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
                                    style={'display': 'flex', 'gap': '20px'},
                                    className="mb-3",
                                    labelStyle={
                                        'display': 'flex', 
                                        'alignItems': 'center', 
                                        'gap': '5px',
                                        'cursor': 'pointer',
                                        'padding': '8px',
                                        'borderRadius': '4px',
                                        'transition': 'background-color 0.2s',
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
                                    style={'display': 'flex', 'gap': '20px'},
                                    className="mb-3",
                                    labelStyle={
                                        'display': 'flex', 
                                        'alignItems': 'center', 
                                        'gap': '5px',
                                        'cursor': 'pointer',
                                        'padding': '8px',
                                        'borderRadius': '4px',
                                        'transition': 'background-color 0.2s',
                                    }
                                )
                            ], width=6)
                        ]),
                    ], style=card_body_style)
                ], style=card_style),
            ], md=6),
            
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
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
                                        style={'display': 'flex', 'gap': '20px'},
                                        className="mb-3",
                                        labelStyle={
                                            'display': 'flex', 
                                            'alignItems': 'center', 
                                            'gap': '5px',
                                            'cursor': 'pointer',
                                            'padding': '8px',
                                            'borderRadius': '4px',
                                            'transition': 'background-color 0.2s',
                                        }
                                    )
                                ], className="mb-3"),
                            ], width=6)
                        ]),
                    ], style=card_body_style)
                ], style=card_style, className="mb-4"),
                
                # Section spécifique femmes
                html.Div(
                    html.Div([
                        html.Div([
                            html.Div([
                                get_icon("mdi:human-female", 24, "white"),
                                html.H3(translations["Section Femmes"], style=section_title_style)
                            ])
                        ], style=card_header_style),
                        
                        html.Div([
                            dbc.Row([
                                # Première colonne
                                dbc.Col([
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:calendar-today", 16),
                                            translations["DDR <14 jours avant le don"]
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="ddr_recent",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={'display': 'flex', 'gap': '20px'},
                                            className="mb-3",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '8px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                            }
                                        )
                                    ], className="mb-3"),
                                    
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
                                            style={'display': 'flex', 'gap': '20px'},
                                            className="mb-3",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '8px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                            }
                                        )
                                    ], className="mb-3"),
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
                                            style={'display': 'flex', 'gap': '20px'},
                                            className="mb-3",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '8px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                            }
                                        )
                                    ], className="mb-3"),
                                    
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
                                            style={'display': 'flex', 'gap': '20px'},
                                            className="mb-3",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '8px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                            }
                                        )
                                    ], className="mb-3"),
                                ], width=6)
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Label([
                                            get_icon("mdi:human-pregnant", 16),
                                            translations["Enceinte"]
                                        ], style=label_style),
                                        dcc.RadioItems(
                                            id="enceinte",
                                            options=[
                                                {"label": translations["oui"], "value": "oui"},
                                                {"label": translations["non"], "value": "non"}
                                            ],
                                            value="non",
                                            style={'display': 'flex', 'gap': '20px'},
                                            className="mb-3",
                                            labelStyle={
                                                'display': 'flex', 
                                                'alignItems': 'center', 
                                                'gap': '5px',
                                                'cursor': 'pointer',
                                                'padding': '8px',
                                                'borderRadius': '4px',
                                                'transition': 'background-color 0.2s',
                                            }
                                        )
                                    ], className="mb-3"),
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
                                        placeholder="Précisez si autre raison",
                                        style=input_style,
                                        className="mb-3"
                                    )
                                ], width=12)
                            ])
                        ], style=card_body_style)
                    ], style=card_style),
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
                                    placeholder="Précisez si autre raison d'inéligibilité",
                                    style=input_style,
                                    className="mb-3"
                                )
                            ], width=12)
                        ])
                    ], style=card_body_style)
                ], style=card_style, className="mb-4"),
                
                # Bouton de prédiction
                dcc.Loading(
                    id="loading-prediction",
                    type="circle",
                    children=[
                        dbc.Button(
                            [
                                get_icon("mdi:calculator-check", 20, "white"),
                                html.Span(translations["Prédire l'éligibilité"], style={'marginLeft': '8px'})
                            ],
                            id="predict-button",
                            className="mt-3 mb-4",
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
                ),
                html.Div([
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
                        }
                    )
                ], style=footer_style)
                
            ], md=6)
        ]),
        
        # Résultats de la prédiction
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        get_icon("mdi:chart-bell-curve-cumulative", 24, "white"),
                        html.H3(translations["Résultats de la Prédiction"], style=section_title_style)
                    ])
                ], style=card_header_style),
                
                html.Div([
                    html.Div(id="prediction-status-container"),
                    
                    # Conteneur en flex pour afficher côte à côte les jauges
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.H4(translations["Probabilité par catégorie"], className="text-center mb-4"),
                                html.Div(id="probability-gauges", style={
                                    'display': 'flex',
                                    'justifyContent': 'space-between',
                                })
                            ], width=12)
                        ]),
                    ], id="probability-container", style={'display': 'none', 'marginTop': '20px'}),
                    
                    # Bouton pour afficher les détails
                    html.Div([
                        dbc.Button(
                            [
                                get_icon("mdi:information-outline", 16, "white"),
                                translations["Voir les détails"]
                            ],
                            id="toggle-details-btn",
                            color="info",
                            size="sm",
                            className="mt-3",
                            style={
                                'margin': '0 auto',
                                'display': 'flex',
                                'alignItems': 'center',
                                'gap': '5px'
                            }
                        )
                    ], id="details-button-container", style={'textAlign': 'center', 'marginTop': '20px', 'display': 'none'}),
                    
                    # Container pour les raisons et recommandations
                    create_reasons_recommendations_display()
                ], style=card_body_style)
            ], style=card_style, id="results-card", className="mt-4 shadow")
        ], className="mt-4"),
        
        # Stockage de l'état de la prédiction
        dcc.Store(id="prediction-result"),
        dcc.Store(id="show-details", data=False)
    ])

# Callback pour afficher/masquer la section femmes en fonction du genre
@app.callback(
    Output("section-femmes", "style"),
    Input("genre", "value")
)
def toggle_women_section(genre):
    """
    Affiche ou masque la section spécifique aux femmes en fonction du genre sélectionné.

    Args:
        genre (str): Le genre sélectionné (Homme ou Femme).

    Returns:
        dict: Un dictionnaire contenant les propriétés de style, soit pour afficher, soit pour masquer la section.
    """
    if genre == "Femme":
        return {"display": "block", "marginBottom": "20px"}
    return {"display": "none"}


@app.callback(
    Output("date_dernier_don_container", "style"),
    Input("a_deja_donne", "value")
)
def toggle_date_dernier_don(a_deja_donne):
    """
    Affiche ou masque le conteneur de date du dernier don en fonction de la réponse à la question "A déjà donné le sang".

    Args:
        a_deja_donne (str): La valeur sélectionnée (Oui ou Non).

    Returns:
        dict: Un dictionnaire contenant les propriétés de style, soit pour afficher, soit pour masquer le conteneur.
    """
    if a_deja_donne == "Oui":
        return {"display": "block", "marginBottom": "20px", "animation": "fadeIn 0.3s ease"}
    return {"display": "none"}

# Callback pour la prédiction
@app.callback(
    [Output("prediction-result", "data"),
     Output("results-card", "style"),
     Output("prediction-status-container", "children"),
     Output("probability-container", "style"),
     Output("probability-gauges", "children"),
     Output("details-button-container", "style"),
     Output("reasons-container", "children"),
     Output("recommendations-container", "children")],
    [Input("predict-button", "n_clicks")],
    [State("genre", "value"),
     State("age", "value"),
     State("niveau_etude", "value"),
     State("situation_matrimoniale", "value"),
     State("religion", "value"),
     State("taux_hemoglobine", "value"),
     State("a_deja_donne", "value"),
     State("mois_dernier_don", "value"),
     State("annee_dernier_don", "value"),
     State("profession", "value"),
     State("taille", "value"),
     State("poids", "value"),
     State("arrondissement_de_residence", "value"),
     State("quartier_residence", "value"),
     State("nationalite", "value"),
     # Nouveaux champs médicaux
     State("anti_biotherapie", "value"),
     State("ist_recente", "value"),
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
     # Champs spécifiques aux femmes
     State("ddr_recent", "value"),
     State("allaitement", "value"),
     State("accouchement_recent", "value"),
     State("interruption_grossesse", "value"),
     State("enceinte", "value"),
     State("autre_raison_indispo_femme", "value"),
     # Autre raison d'inéligibilité
     State("autre_raison_ineligible", "value"),
     # Styles pour le results-card
     State("results-card", "style"),
     # Langue
     State("language-store", "data")]
)
def predict_eligibility(n_clicks, genre, age, niveau_etude, situation_matrimoniale, religion, 
                     taux_hemoglobine, a_deja_donne, mois_dernier_don, annee_dernier_don,
                     profession, taille, poids, arrondissement_de_residence, quartier_residence, nationalite,
                     anti_biotherapie, ist_recente, antecedent_transfusion, porteur_hiv, opere_recemment,
                     drepanocytaire, diabetique, hypertendu, asthmatique, cardiaque, tatoue, scarifie,
                     ddr_recent, allaitement, accouchement_recent, interruption_grossesse, enceinte,
                     autre_raison_indispo_femme, autre_raison_ineligible, results_card_style, language):
    """
    Prédit l'éligibilité au don de sang en envoyant les données à l'API et affiche les résultats.
    """
    translations = TRANSLATIONS[language]
    
    if not n_clicks:
        # Valeurs par défaut pour le chargement initial
        return None, {'display': 'none'}, None, {'display': 'none'}, None, {'display': 'none'}, None, None
    
    # Préparer les données pour l'API
    date_dernier_don = None
    if a_deja_donne == "Oui" and mois_dernier_don is not None and annee_dernier_don is not None:
        date_dernier_don = f"{mois_dernier_don:02d}/{annee_dernier_don}"
    
    api_data = {
        "Genre": genre,
        "Age": age,
        "Niveau_etude": niveau_etude,
        "Situation_Matrimoniale": situation_matrimoniale,
        "Religion": religion,
        "Taux_hemoglobine": taux_hemoglobine,
        "A_deja_donne": a_deja_donne,
        "Date_dernier_don": date_dernier_don,
        "Profession": profession,
        "Taille": taille,
        "Poids": poids,
        "Arrondissement_de_residence": arrondissement_de_residence,
        "Quartier_residence": quartier_residence,
        "Nationalite": nationalite,
        # Conditions médicales
        "Anti_biotherapie": anti_biotherapie,
        "IST_recente": ist_recente,
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
    
    # Ajouter les champs spécifiques aux femmes si applicable
    if genre == "Femme":
        api_data.update({
            "DDR_recent": ddr_recent,
            "Allaitement": allaitement,
            "Accouchement_recent": accouchement_recent,
            "Interruption_grossesse_recente": interruption_grossesse,
            "Enceinte": enceinte,
            "Autre_raison_indispo_femme": autre_raison_indispo_femme if autre_raison_indispo_femme else None
        })
    
    try:
        # Envoyer la requête à l'API
        response = requests.post("https://api-blood-donnation.onrender.com/predict", json=api_data)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extraire le statut d'éligibilité et les probabilités
            statut = result.get("statut", "")
            probabilites = result.get("probabilites", {})
            message = result.get("message", "")
            raisons = result.get("raisons", [])
            recommandations = result.get("recommandations", [])
            
            # Afficher le statut d'éligibilité
            if statut == "Eligible":
                status_ui = create_eligibility_status_container(
                    translations["Éligible au don de sang"],
                    "linear-gradient(135deg, #2ecc71, #27ae60)",
                    "mdi:check-circle"
                )
                status_color = "#2ecc71"  # Vert
            elif statut == "Temporairement Non-eligible":
                status_ui = create_eligibility_status_container(
                    translations["Temporairement non éligible"],
                    "linear-gradient(135deg, #f39c12, #e67e22)",
                    "mdi:alert-circle"
                )
                status_color = "#f39c12"  # Orange
            else:
                status_ui = create_eligibility_status_container(
                    translations["Définitivement non éligible"],
                    "linear-gradient(135deg, #e74c3c, #c0392b)",
                    "mdi:close-circle"
                )
                status_color = "#e74c3c"  # Rouge
            
            # Ajouter le message détaillé
            status_ui.children.append(
                html.Div(
                    message,
                    style={
                        'padding': '15px',
                        'borderRadius': '8px',
                        'backgroundColor': f'rgba({status_color[1:3]}, {status_color[3:5]}, {status_color[5:7]}, 0.1)',
                        'marginTop': '15px',
                        'textAlign': 'center',
                        'fontWeight': '600',
                        'color': status_color,
                        'border': f'1px solid {status_color}'
                    }
                )
            )
            
            # Créer les jauges pour les probabilités
            probability_gauges = []
            
            # Ordre des statuts pour l'affichage
            status_order = ["Eligible", "Temporairement Non-eligible", "Définitivement non-eligible"]
            colors = ["rgba(46, 204, 113, 0.8)", "rgba(243, 156, 18, 0.8)", "rgba(231, 76, 60, 0.8)"]
            
            for i, status_key in enumerate(status_order):
                translated_status = translations.get(status_key, status_key)
                prob_value = probabilites.get(status_key, 0)
                
                gauge = html.Div(
                    dcc.Graph(
                        figure=create_probability_gauge(prob_value, translated_status, colors[i]),
                        config={'displayModeBar': False}
                    ),
                    style={'flex': '1', 'maxWidth': '33%', 'minWidth': '150px'}
                )
                probability_gauges.append(gauge)
            
            # Créer les items pour les raisons
            reasons_items = []
            if raisons:
                for reason in raisons:
                    reasons_items.append(
                        html.Div(
                            reason,
                            style={
                                'padding': '8px',
                                'marginBottom': '8px',
                                'borderRadius': '4px',
                                'backgroundColor': 'rgba(243, 156, 18, 0.1)',
                                'borderLeft': '3px solid #f39c12'
                            }
                        )
                    )
            else:
                reasons_items.append(
                    html.Div(
                        "Aucune raison particulière identifiée.",
                        style={
                            'padding': '8px',
                            'fontStyle': 'italic',
                            'color': '#888'
                        }
                    )
                )
            
            # Créer les items pour les recommandations
            recommendations_items = []
            if recommandations:
                for recommendation in recommandations:
                    recommendations_items.append(
                        html.Div(
                            recommendation,
                            style={
                                'padding': '8px',
                                'marginBottom': '8px',
                                'borderRadius': '4px',
                                'backgroundColor': 'rgba(26, 188, 156, 0.1)',
                                'borderLeft': '3px solid #1abc9c'
                            }
                        )
                    )
            else:
                recommendations_items.append(
                    html.Div(
                        "Aucune recommandation disponible.",
                        style={
                            'padding': '8px',
                            'fontStyle': 'italic',
                            'color': '#888'
                        }
                    )
                )
            
            # Mettre à jour le style de la carte des résultats pour l'afficher
            updated_results_card_style = dict(results_card_style)
            updated_results_card_style['display'] = 'block'
            
            return (
                result, 
                updated_results_card_style,
                status_ui,
                {'display': 'block'},
                probability_gauges,
                {'textAlign': 'center', 'marginTop': '20px', 'display': 'block'},
                reasons_items,
                recommendations_items
            )
        else:
            # Gérer l'erreur de l'API
            error_status = html.Div([
                html.Div([
                    html.Div([
                        get_icon("mdi:alert-circle", 48, "white"),
                    ], style={'marginRight': '15px'}),
                    html.H3(translations["Erreur lors de la prédiction"], style={"color": "white", "marginBottom": "0px"})
                ], style={
                    'display': 'flex', 
                    'alignItems': 'center', 
                    'justifyContent': 'center', 
                    'marginBottom': '15px',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'background': 'linear-gradient(135deg, #e74c3c, #c0392b)',
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
                }),
                html.Div(
                    f"Erreur: {response.status_code} - {response.text}",
                    style={
                        'padding': '15px',
                        'borderRadius': '8px',
                        'backgroundColor': 'rgba(231, 76, 60, 0.1)',
                        'marginTop': '15px',
                        'textAlign': 'center',
                        'fontWeight': '400',
                        'color': '#e74c3c',
                        'border': '1px solid #e74c3c'
                    }
                )
            ])
            
            # Mettre à jour le style de la carte des résultats pour l'afficher
            updated_results_card_style = dict(results_card_style)
            updated_results_card_style['display'] = 'block'
            
            return (
                None, 
                updated_results_card_style,
                error_status,
                {'display': 'none'},
                None,
                {'display': 'none'},
                None,
                None
            )
    
    except Exception as e:
        # Gérer les autres erreurs
        error_status = html.Div([
            html.Div([
                html.Div([
                    get_icon("mdi:alert-circle", 48, "white"),
                ], style={'marginRight': '15px'}),
                html.H3(translations["Erreur lors de la prédiction"], style={"color": "white", "marginBottom": "0px"})
            ], style={
                'display': 'flex', 
                'alignItems': 'center', 
                'justifyContent': 'center', 
                'marginBottom': '15px',
                'padding': '20px',
                'borderRadius': '10px',
                'background': 'linear-gradient(135deg, #e74c3c, #c0392b)',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
            }),
            html.Div(
                f"Erreur: {str(e)}",
                style={
                    'padding': '15px',
                    'borderRadius': '8px',
                    'backgroundColor': 'rgba(231, 76, 60, 0.1)',
                    'marginTop': '15px',
                    'textAlign': 'center',
                    'fontWeight': '400',
                    'color': '#e74c3c',
                    'border': '1px solid #e74c3c'
                }
            )
        ])
        
        # Mettre à jour le style de la carte des résultats pour l'afficher
        updated_results_card_style = dict(results_card_style)
        updated_results_card_style['display'] = 'block'
        
        return (
            None, 
            updated_results_card_style,
            error_status,
            {'display': 'none'},
            None,
            {'display': 'none'},
            None,
            None
        )

# Callback pour afficher/masquer les détails
@app.callback(
    [Output("details-container", "style"),
     Output("show-details", "data"),
     Output("toggle-details-btn", "children")],
    [Input("toggle-details-btn", "n_clicks")],
    [State("show-details", "data"),
     State("language-store", "data")]
)
def toggle_details(n_clicks, show_details, language):
    """Affiche ou masque les détails des raisons et recommandations."""
    translations = TRANSLATIONS[language]
    
    if not n_clicks:
        return {'display': 'none'}, False, [
            get_icon("mdi:information-outline", 16, "white"),
            translations["Voir les détails"]
        ]
    
    if show_details:
        return {'display': 'none'}, False, [
            get_icon("mdi:information-outline", 16, "white"),
            translations["Voir les détails"]
        ]
    else:
        return {'display': 'block'}, True, [
            get_icon("mdi:eye-off-outline", 16, "white"),
            translations["Voir les détails"]
        ]