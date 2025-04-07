import pandas as pd
from prossess_data.prossess import data_final

data = data_final.copy()
a = (pd.to_datetime(data['Date de remplissage de la fiche']).dt.year - pd.to_datetime(data['Date de naissance']).dt.year)
data['Age']=a.values
#### data dont
data_don =  data[data['Date de remplissage de la fiche'].notna()]

data_don = data_don[pd.to_datetime(data_don['Date de remplissage de la fiche'],'coerce').notna()].\
        rename(columns={'Date de remplissage de la fiche':'date dernier don'})
data_don['date dernier don'] = pd.to_datetime(data_don['date dernier don'])
data_don['Annee'] = data_don['date dernier don'].dt.year
data_don = data_don[data_don['Annee']==2019]
data_don['Mois'] = data_don['date dernier don'].dt.month_name()


# Remplacer les valeurs aberrantes par la médiane de l'âge
median_age = data_don['Age'].median()
data_don['Age'] = data_don['Age'].apply(lambda x: median_age if x <= 0 or x > 100 else x)

# Créer des classes d'âge
bins = [0, 20, 30, 40, 50, 60]
#, 70, 80, 90, 100
labels = ['0-20', '21-30', '31-40', '41-50', '51-60']

#, '61-70', '71-80', '81-90', '91-100'
data_don['Age_Class'] = pd.cut(data_don['Age'], bins=bins, labels=labels, right=False)

##############################



######################profiling

data_cluster_don = data_don[['Genre',"Niveau d'etude",'ÉLIGIBILITÉ AU DON.','Religion','Age_Class','Situation Matrimoniale (SM)','Annee','Mois']]  



##data dont annees
data_don_annee = data_don['Annee'].value_counts().reset_index().sort_values(by='Annee')
data_don_annee.columns = ['Annee', 'count']
####
categorie = ['January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December']
data_don_mois = data_don['Mois'].value_counts().reset_index()
data_don_mois.columns = ['Mois', 'count']



