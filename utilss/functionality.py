import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import markdown2
import re
from dash import html
import socket
from utilss.auth_utils import get_admin_email


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
  