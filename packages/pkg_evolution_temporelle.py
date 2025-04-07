import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import calendar
from prossess_data.process_temporelle import *
from sklearn.metrics import silhouette_score
from fanalysis.mca import MCA
from sklearn.cluster import KMeans
from prossess_data.prossess import corrige_date
import plotly_calplot

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

def Plot_genre(data, var_, title=''):
    """
    Crée un graphique en camembert avec trous pour visualiser les valeurs d'éligibilité d'un DataFrame.

    Args:
        data (pandas.DataFrame): Le DataFrame contenant les données à visualiser.
        var_ (str): Le nom de la colonne du DataFrame à utiliser pour les valeurs d'éligibilité.
        title (str, optionnel): Le titre du graphique (par défaut est une chaîne vide).

    Returns:
        plotly.graph_objs._figure.Figure: Un objet Figure de Plotly représentant le graphique en camembert.
    """
    
    # Créer un DataFrame pour les valeurs d'éligibilité
    elegibilite_counts = data[var_].value_counts().to_frame().reset_index()
    elegibilite_counts.columns = [var_, 'Total']

    # Créer un graphique en camembert avec trous
    fig0 = px.pie(
        elegibilite_counts, 
        values='Total', 
        names=var_, 
        hole=0.5,
        title=title,
        color_discrete_sequence=BLOOD_PALETTE['categorical']  # Utilisation de notre palette de couleurs
    )
    
    # Amélioration du style du graphique
    fig0.update_traces(
        pull=[0.1 if i == 1 else 0 for i in range(len(elegibilite_counts))],
        marker_line_color='white',  # Bordure blanche pour un meilleur contraste
        marker_line_width=1.5,
        opacity=0.9,
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        textfont=dict(size=10, family="Arial")
    )
    
    # Mise à jour de la mise en page
    fig0.update_layout(
        title_font=dict(size=14, family="Arial", color=BLOOD_PALETTE['primary'][1]),
        title_x=0.5,  # Centrer le titre
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.2, 
            xanchor="center", 
            x=0.5,
            font=dict(size=10, family="Arial")
        ),
        margin=dict(t=30, l=0, r=0, b=0),
        paper_bgcolor='rgba(248,248,248,0.3)',  # Fond légèrement grisé
        plot_bgcolor='rgba(248,248,248,0.3)'
    )
    
    # Ajouter une annotation au centre du trou
    fig0.add_annotation(
        text=f"Total:<br>{elegibilite_counts['Total'].sum()}",
        x=0.5, y=0.5,
        font=dict(size=12, color=BLOOD_PALETTE['primary'][1], family="Arial", weight="bold"),
        showarrow=False
    )
    
    return fig0


def visualiser_carte_chaleur_disponibilite(df, title="Disponibilité des Donneurs par Mois et Groupe d'Âge"):
    """
    Crée une carte de chaleur améliorée montrant la disponibilité des donneurs
    en fonction du mois et du groupe démographique.

    Args:
        df (pandas.DataFrame): DataFrame contenant les données des donneurs.
        title (str): Titre du graphique.

    Returns:
        plotly.graph_objects._figure.Figure: Une carte de chaleur montrant la disponibilité des donneurs.
    """
    # Préparer les données
    df_prepared = df
    
    # Compter les dons éligibles par mois et groupe d'âge
    pivot_data = pd.crosstab(
        index=df_prepared['Mois'],
        columns=df_prepared['Age_Class'],
        values=df_prepared['ÉLIGIBILITÉ AU DON.'].map({'Eligible': 1}),
        aggfunc='count',
        normalize=False  # Conserver les valeurs absolues
    )
    
    # Créer une copie pour les pourcentages
    pivot_percent = pivot_data.div(pivot_data.sum(axis=1), axis=0) * 100
    
    # Ordonner les mois correctement
    month_order = [calendar.month_name[i] for i in range(1, 13)]
    pivot_data = pivot_data.reindex(month_order)
    pivot_percent = pivot_percent.reindex(month_order)
    
    # Convertir le pivot en format pour heatmap
    z_data = pivot_data.values
    z_percent = pivot_percent.values
    x_data = pivot_data.columns.tolist()
    y_data = pivot_data.index.tolist()
    
    # Créer une palette de couleurs personnalisée basée sur le sang
    colorscale = [
        [0, 'rgba(255,255,255,1)'],                  # Blanc pour zéro
        [0.1, hex_to_rgba(BLOOD_PALETTE['primary'][4], 0.7)],  # Rouge très pâle
        [0.3, hex_to_rgba(BLOOD_PALETTE['primary'][3], 0.8)],  # Rouge pâle
        [0.5, hex_to_rgba(BLOOD_PALETTE['primary'][2], 0.85)], # Rouge moyen
        [0.7, hex_to_rgba(BLOOD_PALETTE['primary'][1], 0.9)],  # Rouge foncé
        [0.9, hex_to_rgba(BLOOD_PALETTE['primary'][0], 0.95)], # Rouge très foncé
        [1.0, hex_to_rgba(BLOOD_PALETTE['primary'][0], 1)]     # Rouge intense
    ]
    
    # Créer la figure
    fig = go.Figure()
    
    # Ajouter la carte de chaleur
    fig.add_trace(go.Heatmap(
        z=z_data,
        x=x_data,
        y=y_data,
        colorscale=colorscale,
        text=[[f"{z:.0f}<br>({p:.1f}%)" for z, p in zip(row_z, row_p)]
                for row_z, row_p in zip(z_data, z_percent)],
        texttemplate="%{text}",
        textfont={"size": 10, "color": "black", "family": "Arial"},
        hoverinfo='x+y+z',
        hovertemplate='<b>%{y}, Groupe %{x}</b><br>Donneurs éligibles: %{z}<extra></extra>',
        colorbar=dict(
            title=dict(
                text="Nombre<br>de donneurs<br>éligibles",
                font=dict(size=12, color=BLOOD_PALETTE['primary'][1], family="Arial")
            ),
            titleside="top",
            tickmode="auto",
            ticks="outside",
            tickfont=dict(size=10, family="Arial"),
            outlinecolor="white",
            outlinewidth=1,
            bordercolor="white",
            borderwidth=1
        )
    ))
    
    # Ajouter des lignes de grille pour une meilleure lisibilité
    for i in range(len(y_data)+1):
        fig.add_shape(
            type="line",
            x0=-0.5, y0=i-0.5, x1=len(x_data)-0.5, y1=i-0.5,
            line=dict(color="white", width=2)
        )
        
    for i in range(len(x_data)+1):
        fig.add_shape(
            type="line",
            x0=i-0.5, y0=-0.5, x1=i-0.5, y1=len(y_data)-0.5,
            line=dict(color="white", width=2)
        )
    
    # Ajouter des icônes représentant des gouttes de sang dans les coins
    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/commons/c/c3/Blood_drop_icon.svg",
            xref="paper", yref="paper",
            x=0.01, y=0.99,
            sizex=0.05, sizey=0.05,
            xanchor="right", yanchor="bottom",
            opacity=0.7
        )
    )
    
    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/commons/c/c3/Blood_drop_icon.svg",
            xref="paper", yref="paper",
            x=0.99, y=0.99,
            sizex=0.05, sizey=0.05,
            xanchor="right", yanchor="bottom",
            opacity=0.7
        )
    )
    
    # Personnaliser la mise en page
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial", color=BLOOD_PALETTE['primary'][1]),
            x=0.5,
            y=0.97
        ),
        height=700,
        width=1000,
        xaxis=dict(
            title=dict(text="Groupe d'Âge", font=dict(size=14, family="Arial")),
            side="bottom",
            tickfont=dict(size=12, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            linecolor='rgba(200,200,200,0.8)'
        ),
        yaxis=dict(
            title=dict(text="Mois", font=dict(size=14, family="Arial")),
            categoryorder='array',
            categoryarray=month_order,
            tickfont=dict(size=12, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            linecolor='rgba(200,200,200,0.8)'
        ),
        margin=dict(t=70, b=20, l=10, r=10),
        plot_bgcolor='rgba(248,248,248,0.9)',
        paper_bgcolor='rgba(248,248,248,0.9)'
    )
    
    # Ajouter des annotations supplémentaires
    fig.add_annotation(
        text="Valeur = Nombre absolu (pourcentage par ligne)",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=12, family="Arial", color=BLOOD_PALETTE['primary'][2])
    )
    
    return fig



def retour_evolution_glob_anuel(data_don_annee=data_don_annee, title="Évolution des dons au fil des années"):
    """
    Crée un graphique en aires montrant l'évolution globale des dons au fil des années.

    Args:
        data_don_annee (pandas.DataFrame, optional): DataFrame contenant les données des dons par année. Defaults to data_don_annee.
        title (str): Titre du graphique.

    Returns:
        plotly.graph_objects._figure.Figure: Un graphique en aires montrant l'évolution des dons.
    """
    # Créer le graphique en utilisant Plotly
    fig = px.area(data_don_annee, x='Annee', y='count',
                title=title,
                labels={'Annee': 'Année du don', 'count': 'Nombre de donneurs'})
    fig.update_traces(marker_color='lightgreen',marker_line_color='black',opacity=1,marker_line_width=1)

    fig.update_layout(title_font_size=12,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30,l=0,r=0,b=0),yaxis_title='',
        xaxis=dict(
            title='',
            type='category',  
            tickmode='linear',  
            tick0=data_don_annee['Annee'].min(),  
            dtick=1,
            tickangle=-45,
            showgrid=False
        )
    )

    return fig


def plot_evol_anne_var(data_don=data_don, var_='Genre', title='Distribution des dons par année et par genre'):
    """
    Crée un graphique en aires montrant l'évolution des dons par année et par variable (par exemple, genre, âge, etc.).
    
    Args:
        data_don (pandas.DataFrame, optional): Le DataFrame contenant les données des dons. Defaults to data_don.
        var_ (str, optional): Le nom de la colonne du DataFrame contenant la variable à utiliser. Defaults to 'Genre'.
        title (str, optional): Le titre du graphique. Defaults to 'Distribution des dons par année et par genre'.
    
    Returns:
        plotly.graph_objects._figure.Figure: Un graphique en aires montrant l'évolution des dons.
    """
    # Préparer les données
    data_prepared = data_don[['Annee', var_]].value_counts().reset_index().sort_values(by='Annee')
    
    # Créer une figure
    fig = go.Figure()
    
    # Déterminer les catégories uniques pour var_
    categories = data_don[var_].unique()
    
    # Utiliser des couleurs de notre palette, adaptées selon le nombre de catégories
    if len(categories) <= 2:
        # Pour le genre (typiquement 2 valeurs), utiliser rouge et bleu
        colors = [BLOOD_PALETTE['primary'][1], BLOOD_PALETTE['secondary'][1]]
    elif len(categories) <= 5:
        # Pour quelques catégories, utiliser les couleurs principales
        colors = BLOOD_PALETTE['categorical'][:len(categories)]
    else:
        # Pour beaucoup de catégories, utiliser une interpolation de couleurs
        import plotly.colors as pc
        colors = pc.n_colors(BLOOD_PALETTE['primary'][0], BLOOD_PALETTE['secondary'][0], len(categories), colortype='rgb')
    
    # Créer un pivot des données pour faciliter la création du graphique
    pivot_df = data_prepared.pivot(index='Annee', columns=var_, values='count').fillna(0)
    
    # Ajouter chaque catégorie comme une aire empilée
    for i, category in enumerate(pivot_df.columns):
        fig.add_trace(go.Scatter(
            x=pivot_df.index,
            y=pivot_df[category],
            mode='lines',
            line=dict(width=0.5, color=colors[i % len(colors)]),
            stackgroup='one',
            name=category,
            fillcolor=hex_to_rgba(colors[i % len(colors)], 0.8),
            hovertemplate='<b>%{x}</b><br>%{y} dons<extra>' + category + '</extra>'
        ))
    
    # Mise à jour de la mise en page
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family="Arial", color=BLOOD_PALETTE['primary'][1]),
            x=0.5
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5,
            font=dict(size=10, family="Arial")
        ),
        margin=dict(t=50, l=20, r=20, b=70),
        yaxis=dict(
            title='Nombre de dons',
            title_font=dict(size=14, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            zerolinecolor='rgba(200,200,200,0.5)'
        ),
        xaxis=dict(
            type='category',
            tickmode='linear',
            tickangle=-45,
            tickfont=dict(size=12, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            title=''
        ),
        paper_bgcolor='rgba(248,248,248,0.3)',
        plot_bgcolor='rgba(248,248,248,0.3)',
        hovermode='x unified'
    )
    
    # Ajouter une icône décorative
    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/commons/c/c3/Blood_drop_icon.svg",
            xref="paper", yref="paper",
            x=0.03, y=0.97,
            sizex=0.05, sizey=0.05,
            xanchor="right", yanchor="bottom",
            opacity=0.7
        )
    )
    
    return fig



def retourn_evolution_mois(data_don=data_don, title="Évolution mensuelle des dons de sang"):
    """
    Crée un graphique à barres montrant l'évolution totale des dons au fil des mois.

    Cette fonction génère un graphique à barres utilisant Plotly pour visualiser le nombre total de dons
    par mois, en utilisant les données fournies dans le DataFrame. Les mois sont ordonnés chronologiquement.

    Args:
        data_don (pandas.DataFrame): Le DataFrame contenant les informations sur les dons de sang,
                                     avec une colonne 'Mois' indiquant le mois de chaque don.
        title (str): Titre du graphique.

    Returns:
        plotly.graph_objects._figure.Figure: Un graphique à barres montrant l'évolution des dons au fil des mois.
    """
    categorie = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    data_don_mois = data_don['Mois'].value_counts().reset_index()
    data_don_mois.columns = ['Mois', 'count']
    
    # Ordonner les mois correctement
    data_don_mois['Mois'] = pd.Categorical(data_don_mois['Mois'], categories=categorie, ordered=True)
    data_don_mois = data_don_mois.sort_values('Mois')

    # Créer une figure
    fig = go.Figure()
    
    # Couleurs pour un effet de gradient par mois
    colors = []
    for i in range(len(data_don_mois)):
        # Utiliser un gradient rouge-bleu pour différencier les saisons
        # Hiver/début d'année: plus de bleu, Été/milieu d'année: plus de rouge
        if i < len(data_don_mois) / 3:
            # Premier tiers (hiver/printemps) - tons de bleu
            color = BLOOD_PALETTE['secondary'][i % len(BLOOD_PALETTE['secondary'])]
        elif i < 2 * len(data_don_mois) / 3:
            # Deuxième tiers (printemps/été) - tons de rouge
            color = BLOOD_PALETTE['primary'][i % len(BLOOD_PALETTE['primary'])]
        else:
            # Dernier tiers (automne/hiver) - tons de bleu/violet
            color = BLOOD_PALETTE['secondary'][4 - (i % len(BLOOD_PALETTE['secondary']))]
        colors.append(color)
    
    # Ajouter les barres
    fig.add_trace(go.Bar(
        x=data_don_mois['Mois'],
        y=data_don_mois['count'],
        text=data_don_mois['count'],
        textposition='auto',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1.5)
        ),
        hovertemplate='<b>%{x}</b><br>%{y} dons<extra></extra>'
    ))
    
    # Ajouter une ligne de tendance
    fig.add_trace(go.Scatter(
        x=data_don_mois['Mois'],
        y=data_don_mois['count'],
        mode='lines+markers',
        line=dict(color=BLOOD_PALETTE['primary'][0], width=2, dash='dot'),
        marker=dict(size=8, color=BLOOD_PALETTE['primary'][0], line=dict(width=2, color='white')),
        name='Tendance',
        hoverinfo='skip'
    ))
    
    # Améliorer la mise en page
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family="Arial", color=BLOOD_PALETTE['primary'][1]),
            x=0.5
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.4, 
            xanchor="center", 
            x=0.5,
            font=dict(size=10, family="Arial")
        ),
        margin=dict(t=50, l=20, r=20, b=70),
        yaxis=dict(
            title='Nombre de donneurs',
            title_font=dict(size=14, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            zerolinecolor='rgba(200,200,200,0.5)',
            showgrid=True
        ),
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=categorie,
            tickangle=-25,
            tickfont=dict(size=12, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            title=''
        ),
        paper_bgcolor='rgba(248,248,248,0.3)',
        plot_bgcolor='rgba(248,248,248,0.3)',
        showlegend=False
    )
    
    # Ajouter une annotation pour la valeur maximale
    max_point = data_don_mois.loc[data_don_mois['count'].idxmax()]
    fig.add_annotation(
        x=max_point['Mois'],
        y=max_point['count'],
        text="Max",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor=BLOOD_PALETTE['primary'][0],
        font=dict(size=12, color=BLOOD_PALETTE['primary'][0], family="Arial"),
        bgcolor="white",
        bordercolor=BLOOD_PALETTE['primary'][0],
        borderwidth=1,
        borderpad=4,
        yshift=20
    )
    
    return fig


def plot_mois_vars_counts(var_='Genre', title='Répartition des dons par mois et par genre'):
    """
    Crée un graphique à barres empilées montrant la répartition des dons par mois et par variable.

    Cette fonction génère un graphique à barres empilées utilisant Plotly pour visualiser la répartition
    des dons par mois et par variable (par exemple, genre, âge, etc.), en utilisant les données fournies
    dans le DataFrame. Les mois sont ordonnés chronologiquement.

    Args:
        var_ (str, optional): Le nom de la colonne du DataFrame contenant la variable à utiliser.
                             Defaults to 'Genre'.
        title (str, optional): Le titre du graphique. Defaults to 'Répartition des dons par mois et par genre'.
    
    Returns:
        plotly.graph_objects._figure.Figure: Un graphique à barres empilées montrant la répartition des dons par mois et par variable.
    """
    
    categorie = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Compter les occurrences par mois et par variable
    counts_df = data_don[['Mois', var_]].value_counts().reset_index(name='count')
    
    # Créer une figure
    fig = go.Figure()
    
    # Obtenir les valeurs uniques de la variable et déterminer la palette de couleurs
    unique_values = data_don[var_].unique()
    
    # Choisir la palette de couleurs en fonction du type de variable
    if var_ == 'Genre':
        # Pour le genre, utiliser des couleurs spécifiques
        color_map = {
            'Homme': BLOOD_PALETTE['primary'][1],  # Rouge pour les hommes (traditionnellement associé au sang)
            'Femme': BLOOD_PALETTE['secondary'][1]  # Bleu pour les femmes (traditionnellement médical)
        }
        colors = [color_map.get(val, BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])]) 
                  for i, val in enumerate(unique_values)]
    elif var_ == 'ÉLIGIBILITÉ AU DON.':
        # Pour l'éligibilité, utiliser des couleurs significatives
        color_map = {
            'Eligible': BLOOD_PALETTE['primary'][1],                # Rouge pour éligible (don de sang)
            'Temporairement Non-eligible': BLOOD_PALETTE['warm'][1], # Orange pour temporairement non éligible
            'Définitivement non-eligible': BLOOD_PALETTE['neutral'][1] # Gris pour définitivement non éligible
        }
        colors = [color_map.get(val, BLOOD_PALETTE['categorical'][i % len(BLOOD_PALETTE['categorical'])]) 
                  for i, val in enumerate(unique_values)]
    else:
        # Pour les autres variables, utiliser la palette catégorielle
        # Avec assez de distinction entre les couleurs
        if len(unique_values) <= len(BLOOD_PALETTE['categorical']):
            colors = BLOOD_PALETTE['categorical'][:len(unique_values)]
        else:
            # Si trop de catégories, utiliser une palette générée dynamiquement
            import plotly.colors as pc
            colors = pc.n_colors(BLOOD_PALETTE['primary'][0], BLOOD_PALETTE['secondary'][2], len(unique_values), colortype='rgb')
    
    # Créer un pivot pour faciliter le traitement
    pivot_df = counts_df.pivot(index='Mois', columns=var_, values='count').fillna(0)
    pivot_df = pivot_df.reindex(categorie)
    
    # Ajouter chaque catégorie comme une barre empilée
    for i, category in enumerate(pivot_df.columns):
        fig.add_trace(go.Bar(
            x=pivot_df.index,
            y=pivot_df[category],
            name=category,
            marker=dict(
                color=colors[i % len(colors)],
                line=dict(color='white', width=0.8)
            ),
            hovertemplate='<b>%{x}</b><br>%{y} dons<extra>' + str(category) + '</extra>'
        ))
    
    # Améliorer la mise en page
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, family="Arial", color=BLOOD_PALETTE['primary'][1]),
            x=0.5
        ),
        barmode='stack',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5,
            font=dict(size=10, family="Arial"),
            title_text=''
        ),
        margin=dict(t=50, l=20, r=20, b=70),
        yaxis=dict(
            title='Nombre de dons',
            title_font=dict(size=14, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            zerolinecolor='rgba(200,200,200,0.5)',
            showgrid=True
        ),
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=categorie,
            tickangle=-25,
            tickfont=dict(size=12, family="Arial"),
            gridcolor='rgba(200,200,200,0.2)',
            title=''
        ),
        paper_bgcolor='rgba(248,248,248,0.3)',
        plot_bgcolor='rgba(248,248,248,0.3)',
        hovermode='x unified'
    )
    
    # Ajouter un texte pour les totaux au-dessus des barres
    # Calculer les totaux par mois
    monthly_totals = pivot_df.sum(axis=1)
    
    # Ajouter des annotations pour les totaux
    for i, month in enumerate(pivot_df.index):
        if month in monthly_totals.index:
            total = monthly_totals[month]
            fig.add_annotation(
                x=month,
                y=total,
                text=f"{int(total)}",
                showarrow=False,
                yshift=10,
                font=dict(size=10, family="Arial", color=BLOOD_PALETTE['primary'][0])
            )
    
    return fig



def create_acm_eligibility_dashboard(data=data_final, variables=None, title="Analyse des donneurs de sang: Éligibilité et comportements"):
    """
    Crée un dashboard avec deux graphiques:
    - À gauche: un diagramme d'éligibilité au don
    - À droite: un scatter plot ACM avec clustering
    
    Parameters:
    data (DataFrame): DataFrame contenant les données relatifs aux personnes ayant deja donner du sang
    variables (list): Liste des variables à utiliser pour l'ACM (optionnel)
    title (str): Titre du dashboard
    
    Returns:
    go.Figure: Figure Plotly contenant les deux graphiques
    """
    # Définir les bornes des classes d'âge
    a = (pd.to_datetime(data['Date de remplissage de la fiche']).dt.year - pd.to_datetime(data['Date de naissance']).dt.year)
    data['Age'] = a.values
    
    bins = [0, 19, 29, 39, 49, 59, 69, 200]  # Corrigé la dernière borne à 69 pour correspondre à '60-69'
    labels = ['<=19', '20-29', '30-39', '40-49', '50-59', '60-69', '>=70']  # Corrigé à '>=70' pour être cohérent
    
    # Créer une nouvelle colonne 'Classe_Age' avec les classes d'âge
    data['Classe_Age'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)
    
    
    # Préparer les données
    data_prof = data[data['A-t-il (elle) déjà donné le sang'] == 'Oui'].copy()
    
    # Correction des dates si la fonction corrige_date est définie
    try:
        data_prof['Date de remplissage de la fiche'] = corrige_date(data_prof)
        data_prof = data_prof[data_prof['Date de remplissage de la fiche'].dt.year == 2019]
        data_prof['mois_don'] = data_prof['Date de remplissage de la fiche'].dt.month_name()
    except:
        print("Fonction corrige_date non disponible, traitement des dates ignoré")
    
    # Définir les variables à utiliser
    if variables is None:
        liste_var = ["Niveau d'etude", "Genre", "Situation Matrimoniale (SM)",
                   "Religion", 'Classe_Age', 'mois_don', 'ÉLIGIBILITÉ AU DON.']
    else:
        liste_var = variables
        
    data_prof = data_prof[liste_var]
    
    # Remplir les valeurs manquantes pour la classe d'âge
    data_prof['Classe_Age'] = data_prof['Classe_Age'].fillna(data_prof['Classe_Age'].mode().values[0])
    
    # Définir les fonctions de recodage
    def recode_age(age_range):
        if age_range in ['40-49', '50-59', '60-69', '>=71']:
            return '>=40'
        elif age_range in ['<=19', '20-29']:
            return '<=29'
        else:
            return age_range
        
    def recode_niveau_etudes(niveau):
        if niveau in ['Pas Précisé', 'Primaire', 'Aucun']:
            return 'PPprAcu'
        else:
            return niveau
    
    def recode_situation_matrimoniale(situation):
        if situation in ['Divorcé(e)', 'veuf (veuve)', 'Célibataire']:
            return 'Célibataire'
        else:
            return situation
     
    def recode_religions(religion):
        if 'chrétien' in str(religion).lower() or 'pentec' in str(religion).lower():
            return 'chrétien'
        else:
            return religion
    
    # Appliquer les recodages
    data_prof["Religion"] = data_prof["Religion"].map(recode_religions)
    data_prof["Situation Matrimoniale (SM)"] = data_prof["Situation Matrimoniale (SM)"].map(recode_situation_matrimoniale)
    data_prof["Niveau d'etude"] = data_prof["Niveau d'etude"].map(recode_niveau_etudes)
    data_prof['Classe_Age'] = data_prof['Classe_Age'].map(recode_age)
    
    # Préparer les données pour l'ACM
    data_acm = data_prof.copy()
    
    # Effectuer l'ACM
    mca = MCA(n_components=5, row_labels=data_acm.index, var_labels=data_acm.columns)
    mca.fit(data_acm.values)
    
    # Récupérer les coordonnées des modalités
    coord_col = mca.col_coord_
    coord_col_df = pd.DataFrame(coord_col, index=mca.col_labels_short_temp_)
    
    # Extraire les coordonnées pour le clustering
    X = coord_col_df.iloc[:, 0:2].values
    
    # Déterminer le nombre optimal de clusters
    silhouette_scores = []
    range_clusters = range(2, 11)
    
    for n_clusters in range_clusters:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(X)
        
        if len(np.unique(cluster_labels)) > 1:
            silhouette_avg = silhouette_score(X, cluster_labels)
            silhouette_scores.append(silhouette_avg)
        else:
            silhouette_scores.append(0)
    
    optimal_clusters = range_clusters[np.argmax(silhouette_scores)] + 2
    
    # Appliquer le K-means avec le nombre optimal de clusters
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    # Créer une palette de couleurs
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Préparer les données pour le diagramme d'éligibilité
    eligibility_counts = data_prof['ÉLIGIBILITÉ AU DON.'].value_counts()
    
    # Créer la figure avec subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("", ""),
        specs=[[{"type": "pie"}, {"type": "scatter"}]],
        column_widths=[0.4, 0.6]
    )
    
    # Ajouter le diagramme circulaire pour l'éligibilité
    fig.add_trace(
        go.Pie(
            labels=eligibility_counts.index,
            values=eligibility_counts.values,
            textinfo='percent+label',
            hole=0.4,
            marker=dict(colors=['#2ca02c', '#d62728', '#1f77b4'])
        ),
        row=1, col=1
    )
    
    # Ajouter le scatter plot ACM
    for cluster_id in range(optimal_clusters):
        cluster_indices = np.where(clusters == cluster_id)[0]
        
        fig.add_trace(
            go.Scatter(
                x=X[cluster_indices, 0],
                y=X[cluster_indices, 1],
                mode='markers+text',
                text=[coord_col_df.index[i] for i in cluster_indices],
                textposition='top center',
                marker=dict(color=colors[cluster_id % len(colors)], size=10),
                name=f'Cluster {cluster_id+1}'
            ),
            row=1, col=2
        )
    
    # Mettre à jour la mise en page
    fig.update_layout(
        title_text=title,
        height=600,
        width=1200,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        font=dict(size=10),
        template="plotly_white"
    )
    
    # Personnaliser les axes du scatter plot
    fig.update_xaxes(title_text="Axe 1", row=1, col=2)
    fig.update_yaxes(title_text="Axe 2", row=1, col=2)
    
    return fig


def prepare_calendar_data(df):
    # Compter le nombre d'occurrences par date
    """
    Prépare les données pour la visualisation du calendrier
    ------------------------------------------------------------------
    Compte le nombre d'occurrences par date, convertit la colonne de date
    en datetime si ce n'est pas déjà le cas, et filtre uniquement pour
    les années 2019 et 2020.

    Parameters
    ----------
    df : pandas.DataFrame
        Le dataframe contenant la colonne 'Date de remplissage de la fiche'

    Returns
    -------
    pandas.DataFrame
        Le dataframe contenant les dates et le nombre d'occurrences
    """
    date_counts = df['Date de remplissage de la fiche'].value_counts().reset_index()
    date_counts.columns = ['Date', 'Nombre']
   
    # Convertir la colonne de date en datetime si ce n'est pas déjà le cas
    date_counts['Date'] = pd.to_datetime(date_counts['Date'])
   
    # Filtrer uniquement pour les années 2019 et 2020
    date_counts = date_counts[date_counts['Date'].dt.year.isin([2019])]
   
    return date_counts

def create_calendar_heatmap(df, title="Calendrier des remplissages de fiches"):
    # Créer un Series avec la date comme index et le nombre comme valeurs
    """
    Crée un calendrier en heatmap montrant les remplissages de fiches au fil du temps.

    Parameters
    ----------
    df : pandas.DataFrame
        Le dataframe contenant la colonne 'Date de remplissage de la fiche'
    title : str
        Le titre du graphique

    Returns
    -------
    plotly.graph_objects._figure.Figure
        Le calendrier en heatmap
    """
    date_counts = prepare_calendar_data(df)
    data_series = date_counts.set_index('Date')['Nombre']
    
    # Créer une palette de couleurs personnalisée liée au don de sang
    blood_colorscale = [
        [0, 'rgba(255,255,255,1)'],              # Blanc pour zéro
        [0.1, hex_to_rgba(BLOOD_PALETTE['primary'][4], 0.4)],  # Rouge très pâle 
        [0.3, hex_to_rgba(BLOOD_PALETTE['primary'][3], 0.6)],  # Rouge pâle
        [0.5, hex_to_rgba(BLOOD_PALETTE['primary'][2], 0.7)],  # Rouge moyen
        [0.7, hex_to_rgba(BLOOD_PALETTE['primary'][1], 0.8)],  # Rouge foncé
        [0.9, hex_to_rgba(BLOOD_PALETTE['primary'][0], 0.9)],  # Rouge très foncé
        [1.0, BLOOD_PALETTE['primary'][0]]                     # Rouge intense
    ]
    
    # Utiliser plotly_calplot pour créer la visualisation
    fig = plotly_calplot.calplot(
        date_counts,
        x='Date',
        y='Nombre',
        title=title,
        colorscale=blood_colorscale,
        showscale=True,
        month_lines_width=3, 
        month_lines_color="#fff",
        dark_theme=False,
        years_title=True
    )
    
    # Ajout de textes et amélioration de la mise en page
    fig.update_layout(
        height=450,
        width=1000,
        title_font=dict(
            family="Arial",
            size=20,
            color=BLOOD_PALETTE['primary'][1]
        ),
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="Nombre de fiches",
            titlefont=dict(size=12, family="Arial"),
            tickfont=dict(size=10, family="Arial"),
            len=0.5,
            thickness=15,
            outlinewidth=1,
            outlinecolor="white"
        ),
        margin=dict(t=50, l=20, r=20, b=20),
        paper_bgcolor='rgba(248,248,248,0.3)',
        plot_bgcolor='rgba(248,248,248,0.3)'
    )
    
    # Ajouter une annotation explicative
    fig.add_annotation(
        text="Intensité de couleur = Nombre de fiches remplies",
        xref="paper", yref="paper",
        x=0.5, y=-0.1,
        showarrow=False,
        font=dict(size=12, family="Arial", color=BLOOD_PALETTE['primary'][2])
    )
    
    # Ajouter une icône décorative (goutte de sang)
    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/commons/c/c3/Blood_drop_icon.svg",
            xref="paper", yref="paper",
            x=0.01, y=0.99,
            sizex=0.05, sizey=0.05,
            xanchor="right", yanchor="bottom",
            opacity=0.7
        )
    )
    
    return fig