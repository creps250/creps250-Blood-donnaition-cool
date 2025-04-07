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

# Dictionnaire de traduction pour ce module
GRAPH_TRANSLATIONS = {
    'fr': {
        "Proportion des candidats aux dons": "Proportion des candidats aux dons",
        "donnateurs": "donnateurs",
        "Répartition des donneurs de sang par Arrondissement de résidence": "Répartition des donneurs de sang par Arrondissement de résidence",
        "Répartition des enquêtés selon la nationalité et par don de sang": "Répartition des enquêtés selon la nationalité et par don de sang",
        "Cartographie des enquetes par quartier": "Cartographie des enquetes par quartier",
        "Repartition du": "Repartition du",
        "des donneurs de sang": "des donneurs de sang",
        "Répartition des classes d'âge des candidats aux dons": "Répartition des classes d'âge des candidats aux dons",
        "Nombre de personnes": "Nombre de personnes",
        "Classe d'âge": "Classe d'âge",
        "Effectifs": "Effectifs"
    },
    'en': {
        "Proportion des candidats aux dons": "Proportion of donation candidates",
        "donnateurs": "donors",
        "Répartition des donneurs de sang par Arrondissement de résidence": "Distribution of blood donors by residence district",
        "Répartition des enquêtés selon la nationalité et par don de sang": "Distribution of surveyed people by nationality and blood donation",
        "Cartographie des enquetes par quartier": "Mapping of surveys by neighborhood",
        "Repartition du": "Distribution of",
        "des donneurs de sang": "of blood donors",
        "Répartition des classes d'âge des candidats aux dons": "Age group distribution of donation candidates",
        "Nombre de personnes": "Number of people",
        "Classe d'âge": "Age group",
        "Effectifs": "Numbers"
    }
}


def hex_to_rgba(hex_color, alpha=1.0):
    """
    Convertit une couleur hexadécimale en format rgba pour pouvoir définir la transparence.
    
    Args:
        hex_color (str): Couleur au format hexadécimal (ex: '#RRGGBB')
        alpha (float): Valeur de transparence entre 0 et 1
        
    Returns:
        str: Couleur au format rgba
    """
    # S'assurer que la couleur est au bon format
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # Convertir en RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Retourner au format rgba
    return f'rgba({r}, {g}, {b}, {alpha})'
 
BLOOD_PALETTE = {
    'primary': ['#9C0824', '#B71C1C', '#D32F2F', '#EF5350', '#FFCDD2'],  # Rouge sang profond à pâle
    'secondary': ['#1A237E', '#303F9F', '#5C6BC0', '#9FA8DA', '#E8EAF6'],  # Bleu médical
    'accent': ['#004D40', '#00796B', '#26A69A', '#80CBC4', '#E0F2F1'],    # Teinte turquoise
    'neutral': ['#212121', '#424242', '#757575', '#BDBDBD', '#EEEEEE'],   # Tons gris
    'warm': ['#BF360C', '#E64A19', '#FF7043', '#FFAB91', '#FBE9E7'],      # Oranges chauds
    'gradient_warm': ['#BF360C', '#D84315', '#E64A19', '#F4511E', '#FF5722', '#FF7043', '#FF8A65', '#FFAB91'],
    'gradient_cool': ['#1A237E', '#283593', '#303F9F', '#3949AB', '#3F51B5', '#5C6BC0', '#7986CB', '#9FA8DA'],
    'categorical': ['#9C0824', '#1A237E', '#004D40', '#BF360C', '#6A1B9A', '#00838F', '#558B2F', '#FF6F00']
}

# Palettes adaptées au thème (clair/sombre)
THEME_ADAPTIVE_PALETTES = {
    'light': {
        'background': '#FFFFFF',
        'cardBackground': '#F5F5F5',
        'text': '#212121',
        'gridLines': '#E0E0E0',
        'highlight': '#B71C1C',
        'mapBackground': 'carto-positron'
    },
    'dark': {
        'background': '#121212',
        'cardBackground': '#1E1E1E',
        'text': '#FFFFFF',
        'gridLines': '#424242',
        'highlight': '#EF5350',
        'mapBackground': 'carto-darkmatter'
    }
}

def get_theme_colors(theme='light'):
    """Retourne les couleurs adaptées au thème spécifié."""
    return THEME_ADAPTIVE_PALETTES[theme]



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
def Carte_arrondissement(data_name, variable_name, label_name, legend_name, titre, language="fr"): 
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
    language : str
        La langue dans laquelle le titre doit être affiché ("fr" ou "en").
    Retourne:
    ---------
    fig : plotly.graph_objs._figure.Figure
        La figure Plotly représentant la carte choroplèthe.
    """
    # Traduire le titre et la légende
    translated_title = GRAPH_TRANSLATIONS[language].get(titre, titre)
    translated_legend = GRAPH_TRANSLATIONS[language].get(legend_name, legend_name)
    
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
        labels={variable_name: translated_legend}  # Légende pour la variable
    )
    # Mise en page de la carte
    fig.update_layout(
        title=translated_title,
        margin={"r": 0, "t": 26, "l": 0, "b": 0},
        font=dict(size=10)
    )
    # Affichage de la carte
    return fig

##>>> two map
def cartographie_quartier(var1="Temporairement Non-eligible", var2="Eligible", language="fr"):
    """
    Génère une carte scatter mapbox visualisant la distribution des enquêtes par quartier.
    Cette fonction crée une carte scatter mapbox en utilisant Plotly Express, où chaque point 
    représente un quartier avec ses coordonnées de latitude et de longitude. La couleur des points 
    représente le nombre de femmes, et la taille des points représente le nombre d'hommes. La carte 
    utilise l'échelle de couleurs 'IceFire' et le style 'open-street-map'.
    
    Args:
        var1 (str): Variable à utiliser pour la couleur des points. Par défaut "Temporairement Non-eligible".
        var2 (str): Variable à utiliser pour la taille des points. Par défaut "Eligible".
        language (str): Langue pour les titres ("fr" ou "en").
        
    Retourne:
        plotly.graph_objs._figure.Figure: Un objet figure Plotly contenant la carte scatter mapbox.
    """
    # Traduire le titre
    map_title = "Cartographie des enquetes par quartier"
    translated_title = GRAPH_TRANSLATIONS[language].get(map_title, map_title)

    fig = px.scatter_mapbox(coord_quart, lat="Latitude", lon="Longitude", color=var1, size=var2,
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=10, hover_name="dr")
    fig.update_traces(text=coord_quart["dr"], textposition="top center")
    fig.update_layout(mapbox_style="open-street-map", margin=dict(t=30, l=0, r=0, b=0),
                    title=translated_title)

    return fig
 
  
#####Repartition quartier
def repartition_donneurs_sang(data=data_final, var_='A-t-il (elle) déjà donné le sang', 
                            title='Répartition des donneurs de sang', language="fr"):
    """
    Crée un graphique en camembert avec trous professionnellement stylisé pour visualiser la répartition des donneurs de sang.

    Ce graphique est un camembert avec trous qui montre la répartition des donneurs de sang d'après la variable
    `var_` dans le DataFrame `data`. La taille de chaque partie du camembert est proportionnelle au nombre de
    personnes qui ont la valeur correspondante pour la variable `var_`. Les couleurs s'adaptent au thème actuel de l'application.

    Paramètres:
    -----------
    data : pandas.DataFrame
        Le DataFrame contenant les données à visualiser.
    var_ : str
        Le nom de la colonne du DataFrame contenant les valeurs à visualiser.
    title : str
        Le titre du graphique.
    language : str
        La langue de l'interface ("fr" ou "en").

    Retourne:
    ---------
    plotly.graph_objs._figure.Figure
        Un objet figure Plotly représentant le graphique en camembert amélioré.
    """
    # Déterminer le thème actuel basé sur les couleurs de fond globales
    # On peut utiliser cette approche car la couleur de fond est un bon indicateur du thème
    is_dark_theme = False
    try:
        # Cette méthode tente de détecter le thème à partir de l'environnement global
        import dash
        if dash.callback_context.inputs is not None:
            # Si nous sommes dans un contexte de callback
            ctx = dash.callback_context
            if 'theme-store.data' in ctx.inputs:
                is_dark_theme = ctx.inputs['theme-store.data'] == 'dark'
            else:
                # Fallback: utiliser une détection sur les couleurs typiques du thème sombre
                import plotly.io as pio
                current_template = pio.templates.default
                is_dark_theme = 'plotly_dark' in current_template or 'darkly' in current_template
    except:
        # Si une erreur se produit, on utilise une estimation basée sur les constantes THEME_ADAPTIVE_PALETTES
        # qui sont probablement définies dans le fichier
        is_dark_theme = False  # Utiliser le thème clair par défaut
    
    # Récupérer les couleurs du thème
    theme_colors = get_theme_colors('dark' if is_dark_theme else 'light')
    
    # Traduire le titre
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Préparer les données
    elegibilite_counts = data[var_].value_counts().reset_index()
    elegibilite_counts.columns = [var_, 'Total']
    
    # Calculer le total pour le texte au centre
    total = elegibilite_counts['Total'].sum()
    
    # Déterminer les couleurs en fonction du thème et du nombre de catégories
    num_categories = len(elegibilite_counts)
    
    if is_dark_theme:
        # Utiliser une palette de couleurs adaptée au thème sombre
        if 'A-t-il (elle) déjà donné le sang' in var_:
            # Couleurs spécifiques pour le don de sang (Rouge/Bleu)
            colors = [BLOOD_PALETTE['primary'][1], BLOOD_PALETTE['secondary'][1]]  
            if num_categories > 2:
                colors.extend([BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])] 
                            for i in range(2, num_categories)])
        elif 'ÉLIGIBILITÉ AU DON.' in var_:
            # Couleurs spécifiques pour l'éligibilité (Vert/Orange/Rouge)
            colors = [BLOOD_PALETTE['accent'][1], BLOOD_PALETTE['warm'][1], BLOOD_PALETTE['primary'][1]]
            if num_categories > 3:
                colors.extend([BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])] 
                            for i in range(3, num_categories)])
        else:
            # Palette générique avec des couleurs vives pour le thème sombre
            colors = [BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])] 
                    for i in range(num_categories)]
    else:
        # Utiliser une palette de couleurs adaptée au thème clair
        if 'A-t-il (elle) déjà donné le sang' in var_:
            # Couleurs spécifiques pour le don de sang (Rouge/Bleu) mais plus douces
            colors = [BLOOD_PALETTE['primary'][2], BLOOD_PALETTE['secondary'][2]]  
            if num_categories > 2:
                colors.extend([BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])] 
                            for i in range(2, num_categories)])
        elif 'ÉLIGIBILITÉ AU DON.' in var_:
            # Couleurs spécifiques pour l'éligibilité (Vert/Orange/Rouge) mais plus douces
            colors = [BLOOD_PALETTE['accent'][2], BLOOD_PALETTE['warm'][2], BLOOD_PALETTE['primary'][2]]
            if num_categories > 3:
                colors.extend([BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])] 
                            for i in range(3, num_categories)])
        else:
            # Palette générique avec des couleurs douces pour le thème clair
            colors = [hex_to_rgba(BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])], 0.8) 
                    for i in range(num_categories)]
    
    # Préparation des valeurs de 'pull' (extraction des segments du camembert)
    # Extraire le segment correspondant à "Oui" si c'est un camembert de don de sang
    pull_values = None
    if 'A-t-il (elle) déjà donné le sang' in var_:
        # Trouver l'index de "Oui" s'il existe
        try:
            yes_index = elegibilite_counts[elegibilite_counts[var_] == 'Oui'].index[0]
            pull_values = [0.1 if i == yes_index else 0 for i in range(num_categories)]
        except (IndexError, KeyError):
            # Par défaut extraire le premier segment
            pull_values = [0.1 if i == 0 else 0 for i in range(num_categories)]
    else:
        # Extraire le deuxième segment par défaut (maintient la compatibilité)
        pull_values = [0.1 if i == 1 else 0 for i in range(num_categories)]
    
    # Créer le graphique en camembert avec trous
    fig = go.Figure()
    
    # Ajouter le camembert
    fig.add_trace(go.Pie(
        labels=elegibilite_counts[var_],
        values=elegibilite_counts['Total'],
        hole=0.55,  # Trou légèrement plus grand pour un style plus moderne
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        insidetextfont=dict(
            color='white', 
            size=14,
            family='Arial, sans-serif'
        ),
        rotation=90,
        pull=pull_values,
        marker=dict(
            colors=colors,
            line=dict(
                color=theme_colors['text'], 
                width=1.5
            )
        ),
        textposition='auto',
        direction='clockwise'
    ))
    
    # Ajouter du texte au centre du camembert
    fig.add_annotation(
        text=f"<b>Total</b><br>{total}",
        x=0.5, y=0.5,
        font=dict(
            size=16, 
            color=theme_colors['text'],
            family='Arial, sans-serif'
        ),
        showarrow=False
    )
    
    # Ajouter un cercle décoratif autour du trou central
    fig.add_shape(
        type="circle",
        xref="paper", yref="paper",
        x0=0.41, y0=0.41, x1=0.59, y1=0.59,
        line=dict(
            color=hex_to_rgba(theme_colors['highlight'], 0.3),
            width=1.5
        ),
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Mettre à jour la mise en page
    fig.update_layout(
        title=dict(
            text=translated_title,
            x=0.5,
            font=dict(
                size=16,
                color=theme_colors['text'],
                family='Arial, sans-serif'
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent pour s'adapter à n'importe quel arrière-plan
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(
                color=theme_colors['text'],
                size=12,
                family='Arial, sans-serif'
            ),
            bgcolor='rgba(0,0,0,0)',  # Légende transparente
            bordercolor=hex_to_rgba(theme_colors['text'], 0.2),
            borderwidth=1
        ),
        margin=dict(t=30, l=20, r=20, b=0)
    )
    
    # Ajouter des effets avancés adaptés au thème
    if is_dark_theme:
        # Dans le thème sombre, ajouter un effet de lueur
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=0.3, y0=0.3, x1=0.7, y1=0.7,
            fillcolor="rgba(255, 255, 255, 0.05)",
            line=dict(width=0),
            layer="below"
        )
        
        # Ajouter un effet de "glossy" au camembert pour le thème sombre
        import numpy as np
        for i in range(num_categories):
            angle = (i / num_categories) * 2 * 3.14159  # Angle en radians
            gradient_x = 0.5 + 0.35 * np.cos(angle)
            gradient_y = 0.5 + 0.35 * np.sin(angle)
            
            fig.add_shape(
                type="circle",
                xref="paper", yref="paper",
                x0=gradient_x-0.05, y0=gradient_y-0.05,
                x1=gradient_x+0.05, y1=gradient_y+0.05,
                fillcolor=hex_to_rgba("#FFFFFF", 0.1),
                line=dict(width=0),
                layer="below"
            )
    else:
        # Dans le thème clair, ajouter une ombre subtile
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=0.31, y0=0.31, x1=0.69, y1=0.69,
            fillcolor="rgba(0, 0, 0, 0.05)",
            line=dict(width=0),
            layer="below"
        )
        
        # Ajouter un effet de reflet léger pour le thème clair
        fig.add_shape(
            type="rect",
            xref="paper", yref="paper",
            x0=0.3, y0=0.4, x1=0.7, y1=0.43,
            fillcolor=hex_to_rgba("#FFFFFF", 0.1),
            line=dict(width=0),
            layer="above"
        )
    
    return fig

def return_stat_enqueteur(data=data_final, language="fr"):
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
    language (str): La langue de l'interface ("fr" ou "en").

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le graphique avec deux sous-parcelles.
    """
    # Traduire le titre
    title = "Répartition des enquêtés selon la nationalité et par don de sang"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    fig = make_subplots(rows=1, cols=2, vertical_spacing=0.02, horizontal_spacing=0.01,
                        specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        )

    # Add the first pie chart to the first subplot
    fig.add_trace(
        repartition_donneurs_sang(data=data, var_='Nationalité', language=language).data[0],
        row=1, col=1
    )

    # Add the second pie chart to the second subplot
    fig.add_trace(
        repartition_donneurs_sang(data=data, var_='A-t-il (elle) déjà donné le sang', language=language).data[0],
        row=1, col=2
    )

    # Update layout
    fig.update_layout(
        title=translated_title,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30, l=0, r=0, b=0),
        font=dict(size=10)
    )

    # Show the figure
    return fig

 

####>>>>tree graphs
def Etude_repartition_var_dem(data=data_final, var_='Arrondissement de résidence', title='Repartition des Arrondissemnt', language="fr"):

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
    language (str): La langue de l'interface ("fr" ou "en").

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le
    graphique en barres empilées.
    """
    # Traduire le titre
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    var_effectif = data[[var_,'A-t-il (elle) déjà donné le sang']].value_counts().to_frame().reset_index()

    fig2 = px.bar(var_effectif.sort_values(by='count'),
                y=var_, color_discrete_map={'Oui': 'orange', 'Non': 'blue'},
                x='count',
                color='A-t-il (elle) déjà donné le sang', barmode='stack',
                title=translated_title,
                labels={var_: var_, 'count': 'Effectifs'}, orientation='h', text_auto=True)

    fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    # Mettre à jour la mise en page
    fig2.update_layout(yaxis_title='',
                    xaxis_title='',
                    legend_title='as t il Deja donnee du sang :', margin=dict(t=30, l=0, r=0, b=0),
                    xaxis_tickangle=-45,
                    xaxis=dict(showgrid=False, title="", showticklabels=False))
    fig2.update_traces(marker_line_color='black', opacity=1, marker_line_width=1)
    # Afficher le graphique
    return fig2
 

#### >>>>four graphs 
def classe_age_plot(data=data_final, language="fr"):
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
    
    Args:
        data (pandas.DataFrame): Le DataFrame contenant les données à analyser.
        language (str): La langue de l'interface ("fr" ou "en").

    Retourne:
    plotly.graph_objs._figure.Figure: Un objet figure Plotly représentant le graphique en barres.
    """
    # Traduire les titres et légendes
    title = "Répartition des classes d'âge des candidats aux dons"
    count_label = "Nombre de personnes"
    age_class_label = "Classe d'âge"
    effectifs_label = "Effectifs"
    
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    translated_count = GRAPH_TRANSLATIONS[language].get(count_label, count_label)
    translated_age_class = GRAPH_TRANSLATIONS[language].get(age_class_label, age_class_label)
    translated_effectifs = GRAPH_TRANSLATIONS[language].get(effectifs_label, effectifs_label)
    
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
        title=translated_title,
        labels={'count': translated_count, 'Classe_Age': translated_age_class},
        color_discrete_map={'Oui': 'orange', 'Non': 'blue'}
    )
    
    fig.update_traces(marker_line_color='black', opacity=1, marker_line_width=1)
    
    # Mise à jour du layout
    fig.update_layout(
        margin=dict(t=30, l=0, r=8, b=0),
        yaxis=dict(showgrid=False, title=translated_effectifs),
        xaxis_title='',
        font=dict(size=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig
 


####>>>>sankey card
def create_blood_donation_sankey(data=data_final, language="fr", theme='light'):
    """
    Crée un diagramme Sankey amélioré pour visualiser la répartition des dons de sang par arrondissement de résidence.
    
    Cette fonction utilise les données fournies pour générer un diagramme Sankey esthétique,
    qui illustre la relation entre le fait d'avoir déjà donné du sang et l'arrondissement de résidence.
    
    Paramètres:
    data (pandas.DataFrame): Le DataFrame contenant les données à analyser.
    language (str): La langue de l'interface ("fr" ou "en").
    theme (str): Le thème à utiliser ('light' ou 'dark').
    
    Retourne:
    plotly.graph_objs._figure.Figure: Un objet Figure contenant le diagramme Sankey amélioré.
    """
    # Récupérer les couleurs du thème
    theme_colors = get_theme_colors(theme)
    
    # Traduire le titre
    title = "Répartition des donneurs de sang par Arrondissement de résidence"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Préparer les données
    df = data[['A-t-il (elle) déjà donné le sang', 'Arrondissement de résidence']].copy()
    
    # Renommer les colonnes pour plus de clarté
    df.columns = ['Don_de_sang', 'Arrondissement']
    
    # S'assurer qu'il n'y a pas de valeurs manquantes
    df = df.dropna()
    
    # Compter les occurrences de chaque combinaison
    sankey_data = df.groupby(['Don_de_sang', 'Arrondissement']).size().reset_index(name='count')
    
    # Conserver uniquement les 8 principaux arrondissements pour éviter l'encombrement
    top_arrondissements = sankey_data.groupby('Arrondissement')['count'].sum().nlargest(8).index.tolist()
    
    # Agréger les autres arrondissements
    other_arrondissements = sankey_data[~sankey_data['Arrondissement'].isin(top_arrondissements)].copy()
    if not other_arrondissements.empty:
        other_sum = other_arrondissements.groupby('Don_de_sang')['count'].sum().reset_index()
        other_sum['Arrondissement'] = 'Autres'
        sankey_data = pd.concat([
            sankey_data[sankey_data['Arrondissement'].isin(top_arrondissements)],
            other_sum
        ])
    
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
    
    # Préparer les couleurs pour les nœuds
    node_colors = []
    for label in labels:
        if label == 'Oui':
            node_colors.append(BLOOD_PALETTE['primary'][1])  # Rouge pour "Oui"
        elif label == 'Non':
            node_colors.append(BLOOD_PALETTE['secondary'][1])  # Bleu pour "Non"
        elif label == 'Autres':
            node_colors.append(BLOOD_PALETTE['neutral'][2])  # Gris pour "Autres"
        else:
            # Dégradé de bleus pour les arrondissements
            idx = arrondissements.index(label) % len(BLOOD_PALETTE['gradient_cool'])
            node_colors.append(BLOOD_PALETTE['gradient_cool'][idx])
    
    # Préparer les couleurs pour les liens
    link_colors = []
    for source in sources:
        if labels[source] == 'Oui':
            # Dégradé de rouges pour les liens "Oui"
            link_colors.append(hex_to_rgba(BLOOD_PALETTE['primary'][1], 0.6))  # Rouge semi-transparent
        else:
            # Dégradé de bleus pour les liens "Non"
            link_colors.append(hex_to_rgba(BLOOD_PALETTE['secondary'][1], 0.6))  # Bleu semi-transparent
    
    # Créer un diagramme Sankey amélioré
    fig = go.Figure(go.Sankey(
        arrangement='snap',  # Meilleur arrangement pour la lisibilité
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color=theme_colors['gridLines'],
                width=0.5
            ),
            label=labels,
            color=node_colors,
            customdata=labels,  # Pour des infobulles améliorées
            hovertemplate='<b>%{customdata}</b><extra></extra>'
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            hovertemplate='<b>%{source.customdata}</b> → <b>%{target.customdata}</b><br>' +
                          'Nombre: %{value}<extra></extra>'
        )
    ))
    
    # Configuration du titre et des marges
    fig.update_layout(
        title=dict(
            text=translated_title,
            font=dict(
                size=18,
                color=theme_colors['text'],
                family="Arial, sans-serif",
                weight="bold"
            ),
            x=0.5,
            y=0.98
        ),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color=theme_colors['text']
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin=dict(l=5, r=5, t=80, b=5),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    # Ajouter une légende personnalisée
    fig.add_annotation(
        x=0.02,
        y=1.05,
        xref="paper",
        yref="paper",
        text="<b>Légende:</b>",
        showarrow=False,
        font=dict(
            size=12,
            color=theme_colors['text'],
            family="Arial, sans-serif"
        ),
        align="left"
    )
    
    fig.add_annotation(
        x=0.12,
        y=1.05,
        xref="paper",
        yref="paper",
        text="⬤ A déjà donné du sang",
        showarrow=False,
        font=dict(
            size=10,
            color=BLOOD_PALETTE['primary'][1],
            family="Arial, sans-serif"
        ),
        align="left"
    )
    
    fig.add_annotation(
        x=0.32,
        y=1.05,
        xref="paper",
        yref="paper",
        text="⬤ N'a jamais donné du sang",
        showarrow=False,
        font=dict(
            size=10,
            color=BLOOD_PALETTE['secondary'][1],
            family="Arial, sans-serif"
        ),
        align="left"
    )
    
    # Ajouter un effet de bordure pour améliorer l'aspect visuel
    fig.update_layout(
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color=theme_colors['gridLines'],
                    width=1
                ),
                layer='below'
            )
        ]
    )
    
    return fig


def CarteFolium(df, var1, var2, douala_gdf=douala_gdf, language="fr"):
    # Supprimer les lignes avec des NaN dans Latitude ou Longitude
    """
    Crée une carte Folium avec des marqueurs pour chaque quartier avec le nombre de femmes et d'hommes,
    ainsi qu'un cercle pour les éligibles.
    
    Args:
        df (pandas.DataFrame): Le DataFrame contenant les données à visualiser.
        var1 (str): Variable pour les cercles.
        var2 (str): Variable pour les popups.
        douala_gdf (geopandas.GeoDataFrame): GeoDataFrame contenant les polygones des arrondissements.
        language (str): La langue de l'interface ("fr" ou "en").
        
    Returns:
        str: HTML de la carte Folium.
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