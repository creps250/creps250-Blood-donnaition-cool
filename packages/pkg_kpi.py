from prossess_data.prossess import data_final
import pandas as pd


# Age moyen des personnes eligibiles
def age_moyen_eligible(df):
    return df['age'].mean()



#le nombre d'arrondisssement
def nombre_arrondissement(df):
    return df['Arrondissement de résidence'].nunique()

 #total de quartiers 
def total_quartiers(df): 
    return df['Quartier de Résidence'].nunique()


#total d'enquetés

def total_enquetes(df):
    return len(df)


# Age moyen des personnes eligibiles
def age_moyen_elig(df):
    return round(df[df['ÉLIGIBILITÉ AU DON.'] == 'Eligible']['Age'].mean())

# Age moyen des personnes ayabnt deja donnee
def age_moyen_don(df):
    return round(df[df['A-t-il (elle) déjà donné le sang']=='Oui']['Age'].mean())



#pourcentage d'eligibilité

def pourcentage_eligibilite(df):
    return round((len(df[df['ÉLIGIBILITÉ AU DON.'] == 'Eligible']) / len(df)) * 100,2)


# taux de dons
def taux_don(df):
    return round((len(df[df['A-t-il (elle) déjà donné le sang']=='Oui']) *100 / len(df)),2)



def calculer_taux_croissance_annuels(data_don):
    """
    Calcule les taux de croissance annuels et retourne les valeurs maximales de croissance et l'année correspondante.

    Cette fonction prend en entrée un DataFrame contenant les informations sur les dons de sang par année,
    calcule les taux de croissance annuels et retourne les valeurs maximales de croissance et l'année correspondante.

    Paramètres:
    data_don_annee (pandas.DataFrame): Le DataFrame contenant les informations sur les dons de sang par année.

    Retourne:
    tuple: Un tuple contenant la valeur maximale de croissance et l'année correspondante.
    """
    
    data_don_annee = data_don['Annee'].value_counts().reset_index().sort_values(by='Annee')
    # Calculer les taux de croissance annuels
    data_don_annee.set_index('Annee', inplace=True)
    data_don_annee['Taux de croissance (%)'] = data_don_annee['count'].pct_change() * 100

    # Afficher le dataframe avec les taux de croissance
    max_growth = data_don_annee['Taux de croissance (%)'].max()
    max_growth_year = data_don_annee['Taux de croissance (%)'].idxmax()
    
    return round(max_growth,1), max_growth_year



def compter_dons_par_mois(data_don):
    """
    Compte le nombre de dons par mois et calcule les taux de croissance mensuels.

    Cette fonction prend en entrée un DataFrame contenant les informations sur les dons de sang,
    compte le nombre de dons pour chaque mois, trie les mois dans l'ordre chronologique et calcule
    les taux de croissance mensuels. Elle retourne le DataFrame avec les taux de croissance et les
    valeurs maximales de croissance et le mois correspondant.

    Paramètres:
    data_don (pandas.DataFrame): Le DataFrame contenant les informations sur les dons de sang.

    Retourne:
    tuple: Un tuple contenant le DataFrame avec les taux de croissance et les valeurs maximales de croissance et le mois correspondant.
    """
    # Compter le nombre de dons par mois
    data_don_mois = data_don['Mois'].value_counts().reset_index()
    data_don_mois.columns = ['Mois', 'count']

    # Trier les mois dans l'ordre chronologique
    mois_ordre = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    data_don_mois['Mois'] = pd.Categorical(data_don_mois['Mois'], categories=mois_ordre, ordered=True)
    data_don_mois = data_don_mois.sort_values('Mois')

    # Calculer les taux de croissance mensuels
    data_don_mois['Taux de croissance (%)'] = data_don_mois['count'].pct_change() * 100

    # Afficher le DataFrame avec les taux de croissance
    data_don_mois.set_index('Mois', inplace=True)

    # Retourner les valeurs maximales de croissance et le mois correspondant
    max_growth = data_don_mois['Taux de croissance (%)'].max()
    max_growth_month = data_don_mois['Taux de croissance (%)'].idxmax()

    return  round(max_growth,1), max_growth_month

