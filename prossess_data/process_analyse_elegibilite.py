from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from prossess_data.prossess import data_final
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans



# Calculer la probabilité d'occurrence de chaque modalité pour les variables catégorielles
def calculate_probabilities(df, column):
    """
    Calculer les probabilités de chaque valeur unique dans une colonne spécifiée d'un DataFrame.
    Paramètres:
    df (pandas.DataFrame): Le DataFrame contenant les données.
    column (str): Le nom de la colonne pour laquelle calculer les probabilités.
    Retourne:
    pandas.Series: Une série où chaque valeur est remplacée par sa probabilité basée sur les comptes de valeurs de la colonne spécifiée.
    """
    
    probabilities = df[column].value_counts(normalize=True)
    return df[column].map(probabilities)



def cluster_df(data = data_final):
    """
    Effectue le clustering sur un DataFrame donné en utilisant les variables spécifiées.
    Cette fonction prend un DataFrame en entrée, sélectionne certaines variables pour le clustering,
    applique un prétraitement (standardisation des variables numériques et encodage des variables catégorielles),
    réduit la dimensionnalité des données avec TruncatedSVD, puis effectue un clustering avec KMeans.
    Paramètres:
    -----------
    data : DataFrame, optionnel
        Le DataFrame contenant les données à analyser. Par défaut, il utilise `data_final`.
    Retourne:
    --------
    DataFrame
        Un DataFrame avec une colonne supplémentaire 'Cluster' indiquant le cluster attribué à chaque ligne.
    Variables utilisées pour le clustering:
    ---------------------------------------
    - Age
    - Niveau d'etude
    - Genre
    """
    
    cible_clust = 'ÉLIGIBILITÉ AU DON.'
    vars_clust = ["Age","Niveau d'etude", 'Genre', 'Situation Matrimoniale (SM)','Profession',
                'Arrondissement de résidence', 'Religion', 'A-t-il (elle) déjà donné le sang',
                'Quartier de Résidence']
    data_cluster = data[vars_clust]

    df = data_cluster

    numeric_features = ['Age', 'Profession', 'Quartier de Résidence']
    categorical_features = ['Genre', 'Situation Matrimoniale (SM)', 
                            'Religion',"Niveau d'etude", 'A-t-il (elle) déjà donné le sang']  ##'Arrondissement de résidence', 

    # Appliquer la transformation aux variables catégorielles(car vue leur dimensionnalite par 
    # rapport a la base peuvent etre assimille a des distribution continu)
    data_cluster['Quartier de Résidence'] = calculate_probabilities(data_cluster, 'Quartier de Résidence')
    data_cluster['Profession'] = calculate_probabilities(data_cluster, 'Profession')
    
    # Prétraitement des données
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # Création du pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('svd', TruncatedSVD(n_components=10)), 
        ('clustering', KMeans(n_clusters=4, random_state=42)) 
    ])

    pipeline.fit(df)
    df['Cluster'] = pipeline.named_steps['clustering'].labels_
    return df

