import warnings
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy import stats

# Nettoyage et prétraitement des données
def nettoyer_donnees(df):
    # Renommer les colonnes pour faciliter leur manipulation
    """
    Nettoie et prétraite les données d'un DataFrame.

    Cette fonction effectue plusieurs opérations de nettoyage sur un DataFrame :
    - Renomme les colonnes en supprimant les espaces en début et fin de nom.
    - Supprime les lignes contenant des valeurs aberrantes dans la colonne 'Age'.
    - Convertit les valeurs de la colonne 'Age' en numériques, supprimant celles qui ne peuvent pas être converties.
    - Filtre les âges pour qu'ils soient dans une plage réaliste (entre 18 et 80 ans).
    - Gère les valeurs manquantes dans les colonnes catégorielles spécifiées en les remplissant avec la valeur la plus fréquente.

    Paramètres:
    -----------
    df : pandas.DataFrame
        Le DataFrame contenant les données à nettoyer.

    Retourne:
    --------
    pandas.DataFrame
        Le DataFrame nettoyé.
    """

    df.columns = [col.strip() for col in df.columns]
    
    # Supprimer les lignes avec des valeurs aberrantes dans 'Age'
    valeurs_aberrantes = [
        '25673051888', '00', '2O', '0', '4&', '00'
    ]
    
    # Supprimer les lignes contenant ces valeurs aberrantes
    df = df[~df['Age'].isin(valeurs_aberrantes)]
    # Convertir 'Age' en numérique, en gérant les erreurs
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    # Supprimer les lignes où 'Age' ne peut pas être converti en nombre
    df = df.dropna(subset=['Age'])
    
     # Filtrer les âges dans une plage réaliste (par exemple, entre 18 et 80 ans)
    df = df[(df['Age'] >= 18) & (df['Age'] <= 80)]
    print("Nombre de lignes après nettoyage des âges :", len(df))
    
    # Gestion des autres valeurs manquantes
    colonnes_categorielles = ['Sexe', 'Type de donation', 'Groupe Sanguin ABO / Rhesus', 'Phenotype']
    for col in colonnes_categorielles:
        df[col] = df[col].fillna(df[col].mode()[0])
    
    return df




### pour la corrrespondance entre quartier et arrondissement
correspondance = {
    "Pk 10": "Douala 5", "MBANGO": "Non spécifié", "Total Nkolmbon": "Douala 3", "PK30": "Non spécifié",
    "Ange Raphaël ": "Douala 1", "PK 25": "Non spécifié", "BONA PRISO GOUPWE": "Douala 1", 
    "Makepe missoke": "Douala 3", "JAPOMA": "Douala 5", "NDOGPASSI VILLAGE": "Douala 3",
    "TRADEX BONNE DIX": "Non spécifié", "Mboko": "Non spécifié", "Pas mentionné": "Non spécifié",
    "NEWBELL": "Douala 2", "NYALLA CHATEAU": "Douala 3", "YOUPWE": "Douala 4", 
    "VILLAGE MARCHE": "Non spécifié", "CITE SIC": "Douala 2", "NYALLA PAYS BAS": "Douala 3",
    "Ngodi Bakoko": "Douala 5", "DOGPASSI": "Douala 3", "BONENDALE": "Non spécifié", 
    "LOGBESSOU": "Douala 3", "NDOGPASSI 1": "Douala 3", " NDOGPASSI 3": "Douala 3",
    "Village entrée Bille": "Non spécifié", "BONANDJO": "Douala 1", "NDOKPASSI": "Douala 3",
    "MADAGASCAR": "Non spécifié", "New-Bell": "Douala 2", "NYALLA PARISO": "Douala 3",
    "BOKO PLAGE": "Non spécifié", "PK13 BASSA": "Douala 5", "Ndogssimbi": "Non spécifié",
    "Cité cic": "Douala 3", "Songogan bloc 11": "Non spécifié", "Nkomondo": "Douala 5",
    "Nkongmondo": "Douala 5", "Ndogbon": "Douala 2", "Ndokoti": "Douala 3",
    "Ange Raphaël": "Douala 1", "Cite de la paix": "Non spécifié", "douala": "Non spécifié",
    "Carrefour Agip": "Douala 1", "Hôpital général": "Douala 1", "Cité de palmiers": "Douala 5",
    "Bonapriso 2": "Douala 1", "Bependa casmando": "Douala 3", "Essengue": "Douala 2",
    "Douala-douala": "Non spécifié", "Ngodi- Akwa": "Douala 1", "Terminus": "Douala 3",
    "New priso": "Douala 1", "Ndogpassi": "Douala 3", "Bwang Bakoko": "Douala 5",
    "Ngodi- Bakoko": "Douala 5", "Ngodi bonomo": "Non spécifié", "Oyack": "Douala 3",
    "Entree bille": "Non spécifié", "Ipd": "Non spécifié", "Borne 10": "Douala 5", "Tergal": "Non spécifié",
    "Tradex borne 10": "Douala 5", "Kambo boko": "Non spécifié", "Regeneration": "Non spécifié",
    "Boko": "Douala 4", "Boko cogefar": "Non spécifié", "Tradex village": "Douala 5",
    "Soubom": "Douala 4", "Mbassong": "Non spécifié", "Nyalla pariso": "Douala 3",
    "Bepanda omnisport": "Douala 3", "Soboum": "Douala 4", "Mbangue": "Bot Makak",
    "Makafo": "Non spécifié", "PK12": "Douala 5", "Bessengue": "Douala 2", "Ndogpassi III": "Douala 3",
    "Mbanga bakoko": "Douala 5", "Ndogpassi I ": "Douala 3", "Ngodi Akwa": "Douala 1",
    "Cite de cille": "Non spécifié", "NDOGPASSI 2": "Douala 3", "Dakar": "Non spécifié", 
    "Douala": "Non spécifié", "BEPENDA": "Douala 3", "Ari ": "Non spécifié", "Douala douala": "Non spécifié",
    "Logbessou ": "Douala 3", "Bependa": "Douala 3", "Newbell": "Douala 2", 
    "Yansoki ": "Douala 5", "Pk8": "Douala 5", "Village": "Non spécifié", "Japoma": "Douala 5",
    "Terminus saint Michel ": "Douala 3", "Bonanjo": "Douala 1", "Yassa": "Douala 3",
    "Ccc ": "Douala 3", "Soboum-Dakar ": "Douala 4", "Hôpital général de douala ": "Douala 1",
    "Saint Thomas logbaba ": "Douala 3", "Bangapongo ": "Douala 4", "Makepe": "Douala 3",
    "New town aéroport ": "Douala 5", "NDOGPASSI 3": "Douala 3", "She’ll-village": "Douala 4",
    "She’ll village ": "Douala 4", "Bependa ": "Douala 3", "Bocom safari ": "Douala 3",
    "Kotto": "Douala 3", "Pk14": "Douala 5", "Logpom": "Douala 3", "Bonamoussadi": "Douala 5",
    "Bonamoussadi ": "Douala 5", "Ndogbong ": "Douala 2", "Douala ": "Non spécifié", "Pk10": "Douala 5",
    "Nyalla pariso ": "Douala 3", "Non précise ": "Non spécifié", "YASSA": "Douala 3", "Rien": "Non spécifié",
    "PK11": "Douala 5", "Pk11": "Douala 5", "Beedi": "Douala 3", "Douala CCC": "Douala 3",
    "Akwa": "Douala 1", "Deido": "Douala 1", "Bali": "Douala 1", "Bonapriso": "Douala 1",
    "Malangue": "Douala 5", "Ange rafael": "Douala 1", "Akwa ngodi": "Douala 1",
    "Newton aeroport": "Douala 5", "PK9": "Douala 5", "PK14": "Douala 5", "MAKEPE": "Douala 3",
    "BONABERI": "Douala 4", "DOUALA": "Non spécifié", "NGODI BAKOKO": "Douala 5", 
    "KOTTO IMMEUBLE": "Douala 3", "PK21": "Douala 5", "BEPENDA MATURITE": "Douala 3",
    "BP SITE": "Douala 5", "PK5": "Douala 5", "BP CITE": "Douala 2", "RUE FOCH": "Douala 1",
    "NEW-BELL": "Douala 2", "BEEDI": "Douala 3", "NDOKOTI": "Douala 3", "ENRI": "Non spécifié",
    "NDOPASSI III": "Douala 3", "DEIDO": "Douala 1", "KOTTO BONAMOUSSADI": "Douala 5",
    "LOGPOM": "Douala 3", "NYALLA": "Douala 3", "BOIS DE SINGE": "Douala 2", "DAKAR": "Non spécifié",
    "BONAMOUSSADI": "Douala 5", "VILLAGE": "Non spécifié", "NDOGPASSI I": "Douala 3",
    "MISSOLE II": "Douala 5", "BALI": "Douala 1", "NDOGBONG": "Douala 2", "BESSENGUE": "Douala 2",
    "NDOGPASSI": "Douala 3", "NYALLA HAOUSSA": "Douala 3", "CITE CICAM": "Douala 3",
    "NEW BELL BASSA": "Douala 2", "NKONGUONDO": "Douala 5", "NKONMONDO": "Douala 5",
    "NKONGMONDO": "Douala 5", "NGODI AKWA": "Douala 1", "QUARYIER ESPOIR": "Douala 5",
    "Pas precise": "Non spécifié", "Total nkolbong": "Non spécifié", "Jardin logbaba": "Douala 3",
    "Logbessou": "Douala 3", "Logbaba st thomad": "Douala 3", "Rue koloko bonapriso": "Douala 1",
    "Pk9": "Douala 5", "Bepanda": "Douala 3", "Bonaberie": "Douala 4", 
    "Cité-sic bassa": "Douala 2", "Nouvelle route cité sic": "Douala 2", 
    "Saint thomas": "Douala 3", "Cité sic": "Douala 2", "Pk17": "Douala 5", "Kms": "Non spécifié",
    "Newton aéroport ": "Douala 5", "Pk16": "Douala 5", "Pk15": "Douala 5", "Pk15 ": "Douala 5",
    "Journaliste ": "Non spécifié", "Ndogbong": "Douala 2", "Yassa ": "Douala 3", "Japouma ": "Douala 5",
    "Bonaloka": "Non spécifié", "Village ": "Non spécifié", "NDOGPASSI ": "Douala 3", "Brassaville": "Non spécifié",
    "New bell ": "Douala 2", "Pk5 new bell": "Douala 2", "Pk16(sappe )": "Douala 5",
    "Yansoki bakoko": "Douala 5", "Cité belge": "Douala 5", "Cité maetude ": "Non spécifié",
    "Logbaba jardin": "Douala 3", "Elf (rond point)": "Douala 1", "Logbaba": "Douala 3",
    "Dibombari": "Non spécifié", "New-bell /nkouloulou": "Douala 2", "Besengue ": "Douala 2",
    "Cité cicam": "Douala 3", "Non précisé": "Non spécifié", "Pas précisé": "Non spécifié",
    "Douala(non) précisé": "Non spécifié", "Douala non précisé": "Non spécifié", "BRAZZAVILLE": "Non spécifié",
    "Ndogpassi 2": "Douala 3", "Logpom ": "Douala 3", "Nkolbong": "Douala 3",
    "Borne 10 village ": "Non spécifié", "Henry ": "Non spécifié", "Henry": "Non spécifié",
    "Brazzaville ": "Douala 3", "New bell": "Douala 2", "PK18": "Douala 5",
    "Ndogpassi ": "Douala 3", "Ekithe ": "Non spécifié", "Nyalla ": "Douala 3", "Bonaberi": "Douala 4",
    "NDONGBONG": "Douala 2", "non precisé": "Non spécifié", "NON PRECISE": "Non spécifié",
    "Non precisé": "Non spécifié", "Yatika": "Non spécifié", "Pk13": "Douala 5",
    "Entree chinoise": "Douala 5", "Pk12": "Douala 5", "Cite des palmiers": "Douala 5",
    "Nyalla pariazo": "Douala 3", "Cogefar": "Non spécifié", "Ange raphael": "Douala 5",
    "Ndogpassi 3": "Douala 2", "Cite cicam": "Douala 5", "Sic cacao": "Douala 1",
    "BP Cité": "Douala 2", "Carrefour Bonabassem": "Douala 4", "Douala 812.12": "Non spécifié",
    "cité Sic": "Douala 5", "Cité sic": "Douala 5", "BOKO": "Douala 4", "Combi": "Non spécifié",
    "Nkoulouloun": "Non spécifié", "Brazaville": "Non spécifié", "Nyalla": "Douala 3",
    "Billongue": "Non spécifié", "Madagascar": "Douala 2", "Bonadiwoto": "Non spécifié",
    "Cite sic": "Douala 5", "Nkomodo": "Non spécifié", "Nglon": "Non spécifié",
    "Akwa nord": "Douala 1", "Cite de palmier": "Douala 5", "Ancien abatoire": "Non spécifié",
    "PK11 bassa": "Douala 3", "PK12 Emmene cite": "Douala 3", "Ngodi": "Non spécifié",
    "Logbaba plateau": "Douala 3", "Edea": "Non spécifié", "PK11 MBENGUE CITY": "Douala 3",
    "Globo": "Non spécifié", "PK12 MANDJAB": "Douala 3", "Bonadibong": "Non spécifié",
    "Ndogpassi3": "Douala 2", "Pas precisé": "Non spécifié", "Cité des palmiers": "Douala 5",
    "BEPANDA": "Douala 3", "PK10": "Douala 3", "LOGBABA": "Douala 3", "CITEE DES PALMIERS": "Douala 5",
    "Pk 10": "Douala 3", "MBANGO": "Lolodorf", "Total Nkolmbon": "Non spécifié",
    "PK30": "Non spécifié", "Ange Raphaël ": "Douala 5", "PK 25": "Non spécifié",
    "BONA PRISO GOUPWE": "Douala 1", "Makepe missoke": "Douala 4", "JAPOMA": "Douala 5",
    "NDOGPASSI VILLAGE": "Douala 2", "TRADEX BONNE DIX": "Non spécifié", "Mboko": "Non spécifié",
    "Pas mentionné": "Non spécifié", "NEWBELL": "Douala 4", "NYALLA CHATEAU": "Douala 5",
    "YOUPWE": "Douala 2", "VILLAGE MARCHE": "Non spécifié", "CITE SIC": "Douala 5",
    "NYALLA PAYS BAS": "Douala 5", "Ngodi Bakoko": "Non spécifié", "DOGPASSI": "Douala 2",
    "BONENDALE": "Douala 5", "LOGBESSOU": "Douala 4", "NDOGPASSI 1": "Douala 2",
    "NDOGPASSI 3": "Douala 2", "Village entrée Bille": "Douala 5", "BONANDJO": "Douala 1",
    "NDOKPASSI": "Douala 2", "MADAGASCAR": "Douala 2", "New-Bell": "Douala 4",
    "NYALLA PARISO": "Douala 5", "BOKO PLAGE": "Non spécifié", "PK13 BASSA": "Douala 3",
    "Ndogssimbi": "Non spécifié", "Cité cic": "Douala 5", "Songogan bloc 11": "Non spécifié",
    "Nkomondo": "Douala 1", "Nkongmondo": "Douala 1", "Ndogbon": "Douala 5",
    "Ndokoti": "Douala 2", "Ange Raphaël": "Douala 5", "Cite de la paix": "Douala 3",
    "douala": "Non spécifié", "Carrefour Agip": "Douala 1", "Hôpital général": "Douala 1",
    "Cité de palmiers": "Douala 5", "Bonapriso 2": "Douala 1", "Bependa casmando": "Douala 2",
    "Essengue": "Douala 1", "Douala-douala": "Non spécifié", "Ngodi- Akwa": "Douala 1",
    "Terminus": "Douala 1", "New priso": "Douala 1", "Ndogpassi": "Douala 2",
    "Bwang Bakoko": "Non spécifié", "Ngodi- Bakoko": "Non spécifié", "Ngodi bonomo": "Non spécifié",
    "Oyack": "Douala 3", "Entree bille": "Douala 5", "Ipd": "Non spécifié",
    "Borne 10": "Douala 3", "Tergal": "Non spécifié", "Tradex borne 10": "Douala 3",
    "Kambo boko": "Non spécifié", "Regeneration": "Non spécifié", "Boko": "Non spécifié",
    "Boko cogefar": "Non spécifié", "Tradex village": "Non spécifié", "Soubom": "Douala 2",
    "Mbassong": "Non spécifié", "Nyalla pariso": "Douala 5", "Bepanda omnisport": "Douala 2",
    "Soboum": "Douala 2", "Mbangue": "Bot Makak", "Makafo": "Non spécifié",
    "PK12": "Douala 3", "Bessengue": "Douala 1", "Ndogpassi III": "Douala 2",
    "Mbanga bakoko": "Non spécifié", "Ndogpassi I ": "Douala 2", "Ngodi Akwa": "Douala 1",
    "Cite de cille": "Douala 5", "Ndobong": "Non spécifié", "Brazzaville": "Douala 3",
    "Ndogbong Citadelle": "Non spécifié", "Anhe rafael": "Douala 5", "Bangue": "Non spécifié",
    "Elf": "Douala 1", "Jardin ndogmbe": "Non spécifié", "Pihidibamba": "Non spécifié",
    "Song mahop": "Non spécifié", "Songmahop": "Non spécifié", "Yassa tika": "Douala 5",
    "Ndokotti ccc": "Douala 2", "Boko plage": "Non spécifié", "Bilongue": "Non spécifié",
    "Bp cité": "Douala 2", "Ngodi bakoko": "Non spécifié", "Genie militaire": "Douala 1",
    "Bakoko": "Non spécifié", "Cité Sic": "Douala 5", "Bependa Omnisport": "Douala 2",
    "Bepanda Omnisport": "Douala 2", "Bahan": "Non spécifié", "Cite Berge": "Non spécifié",
    "Mbangopongo": "Lolodorf", "Shele village": "Douala 5", "Bonadoumbe": "Non spécifié",
    "Ndogsibi": "Non spécifié", "Pas précisé ": "Non spécifié", "R .A.S": "Non spécifié",
    "R A S": "Non spécifié", "ARI": "Non spécifié", "Oyack ": "Douala 3",
    "Dogbassi 3": "Douala 2", "R A S ": "Non spécifié", "NYALLA ": "Douala 5",
    "Ngodi bakogo": "Non spécifié", " R A S": "Non spécifié", "Madasgascar": "Douala 2",
    "RAS": "Non spécifié", "BILONGUE": "Non spécifié", "BP8232": "Non spécifié",
    "ROND POINT CCC": "Douala 2", "COGEFAR": "Non spécifié", "NEW BELL": "Douala 4",
    "ANGE RAPHAEL CAMPUS 2": "Douala 5", "BONATEKI DEIDO": "Douala 1", "AKWA NORD": "Douala 1",
    "CITE DE BILLE ": "Douala 5", "NGODI": "Non spécifié", "RAS ": "Non spécifié",
    "NDOBASSI 2": "Douala 2", "NDOG-PASSI": "Douala 2", "MBOKO": "Non spécifié",
    "BONAPRISO RUE KOLOKO": "Douala 1", "NEWTON AIRPORT": "Douala 5", "TEXACO AEROPORT": "Douala 5",
    "NEWTON  AIRPORT": "Douala 5", " Cité sic": "Douala 5", "bonaberi": "Douala 4",
    "Akwa": "Douala 1", "Bonadibong": "Douala 1", "Bonadiwoto": "Douala 3",
    "Bonadoumbe": "Douala 1", "Ngodi Akwa": "Douala 1", "Ngodi- Akwa": "Douala 1",
    "Ngodi bonomo": "Douala 1", "Bonaloka": "Douala 2", "Ndogssimbi": "Douala 2",
    "Songogan bloc 11": "Douala 2", "Ndogbon": "Douala 2", "Nkongmondo": "Douala 2",
    "Nkomondo": "Douala 2", "Ndogbong Citadelle": "Douala 2", "Jardin ndogmbe": "Douala 2",
    "Song mahop": "Douala 2", "Songmahop": "Douala 2", "Cite Berge": "Douala 2",
    "Brazzaville": "Douala 3", "Brassaville": "Douala 3", "BRAZZAVILLE": "Douala 3",
    "Brazaville": "Douala 3", "Bangue": "Douala 3", "Pihidibamba": "Douala 3",
    "Billongue": "Douala 4", "Bilongue": "Douala 4", "Bwang Bakoko": "Douala 4",
    "Bakoko": "Douala 4", "Ngodi Bakoko": "Douala 4", "Ngodi- Bakoko": "Douala 4",
    "Mbanga bakoko": "Douala 4", "Boko": "Douala 4", "Boko cogefar": "Douala 4",
    "Boko plage": "Douala 4", "Kambo boko": "Douala 4", "MBOKO": "Douala 4",
    "BOKO PLAGE": "Douala 4", "PK 25": "Douala 5", "PK30": "Douala 5",
    "Tradex village": "Douala 5", "TRADEX BONNE DIX": "Douala 5", "Total Nkolmbon": "Douala 5",
    "Total Nkolbong": "Douala 5", "Nkoulouloun": "Douala 5", "Nkolbong": "Douala 5",
    "New priso": "Douala 1", "Dibombari": "Douala 6", "Mboko": "Douala 6",
    "Ari": "Non spécifié", "Village": "Non spécifié", "VILLAGE": "Non spécifié",
    "Pas precise": "Non spécifié", "Non précisé": "Non spécifié", "Non precisé": "Non spécifié",
    "Pas précisé": "Non spécifié", "Pas mentionné": "Non spécifié", "VILLAGE MARCHE": "Non spécifié",
    "Oyack": "Douala 3", "Edea": "Non spécifié", "Meiganga": "Non spécifié",
    "Bahan": "Baham", "Shele village": "Douala 5", "Soboum": "Non spécifié",
    "Soubom": "Douala 2", "MBANGO": "Douala 1", "Mbangue": "Bot Makak",
    "Makafo": "Non spécifié", "Mbangopongo": "Lolodorf", "Nglon": "Non spécifié",
    "Ancien abatoire": "Douala 3", "Ngodi": "Non spécifié", "Globo": "Non spécifié",
    "Ekithe": "Non spécifié", "Yatika": "Non spécifié", "Cogefar": "Non spécifié",
    "Sic cacao": "Douala 1", "BP Cité": "Douala 2", "BP8232": "Non spécifié",
    "Combi": "Non spécifié", "Regeneration": "Non spécifié", "Cite de la paix": "Douala 1",
    "Douala-douala": "Non spécifié", "Douala douala": "Non spécifié", "douala": "Non spécifié",
    "Douala(non) précisé": "Non spécifié", "Douala non précisé": "Non spécifié", "DOUALA": "Non spécifié",
    "DAKAR": "Non spécifié", "CONGO": "Non spécifié", "ENRI": "Non spécifié",
    "Henry": "Non spécifié", "Journaliste": "Non spécifié", "Kms": "Non spécifié",
    "R .A.S": "Non spécifié", "R A S": "Non spécifié", "Ras": "Non spécifié",
    "R A S": "Non spécifié", "RAS": "Non spécifié", "NON PRECISE": "Non spécifié",
    "non precisé": "Non spécifié"
}


try:
    data =pd.read_excel('dataset/Challenge dataset.xlsx')
    df_volontaire = pd.read_excel('dataset/Challenge dataset.xlsx',sheet_name="2020")
except:
    data =pd.read_excel('dataset/Challenge dataset - Copie.xlsx')
    df_volontaire = pd.read_excel('dataset/Challenge dataset - Copie.xlsx',sheet_name="2020")   


df_volontaire = nettoyer_donnees(df_volontaire)
###################prosess data
## Detecter les date de controle incoherentes
invalid_day_control = data.loc[pd.to_datetime(data.iloc[:, 0],errors='coerce').isna()].iloc[:, 0].values

## process 1
def transform_date(date_str):
    """
    Transforms a date string with an invalid year to a valid date format.
    
    If the date string is found in the invalid_day_control array, it replaces the year with '2019'.
    Otherwise, it returns the original date string.
    
    Parameters:
    date_str (str): The date string to be transformed.
    
    Returns:
    str: The transformed date string or the original date string if no transformation is needed.
    """
    if date_str in invalid_day_control:
        try:
            date_parts = date_str.replace('/', '-').split('-')
            return '2019' + '-' + date_parts[0] + '-' + date_parts[1]
        except:
            return date_str
    else:
        return date_str


def corrige_date(data=data):
    """
    Corrects the dates in the given dataframe.

    This function transforms the dates in the first column of the dataframe using the `transform_date` function.
    It then replaces any invalid dates with the mode (most frequent date) of the transformed dates.

    Parameters:
    data (pandas.DataFrame): The dataframe containing the dates to be corrected.

    Returns:
    pandas.Series: A series containing the corrected dates.
    """
    step1 = pd.to_datetime(data.iloc[:, 0].apply(transform_date), errors='coerce', format='%Y-%m-%d')
    mode = step1.mode().values[0]
    return step1.apply(lambda x: mode if pd.isnull(x) else x)

###>>>> step1
data.iloc[:,0]  = corrige_date()


index_naiss = data.loc[pd.to_datetime(data.iloc[:,1],errors='coerce').isna()].iloc[:, 1].values


## process 2
def transform_element(element):
    """
    Transforme un élément de date en une date valide.

    Si l'élément de date se trouve dans l'index des dates de naissance invalides (index_naiss),
    il corrige l'année en fonction des deux derniers chiffres de l'année :
    - Si les deux derniers chiffres sont inférieurs à 19, l'année est corrigée en 2000+.
    - Sinon, l'année est corrigée en 1900+.

    Paramètres:
    element (str): La chaîne de caractères représentant la date à transformer.

    Retourne:
    str: La chaîne de caractères représentant la date transformée ou l'élément original si aucune transformation n'est nécessaire.
    """
    if element in index_naiss:
        last_two = int(element[-2:])
        if last_two < 19:
            parts = element.split('/')
            parts[2] = '2' + parts[2][1:]
            return '/'.join(parts)
        else:
            parts = element.split('/')
            parts[2] = '19' + parts[2][2:]
            return '/'.join(parts)
    else:
        return element

###>>>> step2
data.iloc[:,1] =  pd.to_datetime(data.iloc[:,1].apply(transform_element),errors='coerce')


######process arrondissemnt
def correspondance_quartier(ligne):
    """
    Attribue l'arrondissement de résidence en fonction du quartier de résidence.

    Cette fonction utilise un dictionnaire de correspondance pour attribuer l'arrondissement de résidence
    à partir du quartier de résidence. Si le quartier de résidence n'est pas trouvé dans le dictionnaire,
    elle retourne la valeur actuelle de l'arrondissement de résidence.

    Paramètres:
    ligne (pandas.Series): Une ligne du DataFrame contenant les informations sur le quartier de résidence.

    Retourne:
    str: L'arrondissement de résidence correspondant au quartier de résidence.
    """
    try:  
        ligne["Arrondissement de résidence"] = correspondance[ligne["Quartier de Résidence"]]
        
        return ligne["Arrondissement de résidence"]
        
    except:
        return ligne["Arrondissement de résidence"]


#####>>>>>> process3
data['Arrondissement de résidence'] = data.apply(lambda x: correspondance_quartier(x), axis=1).\
    str.lower().str.strip().str.replace('é','e').str.replace('ras','pas precise').\
    str.replace('non','pas').str.replace('r a s','ras').\
    str.replace('pas mentionne','pas precise').str.replace('ras','pas precise').\
    str.replace('pas precise','inconnu')


###### process nationnalite
def transform_nation(data=data,col='Nationalité'):
    """
    Transforme les valeurs de la colonne spécifiée en les nettoyant et en les standardisant.

    Cette fonction nettoie les valeurs de la colonne spécifiée en supprimant les espaces et les points,
    en convertissant les valeurs en minuscules et en remplaçant certaines valeurs spécifiques par des valeurs standardisées.

    Paramètres:
    data (pandas.DataFrame): Le dataframe contenant les données à transformer.
    col (str): Le nom de la colonne à transformer.

    Retourne:
    pandas.Series: Une série contenant les valeurs transformées de la colonne spécifiée.
    """
    return data[col].str.strip().str.replace('.','').str.replace(' ','').str.\
                lower().replace({'rien':'ras','nonprecisé':'ras','malien':'malienne'})
                
#####>>>>>> process4                
data['Nationalité']  = transform_nation()


###### process religion
data["Religion"] = (
    data["Religion"]\
    .str.lower()  # Convertir en minuscules
    .str.strip()  # Supprimer les espaces inutiles
    .str.replace(r"\s+", " ", regex=True)  # Remplacer les espaces multiples par un seul espace
)

# Standardiser les termes
replace_dict = {
    "chretien": "chrétien (protestant)",
    "pentecotiste": "pentecôtiste",
    "pantecotiste": "pentecôtiste",
    "pentecôtistes": "pentecôtiste",
    "chretien (catholique)": "chrétien (catholique)",
    "chretien (protestant )": "chrétien (protestant)",
    "chretien (ne de nouveau)": "chrétien (protestant)",
    "chretien (témoin de jéhovah)": "chrétien (témoin de jéhovah)",
    "chrétien non précisé": "chrétien (protestant)",
    "chrétien pas précisé": "chrétien (protestant)",
    "non precise": "pas précisé",
    "non-croyant": "non croyant",
    "loïc": "non croyant",  # Exemple de remplacement pour une entrée non pertinente
    "loique": "non croyant",
    "r a s": "pas précisé",
    "cmci": "chrétien (protestant)",
    "uebc": "chrétien (protestant)",
    "epc": "chrétien (protestant)",
    "aucune": "pas précisé",
    "laïc": "non croyant",
    "crois en tout": "croyant",
    "presbyterien": "chrétien (protestant)",
    "baptist": "chrétien (protestant)",
    "baptiste": "chrétien (protestant)",
    "adventiste": "chrétien (protestant)",
    "traditionaliste": "animiste",
    "animiste": "animiste",
    "croyant": "croyant",
    "chrétienne": "chrétien (protestant)",
    'chrétien': 'chrétien (protestant)'
}

# Appliquer le dictionnaire de remplacement
data["Religion"] = data["Religion"].replace(replace_dict)


### process raison indisponibilite
rais_indis = data.columns[data.columns.str.lower().str.startswith('raison indisponibilité')].tolist() 
for i,j in enumerate(rais_indis):
    data[j] = data[rais_indis].iloc[:,i].str.lower().\
        replace({'oui':rais_indis[i].split('[')[1].strip(']').strip()})


x= data[rais_indis].apply(lambda x: ','.join(x.astype(str)).\
                                       replace('non','nan').replace('nan','').strip(), axis=1)

x =  x.str.replace(',,,,', ',').str.replace(',,,', '').str.replace(',,', '').str.replace(',', '').str.strip(',')
data['Raison_indisponibilite'] =x

#######################################
### prossess raison indisponibilite de la femme
rais_indis = data.columns[data.columns.str.startswith('Raison de l’indisponibilité de la femme')].tolist() 

for i,j in enumerate(rais_indis):
    data[j] = data[rais_indis].iloc[:,i].str.lower().\
        replace({'oui':rais_indis[i].split('[')[1].strip(']').strip()})
        
        
########################################
### process raison non eligibilite
rais_de_non = data.columns[data.columns.str.lower().str.startswith('raison de n')].tolist() 
rais_de_non.append('Si autres raison préciser')


for i,j in enumerate(rais_de_non[:-1]):
    data[j] = data[rais_de_non].iloc[:,i].str.lower().\
        replace({'oui':rais_de_non[i].split('[')[1].strip(']').strip()})
        
        
## se ramener a une seule variable pour gerer les var indisponibilites
x  = data[rais_de_non].apply(lambda x: ' '.join(x.astype(str)).\
                                       replace('non','nan').replace('nan','').strip(), axis=1)
data['Raison de non-eligibilité totale'] = x.replace('', 'RAS')


### calcul de l age
a = (pd.to_datetime(data['Date de remplissage de la fiche']).dt.year - pd.to_datetime(data['Date de naissance']).dt.year)
data['Age']=a.values


# Remplacer les valeurs aberrantes par la médiane de l'âge
median_age = data['Age'].median()
data['Age'] = data['Age'].apply(lambda x: median_age if x <= 0 or x > 100 else x)

# Créer des classes d'âge
bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
data['Age_Class'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

        
data_final = data