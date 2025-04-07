import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import markdown2
import plotly.graph_objects as go
import re
from dash import html
import socket
from utilss.auth_utils import get_admin_email
from dash_iconify import DashIconify
import pandas as pd



def send_upload_notification_email(filename, language,maill=get_admin_email()):
    # Email configuration
    """
    Sends an email notification to the recipient when a file is uploaded to the
    blood donation dashboard system.

    Args:
        filename (str): The name of the uploaded file.
        language (str): The language of the email notification ('fr' or 'en').

    Returns:
        None
    """
    sender_email = "kosprogcrepin@gmail.com"
    sender_password = "logy mvpc lent enok"
    recipient_email = get_admin_email()

    # Email content based on language
    if language == 'fr':
        subject = "Mise à jour réussie de la base de données"
        body = f"Le fichier {filename} a été uploadé avec succès dans le système de dashboard de don de sang par {maill}."
    else:
        subject = "Successful Database Update"
        body = f"The file {filename} has been successfully uploaded to the blood donation dashboard system."

    try:
        # Set a longer timeout
        socket.setdefaulttimeout(30)  # 30 seconds timeout

        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach body
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP session with more robust connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()  # Can help with connection issues
            server.starttls()  # Use TLS encryption
            server.ehlo()  # Call ehlo again after starttls
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Email notification sent successfully")

    except socket.timeout:
        print("Connection timed out. Check your internet connection.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email notification: {e}")




def modifier_ligne(nom_fichier, numero_ligne, nouveau_contenu):
    # Lire toutes les lignes du fichier
    """
    Modifie le contenu d'une ligne spécifique dans un fichier.

    Args:
        nom_fichier (str): Le nom du fichier à modifier.
        numero_ligne (int): Le numéro de la ligne à modifier (commence à 1).
        nouveau_contenu (str): Le nouveau contenu à insérer dans la ligne spécifiée.

    Returns:
        bool: True si la modification a réussi, False si le numéro de ligne est invalide.
    """

    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
    
    # Vérifier que le numéro de ligne est valide
    if numero_ligne < 1 or numero_ligne > len(lignes):
        print(f"Erreur: La ligne {numero_ligne} n'existe pas")
        return False
    
    # Modifier la ligne spécifiée (les indices commencent à 0, donc on soustrait 1)
    lignes[numero_ligne - 1] = nouveau_contenu + '\n'
    
    # Réécrire le fichier avec les modifications
    with open(nom_fichier, 'w') as fichier:
        fichier.writelines(lignes)
    
    return True


def safe_markdown_to_children(text):
    """
    Convertit le markdown en un paragraphe unique Dash.

    Args:
        text (str): Le texte markdown à convertir.

    Returns:
        dash.html.P: Un composant paragraphe Dash contenant le texte converti.
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
 
 
 
def get_icon(name, size=20, color="#e74c3c", with_animation=False, animation_type="pulse"):
    """
    Crée une icône avec effets et animations optionnels
    
    Args:
        name (str): Nom de l'icône
        size (int): Taille de l'icône
        color (str): Couleur de l'icône
        with_animation (bool): Activer l'animation
        animation_type (str): Type d'animation (pulse, bounce, spin)
        
    Returns:
        DashIconify: L'icône avec des animations optionnelles
    """
    # Classes pour les animations
    animation_class = ""
    if with_animation:
        if animation_type == "pulse":
            animation_class = "icon-pulse"
        elif animation_type == "bounce":
            animation_class = "icon-bounce"
        elif animation_type == "spin":
            animation_class = "icon-spin"
    
    return DashIconify(
        icon=name,
        width=size,
        height=size,
        color=color,
        className=animation_class
    )

# Fonction pour calculer l'IMC (BMI)
def calculate_bmi(height_cm, weight_kg):
    """
    Calcule l'indice de masse corporelle (IMC/BMI)
    
    Args:
        height_cm (float): Taille en centimètres
        weight_kg (float): Poids en kilogrammes
        
    Returns:
        float: Valeur de l'IMC
    """
    if height_cm <= 0 or weight_kg <= 0:
        return 0
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 1)

# Fonction pour obtenir la catégorie et la couleur de l'IMC

# Fonction utilitaire pour créer des icônes avec animations et effets

# Fonction pour calculer l'IMC (BMI)
def calculate_bmi(height_cm, weight_kg):
    """
    Calcule l'indice de masse corporelle (IMC/BMI)
    
    Args:
        height_cm (float): Taille en centimètres
        weight_kg (float): Poids en kilogrammes
        
    Returns:
        float: Valeur de l'IMC
    """
    if height_cm <= 0 or weight_kg <= 0:
        return 0
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 1)

# Fonction pour obtenir la catégorie et la couleur de l'IMC
def get_bmi_category(bmi):
    """
    Obtient la catégorie et la couleur correspondant à un IMC
    
    Args:
        bmi (float): Valeur de l'IMC
        
    Returns:
        tuple: (catégorie, couleur)
    """
    if bmi < 16.5:
        return "Dénutrition", "#2c3e50"  # Bleu foncé
    elif bmi < 18.5:
        return "Maigreur", "#3498db"  # Bleu
    elif bmi < 25:
        return "Normal", "#2ecc71"  # Vert
    elif bmi < 30:
        return "Surpoids", "#f39c12"  # Orange
    elif bmi < 35:
        return "Obésité modérée", "#e67e22"  # Orange foncé
    elif bmi < 40:
        return "Obésité sévère", "#d35400"  # Rouge orangé
    else:
        return "Obésité morbide", "#c0392b"  # Rouge

# Fonction pour créer un conteneur pour chaque statut d'éligibilité avec animation et effets 3D
def create_eligibility_status_container(status, color_gradient, icon_name, animate=True):
    """
    Crée un conteneur stylisé pour afficher le statut d'éligibilité avec effets 3D et animations.
    
    Args:
        status (str): Le texte du statut à afficher
        color_gradient (str): Le gradient de couleur CSS pour l'arrière-plan
        icon_name (str): Le nom de l'icône à afficher
        animate (bool): Activer l'animation d'entrée
        
    Returns:
        html.Div: Un div contenant l'affichage stylisé du statut
    """
    animation_class = "fade-in-scale" if animate else ""
    
    return html.Div([
        html.Div([
            html.Div([
                get_icon(icon_name, 48, "white", with_animation=True, animation_type="pulse"),
            ], style={'marginRight': '15px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            html.H3(status, style={
                "color": "white", 
                "marginBottom": "0px", 
                "fontWeight": "bold",
                "textShadow": "1px 1px 3px rgba(0,0,0,0.2)"
            })
        ], style={
            'display': 'flex', 
            'alignItems': 'center', 
            'justifyContent': 'center', 
            'marginBottom': '15px',
            'padding': '22px',
            'borderRadius': '15px',
            'background': color_gradient,
            'boxShadow': '0 8px 16px rgba(0, 0, 0, 0.15), inset 0 -4px 0 rgba(0, 0, 0, 0.1)',
            'transition': 'all 0.3s ease',
            'transform': 'translateZ(0)',
            'backfaceVisibility': 'hidden',
            'overflow': 'hidden',
            'position': 'relative'
        }, className=animation_class)
    ], style={
        'position': 'relative',
        'overflow': 'hidden'
    })

# Créer un indicateur de jauge amélioré pour l'éligibilité avec effets d'animations et styles modernes

def create_probability_gauge(probability, title, color, plot_font_color="black", animated=True):
    """
    Crée une jauge moderne et animée pour afficher la probabilité d'un statut d'éligibilité.
    
    Args:
        probability (float): La probabilité à afficher (entre 0 et 1)
        title (str): Le titre de la jauge
        color (str): La couleur de la jauge
        plot_font_color (str): La couleur du texte
        animated (bool): Activer l'animation de la jauge
    
    Returns:
        go.Figure: Une figure Plotly contenant la jauge de probabilité
    """
    # Initialiser les valeurs RGB
    r, g, b = 0, 0, 0
    
    # Extraire les composantes RGB de la couleur
    if isinstance(color, str):
        if color.startswith('rgba('):
            try:
                parts = color.replace('rgba(', '').replace(')', '').split(',')
                r, g, b = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())
                base_rgb = f"rgb({r}, {g}, {b})"
            except (ValueError, IndexError):
                base_rgb = color
        elif color.startswith('rgb('):
            try:
                parts = color.replace('rgb(', '').replace(')', '').split(',')
                r, g, b = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())
                base_rgb = color
            except (ValueError, IndexError):
                base_rgb = color
        elif color.startswith('#'):
            try:
                hex_color = color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join([c*2 for c in hex_color])
                r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                base_rgb = color
            except (ValueError, IndexError):
                base_rgb = color
        else:
            base_rgb = color
    else:
        base_rgb = color
    
    # Créer des dégradés pour la jauge
    step_colors = [
        f"rgba({r}, {g}, {b}, 0.15)",
        f"rgba({r}, {g}, {b}, 0.3)",
        f"rgba({r}, {g}, {b}, 0.6)"
    ]
    
    # Créer la figure pour la jauge - démarrer à 0 si animé
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0 if animated else probability * 100,
        title={
            'text': title, 
            'font': {'size': 16, 'color': plot_font_color, 'family': 'Arial, sans-serif', 'weight': 'bold'}
        },
        number={'suffix': '%', 'font': {'size': 24, 'color': plot_font_color, 'weight': 'bold'}},
        gauge={
            'axis': {
                'range': [0, 100], 
                'tickwidth': 2, 
                'tickcolor': plot_font_color, 
                'tickfont': {'color': plot_font_color, 'size': 12},
                'tickvals': [0, 25, 50, 75, 100],
                'ticktext': ['0%', '25%', '50%', '75%', '100%']
            },
            'bar': {'color': base_rgb, 'thickness': 0.7},
            'bgcolor': "rgba(0, 0, 0, 0.05)",
            'borderwidth': 0,
            'bordercolor': plot_font_color,
            'steps': [
                {'range': [0, 33], 'color': step_colors[0]},
                {'range': [33, 67], 'color': step_colors[1]},
                {'range': [67, 100], 'color': step_colors[2]},
            ],
            'threshold': {
                'line': {'color': plot_font_color, 'width': 2},
                'thickness': 0.8,
                'value': probability * 100
            }
        }
    ))
    
    # Mise à jour du layout
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': plot_font_color, 'family': 'Arial, sans-serif'},
        margin=dict(l=30, r=30, b=20, t=40),
        height=200,
        transition_duration=1000 if animated else 0
    )
    
    # Gestion de l'animation simplifiée
    if animated:
        # Animation simplifiée avec transitions CSS
        indicator = fig.data[0]
        
        # Mettre à jour avec la valeur finale après un délai
        # Cela sera géré par le navigateur via la propriété transition_duration
        indicator.value = probability * 100
        
        # Ajouter un menu updatemenus pour déclencher l'animation au chargement
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Animer',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 1000, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 500, 'easing': 'cubic-in-out'}
                    }]
                }],
                'visible': False
            }]
        )
    
    return fig
#Créer une fonction pour afficher les raisons et recommandations
def create_reasons_recommendations_display():
    """
    Crée une disposition élégante pour afficher les raisons et recommandations.
    
    Returns:
        html.Div: Un div contenant la disposition pour les raisons et recommandations
    """
    return html.Div([
        html.Div([
            # Container pour les raisons
            html.Div([
                html.H4([
                    get_icon("mdi:alert-circle-outline", 24, "#f39c12"),
                    html.Span("Raisons", style={
                        'marginLeft': '10px',
                        'fontWeight': 'bold',
                        'letterSpacing': '0.5px'
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'color': '#f39c12',
                    'borderBottom': '1px solid rgba(243, 156, 18, 0.3)',
                    'paddingBottom': '12px',
                    'marginBottom': '15px'
                }),
                html.Div(id="reasons-container", style={
                    'maxHeight': '200px',
                    'overflowY': 'auto',
                    'padding': '15px',
                    'backgroundColor': 'rgba(255, 243, 224, 0.3)',
                    'borderRadius': '12px',
                    'border': '1px solid rgba(243, 156, 18, 0.3)',
                    'scrollbarWidth': 'thin',
                    'scrollbarColor': '#f39c12 rgba(243, 156, 18, 0.1)'
                }, className="custom-scrollbar")
            ], style={
                'flex': '1', 
                'marginRight': '20px',
                'transition': 'all 0.3s ease',
                'transform': 'translateZ(0)',
                'backgroundColor': 'rgba(255, 243, 224, 0.05)',
                'borderRadius': '15px',
                'padding': '15px',
                'boxShadow': '0 5px 15px rgba(243, 156, 18, 0.1)'
            }, className="reasons-box fade-in"),
            
            # Container pour les recommandations
            html.Div([
                html.H4([
                    get_icon("mdi:lightbulb-on", 24, "#1abc9c"),
                    html.Span("Recommandations", style={
                        'marginLeft': '10px',
                        'fontWeight': 'bold',
                        'letterSpacing': '0.5px'
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'color': '#1abc9c',
                    'borderBottom': '1px solid rgba(26, 188, 156, 0.3)',
                    'paddingBottom': '12px',
                    'marginBottom': '15px'
                }),
                html.Div(id="recommendations-container", style={
                    'maxHeight': '200px',
                    'overflowY': 'auto',
                    'padding': '15px',
                    'backgroundColor': 'rgba(224, 255, 251, 0.3)',
                    'borderRadius': '12px',
                    'border': '1px solid rgba(26, 188, 156, 0.3)',
                    'scrollbarWidth': 'thin',
                    'scrollbarColor': '#1abc9c rgba(26, 188, 156, 0.1)'
                }, className="custom-scrollbar")
            ], style={
                'flex': '1',
                'transition': 'all 0.3s ease',
                'transform': 'translateZ(0)',
                'backgroundColor': 'rgba(224, 255, 251, 0.05)',
                'borderRadius': '15px',
                'padding': '15px',
                'boxShadow': '0 5px 15px rgba(26, 188, 156, 0.1)'
            }, className="recommendations-box fade-in-delay")
        ], style={
            'display': 'flex', 
            'marginTop': '20px', 
            'marginBottom': '20px',
            'flexDirection': 'row',
            'flexWrap': 'wrap',
            'gap': '20px'
        }, className="flex-container")
    ], id="details-container", style={'display': 'none'})

def hex_to_rgba(hex_color, alpha=1.0):
    """Convertit une couleur hexadécimale en format rgba avec transparence"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f'rgba({r}, {g}, {b}, {alpha})'

 
 
 
 
 

  