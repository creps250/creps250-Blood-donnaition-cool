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


def Plot_genre(data,var_,title=''):
    """
    Crée un graphique en camembert avec trous pour visualiser les valeurs d'éligibilité d'un DataFrame.
    Paramètres:
    -----------
    data_cluster_don : pandas.DataFrame
        Le DataFrame contenant les données à visualiser.
    var_ : str
        Le nom de la colonne du DataFrame à utiliser pour les valeurs d'éligibilité.
    title : str, optionnel
        Le titre du graphique (par défaut est une chaîne vide).
    Retourne:
    --------
    plotly.graph_objs._figure.Figure
        Un objet Figure de Plotly représentant le graphique en camembert.
    """
    
    # Créer un DataFrame pour les valeurs d'éligibilité
    elegibilite_counts = data[var_].value_counts().to_frame().reset_index()
    elegibilite_counts.columns = [var_, 'Total']

    # Créer un graphique en camembert avec trous
    fig0 = px.pie(elegibilite_counts, values='Total', names=var_, hole=0.5,
                title=title)
                # Séparer une partie du camembert
    fig0.update_traces(pull=[0.1 if i == 1 else 0 for i in range(len(elegibilite_counts))])
    fig0.update_layout(title_font_size=12,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,font=dict(size=10)),
        margin=dict(t=0,l=0,r=0,b=0)
        )
    fig0.update_traces(marker_line_color='black',opacity=1,marker_line_width=1,textfont=dict(size=8))
    return fig0


def visualiser_carte_chaleur_disponibilite(df):
    """
    Crée une carte de chaleur améliorée montrant la disponibilité des donneurs
    en fonction du mois et du groupe démographique.
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
    
    # Créer une palette de couleurs améliorée
    colorscale = [
        [0, '#FFFFFF'], [0.1, '#FFF8E1'], [0.2, '#FFECB3'], [0.3, '#FFD54F'],
        [0.4, '#FFCA28'], [0.5, '#FFC107'], [0.6, '#FFB300'], [0.7, '#FFA000'],
        [0.8, '#FF8F00'], [0.9, '#FF6F00'], [1.0, '#E65100']
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
        textfont={"size": 8, "color": "black"},  # Taille réduite à 8 points
        hoverinfo='x+y+z',
        hovertemplate='<b>%{y}, Groupe %{x}</b><br>Donneurs éligibles: %{z}<extra></extra>',
        colorbar=dict(
            title="Nombre<br>de donneurs<br>éligibles",
            titleside="top",
            tickmode="auto",
            ticks="outside"
        )
    ))
    
    # Ajouter des lignes de grille pour une meilleure lisibilité
    for i in range(len(y_data)+1):
        fig.add_shape(
            type="line",
            x0=-0.5, y0=i-0.5, x1=len(x_data)-0.5, y1=i-0.5,
            line=dict(color="White", width=2)
        )
        
    for i in range(len(x_data)+1):
        fig.add_shape(
            type="line",
            x0=i-0.5, y0=-0.5, x1=i-0.5, y1=len(y_data)-0.5,
            line=dict(color="White", width=2)
        )
    
    # Personnaliser la mise en page
    fig.update_layout(
        title=dict(
            text="Disponibilité des Donneurs par Mois et Groupe d'Âge",
            font=dict(size=20, family="Arial", color="#E65100"),
            x=0.5,
            y=0.97
        ),
        height=700,
        width=1000,
        xaxis=dict(
            title=dict(text="Groupe d'Âge", font=dict(size=16)),
            side="bottom",
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            title=dict(text="Mois", font=dict(size=16)),
            categoryorder='array',
            categoryarray=month_order,
            tickfont=dict(size=14)
        ),
        margin=dict(t=70, b=20, l=10, r=10),
        plot_bgcolor='rgba(250,250,250,0.9)',
        paper_bgcolor='rgba(250,250,250,0.9)'
    )
    
    # Ajouter des annotations supplémentaires
    fig.add_annotation(
        text="Valeur = Nombre absolu (pourcentage par ligne)",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=12)
    )
    
    return fig


def retour_evolution_glob_anuel(data_don_annee=data_don_annee):
    # Créer le graphique en utilisant Plotly
    fig = px.area(data_don_annee, x='Annee', y='count',
                title='Evolution des dons au fils des annees',
                labels={'Annee': 'Annee du dont', 'count': 'Effectifs de donneurs'})
    fig.update_traces(marker_color='lightgreen',marker_line_color='black',opacity=1,marker_line_width=1)

    fig.update_layout(title_font_size=12,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30,l=0,r=0,b=0),yaxis_title='',
        xaxis=dict(
            title='',
            type='category',  
            tickmode='linear',  
            tick0=data_don_annee['Annee'].min(),  
            dtick=1  ,
            tickangle=-45,
            showgrid=False
        )
        )

    return fig


def plot_evol_anne_var(data_don = data_don,var_='Genre',title='Nombre de dons par année et par genre'):
    fig = px.area(data_don[['Annee', var_]].value_counts().reset_index().sort_values(by='Annee'), 
                x='Annee', 
                y='count', 
                color=var_, 
                title=title,
                labels={'Annee': 'Année', 'count': 'Nombre de dons', var_: var_})

    fig.update_layout(
        title_font_size=12,
        legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
        margin=dict(t=30,l=0,r=0,b=0),yaxis_title='',
        xaxis=dict(
            type='category',  
            tickmode='linear',  
            tick0=data_don_annee['Annee'].min(),  
            dtick=1  ,
            tickangle=-45,
            categoryarray= data_don_annee.Annee.tolist(),
            showgrid=False,
            title=''
        )
        )

    return fig


def retourn_evolution_mois(data_don=data_don):
    data_don_mois = data_don['Mois'].value_counts().reset_index()
    data_don_mois.columns = ['Mois', 'count']

    # Créer le graphique en utilisant Plotly
    fig = px.bar(data_don_mois, x='Mois', y='count',text_auto=True,
                title='Evolution total de dons au fil des mois',
                labels={'Mois': 'Mois du dont', 'count': 'Effectifs de donneurs'})
    fig.update_traces(marker_color='lightblue', marker_line_color='black', opacity=1, marker_line_width=1)

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5),
        margin=dict(t=30,l=0,r=10,b=20), yaxis_title='',xaxis_title='',
        xaxis=dict(
            type='category',   # Assure que l'axe des x est traité comme une catégorie
            categoryorder='array',   # Utilise l'ordre défini dans 'categoryarray'
            categoryarray=categorie, # Applique l'ordre des mois
            tickangle=-25,
            showgrid=False
        ),title_font_size=12
    )

    return fig


def plot_mois_vars_counts(var_='Genre', title='Répartition des dons par mois et par genre'):

    categorie = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Compter les occurrences par mois et par variable
    counts_df = data_don[['Mois', var_]].value_counts().reset_index(name='count')

    # Créer le graphique à barres empilées
    fig = px.bar(counts_df,
                 x='Mois',
                 y='count',
                 color=var_,
                 title=title,
                 labels={'Mois': 'Mois', 'count': 'Nombre de dons', var_: var_},
                 category_orders={'Mois': categorie}, # Ordre des mois
                 color_discrete_sequence=px.colors.qualitative.Set2) # Utilisation d'une palette de couleurs harmonisée

    # Adoucir le style du graphique
    fig.update_traces(marker=dict(line=dict(width=0.5, color='rgba(0,0,0,0.2)')),  # Bordures douces
                      opacity=0.8)  # Légère transparence

    # Personnaliser la mise en page
    fig.update_layout(
        barmode='stack',  # Mode empilé
        yaxis=dict(
            title='Nombre de dons',
            showgrid=False,  # Masquer la grille de l'axe Y
        ),
        xaxis=dict(
            tickangle=-45,
            showgrid=False,  # Masquer la grille de l'axe X
            title=''
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            title_text=''  # Masquer le titre de la légende
        ),
        font=dict(family='Arial, sans-serif', size=12, color='#333333'),  # Police douce
        margin=dict(t=50, l=0, r=0, b=0),title_font_size=12
    )

    return fig



def create_acm_eligibility_dashboard(data=data_final, variables=None):
    """
    Crée un dashboard avec deux graphiques:
    - À gauche: un diagramme d'éligibilité au don
    - À droite: un scatter plot ACM avec clustering
    
    Parameters:
    data (DataFrame): DataFrame contenant les données relatifs aux personnes ayant deja donner du sang
    variables (list): Liste des variables à utiliser pour l'ACM (optionnel)
    
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
        title_text="Analyse des donneurs de sang: Éligibilité et caractéristiques",
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
    date_counts = df['Date de remplissage de la fiche'].value_counts().reset_index()
    date_counts.columns = ['Date', 'Nombre']
   
    # Convertir la colonne de date en datetime si ce n'est pas déjà le cas
    date_counts['Date'] = pd.to_datetime(date_counts['Date'])
   
    # Filtrer uniquement pour les années 2019 et 2020
    date_counts = date_counts[date_counts['Date'].dt.year.isin([2019])]
   
    return date_counts


def create_calendar_heatmap(df):
    # Créer un Series avec la date comme index et le nombre comme valeurs
    date_counts = prepare_calendar_data(df)
    data_series = date_counts.set_index('Date')['Nombre']
    
    # Utiliser plotly_calplot pour créer la visualisation
    fig = plotly_calplot.calplot(
        date_counts,
        x='Date',
        y='Nombre',
        title='Calendrier des remplissages de fiches',
        colorscale='plasma',
        showscale=True,
        month_lines_width=3, 
        month_lines_color="#fff",
        dark_theme=False
        
    )
    
    # Ajuster la mise en page 
    fig.update_layout(
        height=400,
        width=1000,
        title_x=0.5
    )
    
    return fig
