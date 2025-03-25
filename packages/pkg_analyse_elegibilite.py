import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from plotly.subplots import make_subplots
from wordcloud import WordCloud 
from prossess_data.process_analyse_elegibilite import *
from nltk.corpus import stopwords
import nltk


### pour gerer le telechargement des stopword
try:
    a = set(stopwords.words('french'))
except:
    nltk.download('stopwords')    



def create_circular_mask(size):
    """
    Crée un masque circulaire pour une image carrée de taille donnée.
    Paramètres:
    size (int): La taille (largeur et hauteur) de l'image carrée.
    Retourne:
    numpy.ndarray: Un tableau 2D représentant le masque circulaire. Les pixels à l'intérieur du cercle sont définis à 0,
    tandis que les pixels à l'extérieur du cercle sont définis à 255.
    """
    
    x, y = np.ogrid[:size, :size]
    mask = (x - size / 2) ** 2 + (y - size / 2) ** 2 > (size / 2) ** 2
    mask = 255 * mask.astype(int)  # 0 pour le cercle, 255 pour le reste
    return mask

def remove_stop_words(text):
    """
    Supprime les mots vides (stop words) français du texte.
    Paramètres:
    text (str): Le texte à nettoyer.
    Retourne:
    str: Le texte sans les mots vides.
    """
    # Télécharger les stop words français si nécessaire
    # nltk.download('stopwords')
    
    # Récupérer les stop words français
    stop_words = set(stopwords.words('french'))
    
    # Séparer les mots et filtrer les stop words
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    return ' '.join(filtered_words)


def return_wordmap(data = data_final):
    """
    Génère un nuage de mots (word cloud) à partir des données fournies et l'affiche en utilisant Plotly.
    Paramètres:
    -----------
    data : DataFrame, optionnel
        Le DataFrame contenant les données à analyser. Par défaut, utilise data_final.
    Retourne:
    ---------
    fig : plotly.graph_objs._figure.Figure
        La figure Plotly contenant le nuage de mots généré.
    """
    # texte
    
    words_list = data[data['Si autres raison préciser'].notna()]['Si autres raison préciser'].\
        str.lower().str.strip().str.replace('eu','').\
        str.replace('une','').\
        str.replace('la','').str.replace('de ','').\
        str.replace('sur ','').str.replace('par','').tolist()
    text = ' '.join(words_list)
    text = remove_stop_words(text)

    # Créer un masque circulaire
    mask = create_circular_mask(800)  # Ajustez la taille selon vos besoins

    # Générer le word cloud avec le masque
    wordcloud = WordCloud(width=800, height=800, background_color='white', mask=mask).generate(text)

    # Convertir le word cloud en image
    wordcloud_image = wordcloud.to_image()

    # Afficher le word cloud avec Plotly
    fig = px.imshow(wordcloud_image, title='Nuage de mots des raisons de non eligibilite', aspect='equal')
    fig.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(t=25, l=0, r=0, b=0),
        font_size=10
    )
    return fig



def return_wordmap_indispo(data =data_final):
    """
    Génère un nuage de mots (word cloud) basé sur les raisons d'indisponibilité fournies dans les données.
    Paramètres:
    -----------
    data : DataFrame, optionnel
        Le DataFrame contenant les données avec une colonne 'Autre raisons, preciser' qui contient les raisons d'indisponibilité.
    Retour:
    -------
    fig : plotly.graph_objects.Figure
        Une figure Plotly affichant le nuage de mots des raisons d'indisponibilité.
    """
    
    # texte
    words_list = data[data['Autre raisons,  preciser'].notna()]['Autre raisons,  preciser'].\
        str.lower().str.strip().str.replace('«\xa0diclojenal\xa0»','').\
        str.replace('«\xa0diclojenac\xa0»','')\
        .str.replace('et','').str.replace('pas ','').str.replace('aucune ','').tolist()


    text = ' '.join(words_list)

    # Créer un masque circulaire
    mask = create_circular_mask(800)  # Ajustez la taille selon vos besoins

    # Générer le word cloud avec le masque
    wordcloud = WordCloud(width=800, height=800, background_color='white', mask=mask).generate(text)

    # Convertir le word cloud en image
    wordcloud_image = wordcloud.to_image()

    # Afficher le word cloud avec Plotly
    fig = px.imshow(wordcloud_image, title='Nuage de mots des raisons d\'indisponibilité', aspect='equal')
    fig.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
        margin=dict(t=25, l=0, r=0, b=0)
    )
    return fig

 



def elegibilite_raison_plot(data=data_final):
    """
    Crée un graphique en camembert avec trous représentant la répartition du statut d'éligibilité au don.
    Paramètres:
    data (DataFrame): Le DataFrame contenant les données d'éligibilité. Par défaut, il utilise `data_final`.
    Retourne:
    fig0 (plotly.graph_objs._figure.Figure): Le graphique en camembert avec trous.
    """
    # Créer un DataFrame pour les valeurs d'éligibilité
    
    elegibilite_counts = data['ÉLIGIBILITÉ AU DON.'].value_counts().to_frame('total').reset_index()
    elegibilite_counts.columns = ['ÉLIGIBILITÉ AU DON', 'Total']

    # Créer un graphique en camembert avec trous
    fig0 = px.pie(elegibilite_counts, values='Total', names='ÉLIGIBILITÉ AU DON', hole=0.5, 
                title='Répartition du <b>statut d\'éligibilité</b> au don')
                # Séparer une partie du camembert
    fig0.update_traces(pull=[0.1 if i == 1 else 0 for i in range(len(elegibilite_counts))])
    fig0.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30,l=0,r=0,b=0)
        )
    fig0.update_traces(marker_line_color='black',opacity=1,marker_line_width=1)
    return fig0




def plot_status_principal_raison(data= data_final):
    """
    Génère un graphique en entonnoir représentant les raisons de non-éligibilité par statut d'éligibilité.
    Paramètres:
    -----------
    data : DataFrame, optionnel
        Le DataFrame contenant les données à analyser. Par défaut, il utilise `data_final`.
    Retourne:
    ---------
    fig1 : plotly.graph_objs._figure.Figure
        Le graphique en entonnoir représentant les raisons de non-éligibilité par statut d'éligibilité.
    Notes:
    ------
    - La fonction gère les cas où une personne peut être non éligible pour plusieurs raisons.
    - Les raisons de non-éligibilité sont définies dans la liste `elegib`.
    - Le graphique est trié par le nombre total de non-éligibilités pour chaque raison.
    - La mise en page et les couleurs du graphique sont personnalisées.
    """
    ### il peut arriver qu une personne soit non eligible pour plusieurs raisons:ici nous gerons tous les cas
    
    elegib = [
    'Raison de non-eligibilité totale  [Antécédent de transfusion]',
    'Raison de non-eligibilité totale  [Porteur(HIV,hbs,hcv)]',
    'Raison de non-eligibilité totale  [Opéré]',
    'Raison de non-eligibilité totale  [Drepanocytaire]',
    'Raison de non-eligibilité totale  [Diabétique]',
    'Raison de non-eligibilité totale  [Hypertendus]',
    'Raison de non-eligibilité totale  [Asthmatiques]',
    'Raison de non-eligibilité totale  [Cardiaque]',
    'Raison de non-eligibilité totale  [Tatoué]',
    'Raison de non-eligibilité totale  [Scarifié]'
    ]

    data_elig = data[[elegib[0],'ÉLIGIBILITÉ AU DON.']].value_counts().reset_index()
    data_elig = data_elig[data_elig[elegib[0]]!='non']
    data_elig = data_elig.rename(columns={elegib[0]:'index'})
    for i in range(1,len(elegib)):
        s = data[[elegib[i],'ÉLIGIBILITÉ AU DON.']].value_counts().reset_index()
        s = s[s[elegib[i]]!='non']
        s = s.rename(columns={elegib[i]:'index'})
        data_elig = pd.concat([s,data_elig],axis=0)
        
    data_elegibi_value = data_elig.rename(columns={'index':'raison_indispo','count':'Total',
                                                'ÉLIGIBILITÉ AU DON.':'elegibilite'}).drop_duplicates()   

    fig1 = px.funnel(data_elegibi_value.sort_values(by='Total', ascending=False), x = 'Total', y ='raison_indispo', title = "'Raisons de non elegibilite par <b>status d\'éligibilité<b>'",color_discrete_sequence = ['red'], opacity = 1)

    fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    # Mettre à jour la mise en page
    fig1.update_layout(yaxis_title='Raison',
                    xaxis_title='Effectif',
                    legend_title='Éligibilité', margin=dict(t=30,l=0,r=0,b=0),
                    xaxis_tickangle=-45,
                    xaxis=dict(showgrid=False,title="",showticklabels=False))
    fig1.update_traces(marker_color='lightgreen',marker_line_color='black',opacity=1,marker_line_width=1)
    # Afficher le graphique
    return fig1



def plot_elegibi_raison_elegibi(data=data_final):
    # Créer une figure avec deux sous-parcelles
    """
    Creates a figure with two subplots to visualize the distribution of eligibility status and reasons for ineligibility.

    Parameters:
    -----------
    data : DataFrame, optional
        The data to use for generating the plots. Defaults to `data_final`.

    Returns:
    --------
    fig : plotly.graph_objs._figure.Figure
        The figure containing two subplots: a pie chart for eligibility status distribution and a bar chart for reasons of ineligibility.
    """

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Répartition du statut d'éligibilité", "Raisons de non éligibilité"),
                        specs=[[{'type': 'pie'}, {'type': 'bar'}]])

    # Ajouter le pie chart à la première sous-parcelle
    fig.add_trace(
        elegibilite_raison_plot(data=data).data[0],
        row=1, col=1
    )

    # Ajouter le bar chart à la deuxième sous-parcelle
    fig.add_trace(
        plot_status_principal_raison(data= data).data[0],
        row=1, col=2
    )

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                    , margin=dict(t=30,l=0,r=5,b=0),xaxis=dict(showgrid=False,title="",showticklabels=False),
                    yaxis=dict(
                            tickfont=dict(size=8))
                    )

    # Afficher la figure
    return fig




def plot_indispo_eligi(data=data_final):
    """
    Génère un graphique en entonnoir représentant les raisons d'indisponibilité par statut d'éligibilité.
    Paramètres:
    -----------
    data : DataFrame, optionnel
        Le DataFrame contenant les données à analyser. Par défaut, il utilise `data_final`.
    Retourne:
    ---------
    fig2 : plotly.graph_objs._figure.Figure
        Le graphique en entonnoir représentant les raisons d'indisponibilité par statut d'éligibilité.
    """
    
    ### il peut arriver qu une personne soit non eligible pour plusieurs raisons:ici nous gerons tous les cas
    elegib_liste = data.columns[data.columns.str.lower().str.startswith('raison indisponibilité')].tolist() 

    data_elig = data[[elegib_liste[0],'ÉLIGIBILITÉ AU DON.']].value_counts().reset_index()
    data_elig = data_elig[data_elig[elegib_liste[0]]!='non']
    data_elig = data_elig.rename(columns={elegib_liste[0]:'index'})
    for i in range(1,len(elegib_liste)):
        s = data[[elegib_liste[i],'ÉLIGIBILITÉ AU DON.']].value_counts().reset_index()
        s = s[s[elegib_liste[i]]!='non']
        s = s.rename(columns={elegib_liste[i]:'index'})
        data_elig = pd.concat([s,data_elig],axis=0)
        
    data_rindi_elegibi_value = data_elig.rename(columns={'index':'raison_indispo','count':'Total','ÉLIGIBILITÉ AU DON.':'elegibilite'})  

    data_rindi_elegibi_value['raison_indispo'] = data_rindi_elegibi_value['raison_indispo'].str.replace(' ', '<br>', 2)
    fig2 = px.funnel(data_rindi_elegibi_value.sort_values(by='Total', ascending=False),
                y='raison_indispo',
                x='Total',
                color='elegibilite',
                title='Raisons d\'indisponibilité par <b>status d\'éligibilité<b>')

    fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    # Mettre à jour la mise en page
    fig2.update_layout(yaxis_title='',
                    xaxis_title='',
                    legend_title='Éligibilité', margin=dict(t=30,l=0,r=0,b=0),
                    xaxis_tickangle=-45,
                    xaxis=dict(showgrid=False,title="",showticklabels=False))
    fig2.update_traces(marker_color='#E2691E',marker_line_color='black',opacity=1,marker_line_width=1)
    # Afficher le graphique
    return fig2



def raison_indispo_plot(data = data_final):
    """
    Crée une figure avec deux sous-parcelles pour visualiser la répartition du statut d'éligibilité et les raisons d'indisponibilité.
    Paramètres:
    -----------
    data : DataFrame, optionnel
        Les données à utiliser pour générer les graphiques. Par défaut, utilise `data_final`.
    Retourne:
    --------
    fig : plotly.graph_objs._figure.Figure
        La figure contenant les deux sous-parcelles : un pie chart pour la répartition du statut d'éligibilité et un bar chart pour les raisons d'indisponibilité.
    """
        
    # Créer une figure avec deux sous-parcelles
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Répartition du statut d'éligibilité", "Raisons d'indisponibilite"),
                        specs=[[{'type': 'pie'}, {'type': 'bar'}]],horizontal_spacing=0.1)

    # Ajouter le pie chart à la première sous-parcelle
    fig.add_trace(
        elegibilite_raison_plot(data=data).data[0],
        row=1, col=1
    )

    # Ajouter le bar chart à la deuxième sous-parcelle
    fig.add_trace(
        plot_indispo_eligi(data=data).data[0],
        row=1, col=2
    )

    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
                    , margin=dict(t=30,l=0,r=5,b=0),xaxis=dict(showgrid=False,title="",showticklabels=False),
                    yaxis=dict(
                tickfont=dict(size=8)  # Réduire la taille de la police à 10
            )
        )

    # Afficher la figure
    return fig



def plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion']):
    """
    Crée un diagramme Sankey pour visualiser les relations entre les variables démographiques et l'éligibilité au don.
    Args:
        data_don (pd.DataFrame): Le dataframe contenant les données à analyser. Par défaut, il utilise `data_final`.
        cols (list): Liste des colonnes à inclure dans le diagramme Sankey. Par défaut, ['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'].
    Returns:
        plotly.graph_objs._figure.Figure: Un objet Figure contenant le diagramme Sankey.
    Exemple:
        fig = plot_ruban(data_don=my_dataframe, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'])
        fig.show()
    """
    df = data_don[cols]
    
    # Préparation des données pour le diagramme Sankey
    links = []
    source_idx = 0
    target_idx = 0
    
    # Pour stocker les nœuds uniques
    all_nodes = []
    node_indices = {}
    
    # Récupérer tous les nœuds uniques et assigner des indices
    for i in range(len(cols) - 1):
        source_col = cols[i]
        target_col = cols[i + 1]
        
        # Ajouter les valeurs uniques de la colonne source aux nœuds
        for val in df[source_col].unique():
            node_name = f"{source_col} - {val}"
            if node_name not in node_indices:
                node_indices[node_name] = len(all_nodes)
                all_nodes.append(node_name)
        
        # Ajouter les valeurs uniques de la dernière colonne cible
        if i == len(cols) - 2:
            for val in df[target_col].unique():
                node_name = f"{target_col} - {val}"
                if node_name not in node_indices:
                    node_indices[node_name] = len(all_nodes)
                    all_nodes.append(node_name)
    
    # Obtenir l'indice du nœud "Eligible"
    eligible_node = "ÉLIGIBILITÉ AU DON. - Eligible"
    eligible_index = node_indices.get(eligible_node, -1)
    
    # Créer les liens entre les nœuds avec les couleurs appropriées
    link_data = []
    link_colors = []
    
    # Filtrer d'abord le dataframe pour obtenir les lignes où ÉLIGIBILITÉ AU DON = Eligible
    eligible_df = df[df['ÉLIGIBILITÉ AU DON.'] == 'Eligible']
    
    for i in range(len(cols) - 1):
        source_col = cols[i]
        target_col = cols[i + 1]
        
        # Traiter d'abord les liens pour les personnes éligibles (en rose)
        if not eligible_df.empty:
            cross_tab_eligible = pd.crosstab(eligible_df[source_col], eligible_df[target_col])
            for source_val, row in cross_tab_eligible.iterrows():
                for target_val, count in row.items():
                    if count > 0:
                        source_node = f"{source_col} - {source_val}"
                        target_node = f"{target_col} - {target_val}"
                        source_idx = node_indices[source_node]
                        target_idx = node_indices[target_node]
                        
                        link_data.append({
                            'source': source_idx,
                            'target': target_idx,
                            'value': count
                        })
                        link_colors.append("rgba(255, 182, 193, 0.8)")  # Rose pour les éligibles
        
        # Traiter maintenant le dataframe complet pour les autres liens (en gris)
        cross_tab = pd.crosstab(df[source_col], df[target_col])
        for source_val, row in cross_tab.iterrows():
            for target_val, count in row.items():
                if count > 0:
                    # Vérifier si ce lien n'est pas déjà traité comme éligible
                    in_eligible = False
                    if not eligible_df.empty:
                        eligible_count = cross_tab_eligible.get(target_val, {}).get(source_val, 0)
                        if eligible_count == count:
                            in_eligible = True
                    
                    if not in_eligible:
                        source_node = f"{source_col} - {source_val}"
                        target_node = f"{target_col} - {target_val}"
                        source_idx = node_indices[source_node]
                        target_idx = node_indices[target_node]
                        
                        # Si le lien implique directement le nœud Eligible, colorer en rose
                        if source_node == eligible_node or target_node == eligible_node:
                            link_colors.append("rgba(255, 182, 193, 0.8)")  # Rose
                        else:
                            link_colors.append("rgba(211, 211, 211, 0.8)")  # Gris clair
                        
                        link_data.append({
                            'source': source_idx,
                            'target': target_idx,
                            'value': count
                        })
    
    # Création du diagramme Sankey avec couleurs personnalisées
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="blue"
        ),
        link=dict(
            source=[link['source'] for link in link_data],
            target=[link['target'] for link in link_data],
            value=[link['value'] for link in link_data],
            color=link_colors
        )
    )])
    
    # Mise en page du graphique
    fig.update_layout(
        title_text="Relations entre variables démographiques et éligibilité au don",
        font_size=10,
        width=900,
        height=500,
        margin=dict(t=30,l=0,r=5,b=0)
        
    )
    

    
    return fig




def plot_combined_eligibility_heatmap(df, numeric_vars=['Age'],
                                      cat_vars=['Genre', 'Situation Matrimoniale (SM)', 'Religion',"Niveau d'etude", 'A-t-il (elle) déjà donné le sang'] ,
                                      eligibility_column='ÉLIGIBILITÉ AU DON.'): 
    
    """
    Trace une heatmap combinée des profils d'éligibilité par cluster et statut d'éligibilité.
    Cette fonction crée une heatmap qui compare les profils des individus en fonction de leurs variables numériques et catégorielles,
    regroupés par cluster et statut d'éligibilité. Les valeurs des variables numériques sont normalisées entre 0 et 1, et les proportions
    des modalités des variables catégorielles sont calculées.
    Paramètres:
    -----------
    df : pandas.DataFrame
        Le dataframe contenant les données à analyser.
    numeric_vars : list, optionnel
        Liste des noms des variables numériques à inclure dans l'analyse. Par défaut ['Age'].
    cat_vars : list, optionnel
        Liste des noms des variables catégorielles à inclure dans l'analyse. Par défaut ['Genre', 'Situation Matrimoniale (SM)', 'Religion', "Niveau d'etude", 'A-t-il (elle) déjà donné le sang'].
    eligibility_column : str, optionnel
        Le nom de la colonne indiquant le statut d'éligibilité. Par défaut 'ÉLIGIBILITÉ AU DON.'.
    Retour:
    -------
    fig : plotly.graph_objects.Figure
        La figure Plotly contenant la heatmap des profils d'éligibilité.
    """
    df['ÉLIGIBILITÉ AU DON.'] = data_final['ÉLIGIBILITÉ AU DON.']
    # Statuts d'éligibilité uniques
    eligibility_statuses = sorted(df[eligibility_column].unique())
    
    # Préparer le dataframe pour la heatmap
    profiles = []
    
    # Moyennes normalisées des variables numériques
    for var in numeric_vars:
        var_min = df[var].min()
        var_max = df[var].max()
        
        # Pour chaque combinaison de cluster et statut d'éligibilité
        for cluster in sorted(df['Cluster'].unique()):
            for status in eligibility_statuses:
                # Filtrer les données par cluster et statut d'éligibilité
                filtered_data = df[(df['Cluster'] == cluster) & (df[eligibility_column] == status)]
                
                if len(filtered_data) > 0:
                    cluster_mean = filtered_data[var].mean()
                    # Normaliser entre 0 et 1
                    norm_value = (cluster_mean - var_min) / (var_max - var_min) if var_max > var_min else 0
                    
                    # Créer une étiquette de colonne combinant cluster et statut
                    column_label = f"C{cluster}-{status}"
                    
                    profiles.append({
                        'Combinaison': column_label,
                        'Variable': f"{var} (moy)",
                        'Valeur': norm_value,
                        'Texte': f"{cluster_mean:.1f}",
                        'Cluster': cluster,
                        'Status': status
                    })
    
    # Proportions des modalités pour les variables catégorielles
    for var in cat_vars:
        for cluster in sorted(df['Cluster'].unique()):
            for status in eligibility_statuses:
                # Filtrer les données par cluster et statut d'éligibilité
                filtered_data = df[(df['Cluster'] == cluster) & (df[eligibility_column] == status)]
                
                if len(filtered_data) > 0:
                    # Calculer la proportion de chaque modalité
                    for cat in sorted(df[var].unique()):
                        prop = (filtered_data[var] == cat).mean() if len(filtered_data) > 0 else 0
                        
                        # Créer une étiquette de colonne combinant cluster et statut
                        column_label = f"C{cluster}-{status}"
                        
                        profiles.append({
                            'Combinaison': column_label,
                            'Variable': f"{var}: {cat}",
                            'Valeur': prop,
                            'Texte': f"{prop:.1%}",
                            'Cluster': cluster,
                            'Status': status
                        })
    
    # Convertir en dataframe
    profile_df = pd.DataFrame(profiles)
    
    # Pivoter pour créer une matrice
    heatmap_df = profile_df.pivot(index='Variable', columns='Combinaison', values='Valeur')
    text_df = profile_df.pivot(index='Variable', columns='Combinaison', values='Texte')
    
    # Organiser les colonnes par cluster puis par statut d'éligibilité pour une meilleure visualisation
    ordered_cols = []
    for cluster in sorted(df['Cluster'].unique()):
        for status in eligibility_statuses:
            col = f"C{cluster}-{status}"
            if col in heatmap_df.columns:
                ordered_cols.append(col)
    
    heatmap_df = heatmap_df[ordered_cols]
    text_df = text_df[ordered_cols]
    
    # Créer la heatmap
    fig = px.imshow(heatmap_df,
                   labels=dict(x="Cluster - Statut d'éligibilité", y="Variable", color="Valeur"),
                   x=heatmap_df.columns,
                   y=heatmap_df.index,
                   color_continuous_scale='Blues',
                   aspect="auto")
    
    # Ajouter les valeurs comme annotations
    annotations = []
    for i, var in enumerate(heatmap_df.index):
        for j, combo in enumerate(heatmap_df.columns):
            annotations.append(
                dict(
                    x=combo,
                    y=var,
                    text=text_df.loc[var, combo],
                    showarrow=False,
                    font=dict(color="white" if heatmap_df.loc[var, combo] > 0.5 else "black")
                )
            )
    
    # Ajouter des lignes verticales pour séparer les clusters
    shapes = []
    curr_cluster = None
    for i, col in enumerate(ordered_cols):
        cluster = col.split('-')[0]
        if i > 0 and cluster != curr_cluster:
            shapes.append(
                dict(
                    type="line",
                    x0=i-0.5, y0=-0.5,
                    x1=i-0.5, y1=len(heatmap_df.index)-0.5,
                    line=dict(color="black", width=2)
                )
            )
        curr_cluster = cluster
    
    # Créer une légende personnalisée pour les statuts d'éligibilité
    status_map = {
        'Eligible': 'E',
        'Temporairement Non-eligible': 'TNE',
        'Définitivement non-eligible': 'DNE'
    }
    
    # Créer des étiquettes plus courtes et informatives pour l'axe x
    x_ticks = []
    for combo in ordered_cols:
        parts = combo.split('-')
        cluster = parts[0].replace('C', '')
        status = '-'.join(parts[1:])
        # Utiliser l'abréviation du statut si disponible
        status_abbr = status_map.get(status, status)
        x_ticks.append(f"{cluster}-{status_abbr}")
    
    fig.update_layout(
        title="Comparaison des profils par cluster et statut d'éligibilité",
        annotations=annotations,
        shapes=shapes,
        xaxis_tickangle=-45,
        xaxis_ticktext=x_ticks,
        xaxis_tickvals=list(range(len(ordered_cols))),
        title_x=0.5,
        height=max(700, 30 * len(heatmap_df.index)),  # Ajuster la hauteur selon le nombre de variables
        width=max(800, 80 * len(ordered_cols))  # Ajuster la largeur selon le nombre de colonnes
        ,font=dict(size=10),
        margin={"r": 0, "t": 26, "l": 0, "b": 0},
        yaxis=dict(
            tickfont=dict(size=6)
        )
    )
    
    # Ajouter une légende pour les abréviations des statuts
    legend_text = "<br>".join([f"{v}: {k}" for k, v in status_map.items()])
    fig.add_annotation(
        x=-0.48, y=1.0,
        xref="paper", yref="paper",
        text=f"Légende:<br>{legend_text}", 
        showarrow=False,
        align="left",
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    return fig



def plot_cluster_distribution(df):
    
    """
    Plots the distribution of clusters in a pie chart.

    This function takes a DataFrame containing cluster information and plots the distribution of clusters
    using a pie chart with a hole in the center. The pie chart highlights one of the clusters by pulling it out slightly.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the cluster information. It must have a column named 'Cluster'.

    Returns:
    None: This function does not return any value. It displays the pie chart using Plotly.
    """
    
    df['Cluster'] = df['Cluster'].astype(str)
    data_clus = ('cluster ' + df.Cluster.astype(str)).value_counts().reset_index()
    data_clus.columns = ['Cluster', 'count']
    
    # Créer un graphique en camembert avec trous
    fig0 = px.pie(data_clus, values='count', names='Cluster', hole=0.5, 
                  title='Répartition des donneurs de sang par Cluster')
    # Séparer une partie du camembert
    fig0.update_traces(pull=[0.1 if i == 1 else 0 for i in range(len(data_clus))])
    fig0.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=30, l=0, r=0, b=0)
    )
    fig0.update_traces(marker_line_color='black', opacity=1, marker_line_width=1)
    return fig0


def create_treemap(df=data_final):
    # Créer un treemap hiérarchique personnalisé pour les dons de sang
    """
    Crée un treemap hiérarchique personnalisé pour les dons de sang.

    Ce treemap montre la hiérarchie et la composition des donneurs de sang par sexe, type de donation et groupe sanguin.
    Les couleurs sont choisies pour rappeler le sang et sont liées à l'âge moyen des donneurs.

    Parameters:
        df (pandas.DataFrame): Le DataFrame contenant les données des donneurs de sang. Par défaut, il utilise `data_final`.

    Returns:
        plotly.graph_objects._figure.Figure: Le treemap personnalisé.
    """
    fig_treemap = px.treemap(df,
                              path=['Sexe', 'Type de donation', 'Groupe Sanguin ABO / Rhesus'],
                              values='Age',
                              color='Age',
                              color_continuous_scale='YlGnBu',  # Échelle de couleurs rappelant le sang
                              title='Hiérarchie et Composition des Donneurs de Sang',
                              hover_data={
                                  'Sexe': True,
                                  'Type de donation': True,
                                  'Groupe Sanguin ABO / Rhesus': True,
                                  'Age': ':.0f'  # Afficher l'âge sans décimales
                              })
    
    # Personnalisation du layout pour un thème plus médical/don du sang
    fig_treemap.update_layout(
        title={
            'text': 'Hiérarchie et Composition des Donneurs de Sang',
            'font': {'size': 12, 'color': 'darkred'},
            'x': 0.5,  # Centrer le titre
            'xanchor': 'center'
        },
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="darkred"
        ),
        paper_bgcolor='rgba(255,240,240,0.8)',  # Fond légèrement rosé
        plot_bgcolor='rgba(255,240,240,0.8)',
        margin=dict(
        l=0,   
        r=0,   
        t=40,   
        b=0 )
    )
    
    # Personnalisation des hover labels
    fig_treemap.update_traces(
        hovertemplate='<b>%{label}</b><br>' +
                      'Sexe: %{customdata[0]}<br>' +
                      'Type de Donation: %{customdata[1]}<br>' +
                      'Groupe Sanguin: %{customdata[2]}<br>' +
                      'Âge Moyen: %{customdata[3]:.0f} ans<extra></extra>'
    )
    
    return fig_treemap


def create_age_distribution(df=data_final):
    """
    Crée un graphique en violon pour montrer la distribution de l'âge des donneurs de sang par sexe.

    Ce graphique montre la distribution de l'âge des donneurs de sang par sexe en utilisant des violons.
    Les couleurs sont choisies pour rappeler le sang et sont liées à l'âge moyen des donneurs.
    Les annotations statistiques sont également ajoutées pour montrer les moyennes, les médianes, les minima et les maxima.

    Parameters:
        df (pandas.DataFrame): Le DataFrame contenant les données des donneurs de sang. Par défaut, il utilise `data_final`.

    Returns:
        plotly.graph_objects._figure.Figure: Le graphique en violon.
    """
    
    fig_age = go.Figure()
    
    # Palette de couleurs médicales
    color_map = {
        'M': '#8B0000',  # Dark Red for Males
        'F': '#B22222'   # Firebrick for Females
    }
    
    # Distribution par sexe
    for sexe in df['Sexe'].unique():
        subset = df[df['Sexe'] == sexe]
        
        fig_age.add_trace(go.Violin(
            x=subset['Sexe'],
            y=subset['Age'],
            name=sexe,
            line_color=color_map[sexe],
            fillcolor=color_map[sexe],
            opacity=0.6,
            box_visible=True,
            meanline_visible=True,
            points='all',  # Show all points
            pointpos=0,  # Position of points
            jitter=0.05  # Add some jitter to points
        ))
    
    # Mise à jour du layout
    fig_age.update_layout(
        title={
            'text': 'Distribution de l\'Âge des Donneurs par Sexe',
            'font': {
                'size': 12, 
                'color': '#4A0E0E',  # Very dark red
                'family': 'Arial Black'
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title='Âge',
        xaxis_title='',
        violinmode='overlay',
        plot_bgcolor='rgba(255,245,245,0.9)',  # Light pink background
        paper_bgcolor='rgba(255,245,245,0.9)',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#4A0E0E"
        ),margin=dict(
        l=0,   
        r=0,   
        t=40,   
        b=0   
    )
    )
    
    # Ajouter des annotations statistiques
    stats_by_sex = df.groupby('Sexe')['Age'].agg(['mean', 'median', 'min', 'max'])
    
    # Annotations de statistiques
    annotations = [
        dict(
            xref='paper', yref='paper',
            x=0.5, y=-0.15,
            text=(
                f"Statistiques | Homme: Moy={stats_by_sex.loc['M', 'mean']:.1f}, "
                f"Méd={stats_by_sex.loc['M', 'median']:.1f} | "
                f"Femme: Moy={stats_by_sex.loc['F', 'mean']:.1f}, "
                f"Méd={stats_by_sex.loc['F', 'median']:.1f}"
            ),
            showarrow=False,
            font=dict(size=10, color='gray')
        )
    ]
    
    fig_age.update_layout(annotations=annotations)
    
    return fig_age

