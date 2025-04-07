import os
import sqlite3
import hashlib

def create_users_database():
    """
    Crée la base de données SQLite pour les utilisateurs si elle n'existe pas déjà.
    Insère un utilisateur administrateur par défaut.
    
    Returns:
        bool: True si la base de données a été créée ou mise à jour avec succès
    """
    # Créer le dossier users s'il n'existe pas
    if not os.path.exists('users'):
        os.makedirs('users')
    
    # Chemin vers la base de données
    db_path = 'users/user.db'
    
    # Vérifier si la base de données existe déjà
    db_exists = os.path.exists(db_path)
    
    # Se connecter à la base de données (ou la créer si elle n'existe pas)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Créer la table users si elle n'existe pas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
        ''')
        
        # Hasher le mot de passe par défaut pour plus de sécurité
        default_password = "1471"
        # En production, utilisez une méthode de hachage plus sécurisée comme bcrypt
        hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
        
        # Vérifier si l'utilisateur par défaut existe déjà
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", ("crepinkoulo@gmail.com",))
        user_exists = cursor.fetchone()[0] > 0
        
        # Insérer l'utilisateur par défaut s'il n'existe pas déjà
        if not user_exists:
            cursor.execute(
                "INSERT INTO users (email, password, is_admin) VALUES (?, ?, ?)",
                ("crepinkoulo@gmail.com", hashed_password, 1)
            )
            print("Utilisateur administrateur par défaut créé.")
        
        # Valider les changements
        conn.commit()
        print("Base de données initialisée avec succès.")
        return True
    
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")
        return False
    
    finally:
        # Fermer la connexion
        conn.close()

# Exécuter la fonction si ce script est exécuté directement
if __name__ == "__main__":
    create_users_database()
