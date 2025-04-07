import sqlite3
import hashlib
import os
from pathlib import Path
from werkzeug.security import check_password_hash

def get_connected_user_info(email):
    """
    Récupère toutes les informations de l'utilisateur connecté.
    
    Args:
        email (str): L'email de l'utilisateur connecté.
        
    Returns:
        dict: Un dictionnaire contenant toutes les informations de l'utilisateur:
            - id: L'identifiant de l'utilisateur
            - email: L'email de l'utilisateur
            - is_admin: Booléen indiquant si l'utilisateur est administrateur
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('users/user.db')
        cursor = conn.cursor()
        
        # Récupération des informations de l'utilisateur
        cursor.execute("""
            SELECT id, email, password, is_admin
            FROM users 
            WHERE email = ?
        """, (email,))
        
        user_data = cursor.fetchone()
        
        # Fermeture de la connexion
        conn.close()
        
        if not user_data:
            # Aucun utilisateur trouvé avec cet email
            return None
        
        # Construction du dictionnaire avec les informations disponibles
        user_info = {
            'id': user_data[0],
            'email': user_data[1],
            'is_admin': bool(user_data[3]),  # Conversion en booléen
        }
        
        return user_info
        
    except Exception as e:
        print(f"Erreur lors de la récupération des informations utilisateur: {e}")
        return {
            'id': None,
            'email': email,
            'is_admin': False,
            'error': str(e)
        }

def verify_credentials(email, password):
    """
    Vérifie si les identifiants fournis correspondent à un utilisateur dans la base de données.
    
    Args:
        email (str): L'email de l'utilisateur.
        password (str): Le mot de passe de l'utilisateur.
        
    Returns:
        bool: True si les identifiants sont valides, False sinon.
    """
    # Vérifier que les entrées ne sont pas vides
    if not email or not password:
        return False
    
    try:
        # Chemin vers la base de données
        db_path = 'users/user.db'
        
        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            # La base de données n'existe pas, donc les identifiants ne peuvent pas être valides
            print("Base de données d'utilisateurs introuvable.")
            return False
        
        # Hasher le mot de passe fourni
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les identifiants
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE email = ? AND password = ?",
            (email, hashed_password)
        )
        
        # Récupérer le résultat
        result = cursor.fetchone()[0] > 0
        
        # Fermer la connexion
        conn.close()
        
        return result
    
    except Exception as e:
        print(f"Erreur lors de la vérification des identifiants: {e}")
        return False

def get_user_info(email):
    """
    Récupère les informations d'un utilisateur à partir de son email.
    
    Args:
        email (str): L'email de l'utilisateur.
        
    Returns:
        dict: Un dictionnaire contenant les informations de l'utilisateur ou None si l'utilisateur n'existe pas.
    """
    try:
        # Chemin vers la base de données
        db_path = 'users/user.db'
        
        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            return None
        
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer les informations de l'utilisateur
        cursor.execute(
            "SELECT id, email, is_admin FROM users WHERE email = ?",
            (email,)
        )
        
        user = cursor.fetchone()
        
        # Fermer la connexion
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'is_admin': bool(user[2])
            }
        return None
    
    except Exception as e:
        print(f"Erreur lors de la récupération des informations utilisateur: {e}")
        return None

def get_all_users():
    """
    Récupère la liste de tous les utilisateurs dans la base de données.
    
    Returns:
        list: Une liste de dictionnaires contenant les informations des utilisateurs.
    """
    try:
        # Chemin vers la base de données
        db_path = 'users/user.db'
        
        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            return []
        
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les utilisateurs
        cursor.execute("SELECT id, email, is_admin FROM users")
        users = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()
        
        # Convertir les résultats en liste de dictionnaires
        return [{'id': user[0], 'email': user[1], 'is_admin': bool(user[2])} for user in users]
    
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs: {e}")
        return []

def add_user(email, password, is_admin=False):
    """
    Ajoute un nouvel utilisateur à la base de données.
    
    Args:
        email (str): L'email du nouvel utilisateur.
        password (str): Le mot de passe du nouvel utilisateur.
        is_admin (bool): Indique si l'utilisateur est un administrateur.
        
    Returns:
        dict: Le nouvel utilisateur ajouté ou None en cas d'erreur.
    """
    try:
        # Chemin vers la base de données
        db_path = 'users/user.db'
        
        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            # Créer le dossier si nécessaire
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            # Créer la base de données
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Créer la table users
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
            ''')
            
            conn.commit()
        else:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
        
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return None
        
        # Hasher le mot de passe
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insérer le nouvel utilisateur
        cursor.execute(
            "INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
            (email, hashed_password, 1 if is_admin else 0)
        )
        
        # Récupérer l'ID du nouvel utilisateur
        user_id = cursor.lastrowid
        
        # Valider les changements
        conn.commit()
        
        # Fermer la connexion
        conn.close()
        
        # Retourner les informations du nouvel utilisateur
        return {
            'id': user_id,
            'email': email,
            'is_admin': is_admin
        }
    
    except Exception as e:
        print(f"Erreur lors de l'ajout d'un utilisateur: {e}")
        return None

def delete_user(user_id):
    """
    Supprime un utilisateur de la base de données.
    
    Args:
        user_id (int): L'ID de l'utilisateur à supprimer.
        
    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    try:
        # Chemin vers la base de données
        db_path = 'users/user.db'
        
        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            return False
        
        # Vérifier si c'est le dernier administrateur
        users = get_all_users()
        admin_count = sum(1 for user in users if user['is_admin'])
        is_admin = next((user['is_admin'] for user in users if user['id'] == user_id), False)
        
        if admin_count <= 1 and is_admin:
            return False  # Ne pas supprimer le dernier administrateur
        
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Supprimer l'utilisateur
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        # Valider les changements
        conn.commit()
        
        # Fermer la connexion
        conn.close()
        
        return True
    
    except Exception as e:
        print(f"Erreur lors de la suppression d'un utilisateur: {e}")
        return False

def initialize_database_if_needed():
    """
    Vérifie si la base de données existe et l'initialise si nécessaire.
    """
    db_path = Path('users/user.db')
    
    # Vérifier si le dossier et la base de données existent
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True)
    
    # Si la base de données n'existe pas, créer l'utilisateur admin par défaut
    if not db_path.exists():
        add_user("crepinkoulo@gmail.com", "1471", is_admin=True)
        print("Base de données initialisée avec l'administrateur par défaut.")
        
        
def get_admin_email():
    """
    Récupère l'email de l'administrateur depuis la base de données.
    
    Returns:
        str: L'email de l'administrateur ou None si aucun administrateur n'est trouvé
             ou en cas d'erreur.
    """
    try:
        # Chemin vers la base de données
        db_path = 'users/user.db'
        
        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            print("Base de données d'utilisateurs introuvable.")
            return None
        
        # Se connecter à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer l'email de l'administrateur (le premier trouvé si plusieurs)
        cursor.execute(
            "SELECT email FROM users WHERE is_admin = 1 LIMIT 1"
        )
        
        result = cursor.fetchone()
        
        # Fermer la connexion
        conn.close()
        
        # Retourner l'email de l'administrateur s'il existe
        if result:
            return result[0]
        else:
            print("Aucun administrateur trouvé dans la base de données.")
            return None
    
    except Exception as e:
        print(f"Erreur lors de la récupération de l'email de l'administrateur: {e}")
        return None        