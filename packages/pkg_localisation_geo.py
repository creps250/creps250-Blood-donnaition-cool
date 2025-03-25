import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots
import geopandas as gpd
import time
from geopy.geocoders import Nominatim
import pandas as pd
import folium
from prossess_data.process_temporelle import data_final
from branca.element import Figure

### import data
path = "dataset/DD.shp"
#Ouverture du geodataframe
douala_gdf = gpd.read_file(path, encoding='utf-8')
douala_json = douala_gdf.to_json()

###>>>> first process
douala_gdf['NOM'] = douala_gdf['NOM'].replace({'Douala IV': 'douala 4',
                                                             "Douala II":"douala 2",
                                                             "Douala I":"douala 1",
                                                             "Douala III":"douala 3",
                                                             "Douala V":"douala 5"})

 
data = pd.read_excel("dataset/data.xlsx", sheet_name = "2019")
quartiers_uniques = data["dr"].unique() 
qtrs = pd.read_csv("dataset/coordonnees_quartiers2.csv")


qtrs = qtrs.dropna() # supprimer pour le moment les quartiers dont on a pas trouver les coordonnées 

resultat = pd.merge(data, qtrs, left_on='dr', right_on='Quartier', how='inner')

df = resultat.dropna(subset=['Longitude'])

#####process fort
douala = data[data["Arrondissement de résidence"].isin(['douala 3', 'douala 2',"douala 1","douala 4","douala 5"])]
Q = douala["Arrondissement de résidence"].value_counts()/douala.shape[0]*100
df_Q = Q.reset_index()
df_Q.columns = ['commune', 'Prop Candidats aux dons']
communes = pd.merge(douala_gdf, df_Q, left_on='NOM', right_on='commune', how='left')


#######
F = data["dr"].value_counts()/data.shape[0]*100
df_F = F.reset_index()
df_F.columns = ['Quartier', 'Prop Candidats aux dons']

################################################
coord_quart = pd.merge(qtrs,df_F, left_on='Quartier', right_on='Quartier', how='left')
quartiers = pd.merge(data,df_F, left_on='dr', right_on='Quartier', how='left')

vars = ["Niveau d'etude", 'Genre', 'Situation Matrimoniale (SM)', 'cat_profession', 
        'A-t-il (elle) déjà donné le sang', 'ÉLIGIBILITÉ AU DON.']

df_list = []  # Liste pour stocker les DataFrames temporairement

for var in vars:
    df_temp = douala.groupby(['Arrondissement de résidence', var]).size().unstack(fill_value=0)
    df_temp.reset_index(inplace=True)
    df_list.append(df_temp)

# Fusionner tous les DataFrames sur 'Arrondissement de résidence'
df2 = df_list[0]
for df in df_list[1:]:
    df2 = pd.merge(df2, df, on='Arrondissement de résidence', how='left')

# Fusion avec la table 'communes', en ajoutant un suffixe aux colonnes en conflit
communes = pd.merge(df2, communes, left_on='Arrondissement de résidence', right_on='commune', how='left', suffixes=('', '_commune'))

# Supprimer la colonne en double 'commune' si elle existe
if 'commune' in communes.columns:
    communes.drop(columns=['commune'], inplace=True)
    
    
################################################
vars = ["Niveau d'etude", 'Genre', 'Situation Matrimoniale (SM)', 'cat_profession', 
        'A-t-il (elle) déjà donné le sang', 'ÉLIGIBILITÉ AU DON.']

df_list = []  # Liste pour stocker les DataFrames temporairement

for var in vars:
    df_temp = data.groupby(['dr', var]).size().unstack(fill_value=0)
    df_temp.reset_index(inplace=True)
    df_list.append(df_temp)

# Fusionner tous les DataFrames sur 'Arrondissement de résidence'
df2 = df_list[0]
for df in df_list[1:]:
    df2 = pd.merge(df2, df, on='dr', how='left')

# Fusion avec la table 'communes', en ajoutant un suffixe aux colonnes en conflit
coord_quart = pd.merge(df2, coord_quart, left_on='dr', right_on='Quartier', how='left', suffixes=('', '_Quartier'))

# Supprimer la colonne en double 'commune' si elle existe
if 'Quartier' in coord_quart.columns:
    coord_quart.drop(columns=['Quartier'], inplace=True)
    
    
    

#######################################################################

geojson_data = douala_gdf.__geo_interface__
# Création de la carte choroplèthe avec Plotly

##>>> first map
def Carte_arrondissement(data_name,variable_name,label_name,legend_name,titre) :
    """
    Génère une carte choroplèthe des arrondissements de Douala avec des données géographiques et des variables spécifiques.
    Paramètres:
    -----------
    data_name : DataFrame
        Le DataFrame contenant les données à visualiser.
    variable_name : str
        Le nom de la colonne dans le DataFrame contenant les valeurs numériques pour la coloration.
    label_name : str
        Le nom de la colonne dans le DataFrame contenant les noms des arrondissements à afficher en survol.
    legend_name : str
        Le nom à afficher dans la légende pour la variable colorée.
    titre : str
        Le titre de la carte.
    Retourne:
    ---------
    fig : plotly.graph_objs._figure.Figure
        La figure Plotly représentant la carte choroplèthe.
    """
        

    fig = px.choropleth_mapbox(
        data_name,
        geojson=geojson_data,
        locations=communes.index,  # Utilisation de l'index comme identifiant
        color=variable_name,  # La variable numérique utilisée pour la coloration
        hover_name=label_name,  # Nom des arrondissements affiché en survol
        color_continuous_scale="Viridis",  # Palette de couleurs pour la carte
        mapbox_style="carto-positron",  # Style de fond de carte
        center={"lat": 4.05, "lon": 9.7},  # Coordonnées centrales pour Douala
        zoom=11,  # Niveau de zoom initial
        labels={variable_name: legend_name}  # Légende pour la variable
    )
    # Mise en page de la carte
    fig.update_layout(
        title=titre,
        margin={"r": 0, "t": 26, "l": 0, "b": 0},font=dict(size=10)
    )
    # Affichage de la carte
    return fig
# Appel de la fonction
######  Carte_arrondissement(data_name=communes,variable_name="Prop Candidats aux dons",titre="Proportion des candidats aux dons",label_name='Arrondissement de résidence',legend_name="donnateurs")

##>>> two map
def cartographie_quartier(var1="Temporairement Non-eligible",var2 ="Eligible" ):
    """
    Génère une carte scatter mapbox visualisant la distribution des enquêtes par quartier.
    Cette fonction crée une carte scatter mapbox en utilisant Plotly Express, où chaque point 
    représente un quartier avec ses coordonnées de latitude et de longitude. La couleur des points 
    représente le nombre de femmes, et la taille des points représente le nombre d'hommes. La carte 
    utilise l'échelle de couleurs 'IceFire' et le style 'open-street-map'.
    Retourne:
        plotly.graph_objs._figure.Figure: Un objet figure Plotly contenant la carte scatter mapbox.
    """

    fig = px.scatter_mapbox(coord_quart, lat="Latitude", lon="Longitude",color=var1, size=var2,
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=10,hover_name="dr")
    fig.update_traces(text=coord_quart["dr"], textposition="top center")
    fig.update_layout(mapbox_style="open-street-map",margin=dict(t=30,l=0,r=0,b=0),
                    title='Cartographie des enquetes par quartier')

    return fig
 
  



#####Repartition quartier
def repartition_donneurs_sang(data=data_final,var_='A-t-il (elle) déjà donné le sang',title='Répartition des donneurs de sang'):
    """
    Crée un graphique en camembert avec trous pour visualiser la répartition des donneurs de sang.

    Ce graphique est un camembert avec trous qui montre la répartition des donneurs de sang d'après la variable
    `var_` dans le DataFrame `data`. La taille de chaque partie du camembert est proportionnelle au nombre de
    personnes qui ont la valeur correspondante pour la variable `var_`. La couleur est définie en fonction de
    la valeur de la variable.

    La légende est affichée horizontalement en bas du graphique. Le graphique est centré horizontalement et
    a une marge de 30 pixels en haut, et de 0 pixel sur les autres côtés.

    Paramètres:
    data (pandas.DataFrame): Le DataFrame contenant les données à visualiser.
    var_ (str): Le nom de la colonne du DataFrame contenant les valeurs à visualiser.
    title (str): Le titre du graphique.

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le graphique en camembert.
    """
    elegibilite_counts = data[var_].value_counts().reset_index()
    elegibilite_counts.columns = [var_, 'Total']

    # Créer un graphique en camembert avec trous
    fig0 = px.pie(elegibilite_counts, values='Total', names=var_, hole=0.5, 
                title=title)
                # Séparer une partie du camembert
    fig0.update_traces(pull=[0.1 if i == 1 else 0 for i in range(len(elegibilite_counts))],rotation=90)
    fig0.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30,l=0,r=0,b=0)
        )
    fig0.update_traces(marker_line_color='black',opacity=1,marker_line_width=1)
    return fig0

def return_stat_enqueteur(data=data_final):
    # Create a figure with two subplots
    """
    Crée un graphique avec deux sous-parcelles pour visualiser la répartition des enquêtés selon la nationalité
    et par don de sang.

    Ce graphique est composé de deux camemberts avec trous qui montrent la répartition des enquêtés selon la
    nationalité et selon s'ils ont déjà donné du sang ou non. La taille de chaque partie du camembert est
    proportionnelle au nombre de personnes qui ont la valeur correspondante pour la variable.

    La légende est affichée horizontalement en bas du graphique. Le graphique est centré horizontalement et
    a une marge de 30 pixels en haut, et de 0 pixel sur les autres côtés.

    Paramètres:
    data (pandas.DataFrame): Le DataFrame contenant les données à visualiser.

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le graphique avec deux sous-parcelles.
    """
    fig = make_subplots(rows=1, cols=2, vertical_spacing=0.02,horizontal_spacing=0.01,
                        specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        )

    # Add the first pie chart to the first subplot
    fig.add_trace(
        repartition_donneurs_sang(data=data,var_='Nationalité').data[0],
        row=1, col=1
    )

    # Add the second pie chart to the second subplot
    fig.add_trace(
        repartition_donneurs_sang(data=data,var_='A-t-il (elle) déjà donné le sang').data[0],
        row=1, col=2
    )

    # Update layout
    fig.update_layout(
        title = "Répartition des enquêtés selon la nationalité et par don de sang",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30, l=0, r=0, b=0),
        font=dict(size=10)
    )

    # Show the figure
    return fig

 

####>>>>tree graphs
def Etude_repartition_var_dem(data=data_final,var_='Arrondissement de résidence',title='Repartition des Arrondissemnt'):

    """
    Crée un graphique en barres empilées pour visualiser la répartition des enquêtés
    selon une variable de choix (par exemple l'arrondissement de résidence) et
    par don de sang.

    Ce graphique est composé de barres empilées qui montrent la répartition des
    enquêtés selon la variable de choix et selon s'ils ont déjà donné du sang ou
    non. La taille de chaque partie de la barre est proportionnelle au nombre de
    personnes qui ont la valeur correspondante pour la variable.

    La légende est affichée horizontalement en bas du graphique. Le graphique est
    centré horizontalement et a une marge de 30 pixels en haut, et de 0 pixel sur
    les autres côtés.

    Paramètres:
    data (pandas.DataFrame): Le DataFrame contenant les données à visualiser.
    var_ (str): La colonne du DataFrame qui contient la variable à visualiser.
    title (str): Le titre du graphique.

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le
    graphique en barres empilées.
    """
    var_effectif = data[[var_,'A-t-il (elle) déjà donné le sang']].value_counts().to_frame().reset_index()

    fig2 = px.bar(var_effectif.sort_values(by='count'),
                y=var_, color_discrete_map={'Oui': 'orange', 'Non': 'blue'},
                x='count',
                color='A-t-il (elle) déjà donné le sang', barmode='stack',
                title=title,
                labels={var_: var_, 'count': 'Effectifs'},orientation='h',text_auto=True)

    fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    # Mettre à jour la mise en page
    fig2.update_layout(yaxis_title='',
                    xaxis_title='',
                    legend_title='as t il Deja donnee du sang :', margin=dict(t=30,l=0,r=0,b=0),
                    xaxis_tickangle=-45,
                    xaxis=dict(showgrid=False,title="",showticklabels=False))
    fig2.update_traces(marker_line_color='black',opacity=1,marker_line_width=1)
    # Afficher le graphique
    return fig2
 

#### >>>>four graphs 
def classe_age_plot(data=data_final):
    # Définir les bornes des classes d'âge
    """
    Crée un graphique à barres montrant la répartition des classes d'âge.

    Ce graphique est un barplot utilisant Plotly pour visualiser la répartition des classes d'âge
    dans le DataFrame. Les classes d'âge sont définies en fonction de la variable 'Age'.
    La taille de chaque barre est proportionnelle au nombre de personnes qui ont la valeur
    correspondante pour la variable.

    La légende est affichée horizontalement en bas du graphique. Le graphique est
    centré horizontalement et a une marge de 30 pixels en haut, et de 0 pixel sur
    les autres côtés.

    Les couleurs sont définies pour les deux valeurs de la variable 'A-t-il (elle) déjà donné le sang' :
    'Oui' est représenté en orange et 'Non' en bleu.

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le graphique en barres.
    """
    a = (pd.to_datetime(data['Date de remplissage de la fiche']).dt.year - pd.to_datetime(data['Date de naissance']).dt.year)
    data['Age'] = a.values
    
    bins = [0, 19, 29, 39, 49, 59, 69, 200]  # Corrigé la dernière borne à 69 pour correspondre à '60-69'
    labels = ['<=19', '20-29', '30-39', '40-49', '50-59', '60-69', '>=70']  # Corrigé à '>=70' pour être cohérent
    
    # Créer une nouvelle colonne 'Classe_Age' avec les classes d'âge
    data['Classe_Age'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)
    
    # Créer un DataFrame pour le comptage
    classe_counts = data.groupby(['Classe_Age', 'A-t-il (elle) déjà donné le sang']).size().reset_index(name='count')
    
    # Créer le graphique avec plotly express
    fig = px.bar(
        classe_counts, 
        x='Classe_Age', 
        y='count',
        color='A-t-il (elle) déjà donné le sang', 
        barmode='group',  # Utilisez 'group' pour des barres côte à côte ou 'stack' pour des barres empilées
        text_auto=True,
        title='Répartition des classes d\'âge des candidats aux dons',
        labels={'count': 'Nombre de personnes', 'Classe_Age': 'Classe d\'âge'},
        color_discrete_map={'Oui': 'orange', 'Non': 'blue'}
    )
    
    fig.update_traces(marker_line_color='black',opacity=1,marker_line_width=1)
    
    # Mise à jour du layout
    fig.update_layout(
        margin=dict(t=30, l=0, r=8, b=0),
        yaxis=dict(showgrid=False, title="Effectifs"),
        xaxis_title = '',
        font=dict(size=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig
 
 
 
####>>>>sankey card
def create_blood_donation_sankey(data=data_final):
    # Créer une copie des données pour éviter de modifier l'original
    """
    Crée un diagramme Sankey pour visualiser la répartition des dons de sang par arrondissement de résidence.

    Cette fonction utilise les données fournies pour générer un diagramme Sankey, qui illustre la relation
    entre le fait d'avoir déjà donné du sang et l'arrondissement de résidence des participants. Les flux
    dans le diagramme montrent le nombre de personnes répondant "Oui" ou "Non" à la question de don de sang
    pour chaque arrondissement.

    Paramètres:
    data (pandas.DataFrame): Le DataFrame contenant les données à analyser. Par défaut, il utilise `data_final`.

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet Figure contenant le diagramme Sankey représentant la répartition
    des dons de sang selon les arrondissements de résidence.
    """

    df = data[['A-t-il (elle) déjà donné le sang', 'Arrondissement de résidence']].copy()
    
    # Renommer les colonnes pour plus de clarté
    df.columns = ['Don_de_sang', 'Arrondissement']
    
    # S'assurer qu'il n'y a pas de valeurs manquantes
    df = df.dropna()
    
    # Compter les occurrences de chaque combinaison
    sankey_data = df.groupby(['Don_de_sang', 'Arrondissement']).size().reset_index(name='count')
    
    # Créer des listes sources, targets et values pour le diagramme Sankey
    # Créer d'abord une liste unique de tous les nœuds
    don_de_sang_options = sankey_data['Don_de_sang'].unique().tolist()
    arrondissements = sankey_data['Arrondissement'].unique().tolist()
    
    # Créer un dictionnaire pour mapper les noms de nœuds à des indices
    labels = don_de_sang_options + arrondissements
    node_indices = {name: i for i, name in enumerate(labels)}
    
    # Créer les listes sources, targets et values
    sources = []
    targets = []
    values = []
    
    for _, row in sankey_data.iterrows():
        source_idx = node_indices[row['Don_de_sang']]
        target_idx = node_indices[row['Arrondissement']]
        sources.append(source_idx)
        targets.append(target_idx)
        values.append(row['count'])
    
    # Préparer les couleurs pour les liens
    # Rose pour "Oui" et gris clair pour "Non"
    link_colors = []
    for source in sources:
        if labels[source] == 'Oui':
            link_colors.append('rgba(255, 182, 193, 0.8)')  # Rose pour "Oui"
        else:
            link_colors.append('rgba(211, 211, 211, 0.8)')  # Gris clair pour "Non"
    
    # Préparer les couleurs pour les nœuds
    node_colors = []
    for label in labels:
        if label == 'Oui':
            node_colors.append('rgba(255, 105, 180, 0.8)')  # Rose vif pour le nœud "Oui"
        elif label == 'Non':
            node_colors.append('rgba(169, 169, 169, 0.8)')  # Gris pour le nœud "Non"
        else:
            node_colors.append('rgba(0, 123, 255, 0.8)')    # Bleu pour les arrondissements
    
    # Créer le diagramme Sankey
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors
        )
    ))
    
    # Mettre à jour la mise en page
    fig.update_layout(
        title_text="Repartition du don de sang par arrondissement de résidence",
        font=dict(size=10),
        autosize=True,
        margin=dict(l=25, r=25, t=50, b=25),
    )
    
    return fig



def CarteFolium(df, var1, var2,douala_gdf=douala_gdf):
    # Supprimer les lignes avec des NaN dans Latitude ou Longitude
    """
    Crée une carte Folium avec des marqueurs pour chaque quartier avec le nombre de femmes et d'hommes,
    ainsi qu'un cercle pour les éligibles.
    """
    
    coord_quart_cleaned = df.dropna(subset=['Latitude', 'Longitude'])
    
    # Créer une carte centrée sur les coordonnées moyennes
    m = folium.Map(location=[coord_quart_cleaned["Latitude"].mean(), coord_quart_cleaned["Longitude"].mean()], zoom_start=10)

    # Ajouter des marqueurs pour chaque point de données
    for _, row in coord_quart_cleaned.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"dr: {row['dr']}<br>Homme: {row[var1]}<br>Femme: {row[var2]}",
            tooltip=row["dr"]
        ).add_to(m)
        
        # Cercle pour "Eligible"
        folium.Circle(
            location=[row['Latitude'], row['Longitude']],
            radius=row[var1],  # Ajuster la taille
            color="green",
            fill=True,
            fill_color="red",
            fill_opacity=1,
            tooltip=f"{row[var2]} éligibles"
        ).add_to(m)

    # Définir le CRS pour douala_gdf AVANT de l'utiliser dans Choropleth
    # Assurez-vous que cette variable est définie dans votre scope ou passée en argument
    
    # Définir le CRS (WGS84 est standard pour les cartes web)
    douala_gdf.crs = "EPSG:4326"  
    
    # Maintenant vous pouvez l'utiliser dans Choropleth
    polygone = folium.Choropleth(geo_data=douala_gdf)
    polygone.add_to(m)
    
    return m._repr_html_()

# appel de la fonction
###   CarteFolium(coord_quart,"Femme","Homme")
