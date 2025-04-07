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
import colorsys

### pour gérer le téléchargement des stopwords
try:
    a = set(stopwords.words('french'))
except:
    nltk.download('stopwords')    

# Dictionnaire de traduction pour les titres des graphiques
GRAPH_TRANSLATIONS = {
    'fr': {
        "Nuage de mots des raisons de non eligibilite": "Nuage de mots des raisons de non eligibilite",
        "Nuage de mots des raisons d'indisponibilité": "Nuage de mots des raisons d'indisponibilité",
        # ... (reste du dictionnaire inchangé)
    },
    'en': {
        "Nuage de mots des raisons de non eligibilite": "Word cloud of ineligibility reasons",
        "Nuage de mots des raisons d'indisponibilité": "Word cloud of unavailability reasons",
        # ... (reste du dictionnaire inchangé)
    }
}

# Définition des palettes de couleurs thématiques pour le don de sang
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
THEME_PALETTES = {
    'light': {
        'background': '#FFFFFF',
        'cardBackground': '#F5F5F5',
        'text': '#212121',
        'gridLines': '#E0E0E0',
        'pieHole': '#F5F5F5',
        'eligible': '#4CAF50',           # Vert pour éligible
        'temp_ineligible': '#FF9800',    # Orange pour temporairement non éligible
        'ineligible': '#F44336'          # Rouge pour définitivement non éligible
    },
    'dark': {
        'background': '#121212',
        'cardBackground': '#1E1E1E',
        'text': '#FFFFFF',
        'gridLines': '#424242',
        'pieHole': '#1E1E1E',
        'eligible': '#81C784',           # Vert plus clair pour éligible
        'temp_ineligible': '#FFB74D',    # Orange plus clair pour temporairement non éligible
        'ineligible': '#E57373'          # Rouge plus clair pour définitivement non éligible
    }
}

# Fonction pour créer un dégradé de couleurs
def create_color_gradients(base_color, steps=5, lighten=True):
    """Crée un dégradé de couleurs à partir d'une couleur de base"""
    h, l, s = colorsys.rgb_to_hls(*[int(base_color[i:i+2], 16)/255 for i in (1, 3, 5)])
    
    result = []
    for i in range(steps):
        if lighten:
            new_l = l + (1-l) * (i / (steps-1))
        else:
            new_l = l * (1 - i / (steps-1))
        
        r, g, b = colorsys.hls_to_rgb(h, new_l, s)
        result.append(f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')
    
    return result

def hex_to_rgba(hex_color, alpha=1.0):
    """Convertit une couleur hexadécimale en format rgba avec transparence"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f'rgba({r}, {g}, {b}, {alpha})'

def create_circular_mask(size):
    """Crée un masque circulaire pour une image carrée de taille donnée."""
    x, y = np.ogrid[:size, :size]
    mask = (x - size / 2) ** 2 + (y - size / 2) ** 2 > (size / 2) ** 2
    mask = 255 * mask.astype(int)  # 0 pour le cercle, 255 pour le reste
    return mask

def remove_stop_words(text):
    """Supprime les mots vides (stop words) français du texte."""
    stop_words = set(stopwords.words('french'))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def return_wordmap(data=data_final, language="fr", theme='light'):
    """Génère un nuage de mots élégant à partir des raisons de non-éligibilité."""
    # Traduction
    title = "Nuage de mots des raisons de non eligibilite"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Récupération et nettoyage du texte
    words_list = data[data['Si autres raison préciser'].notna()]['Si autres raison préciser'].\
        str.lower().str.strip().str.replace('eu','').\
        str.replace('une','').\
        str.replace('la','').str.replace('de ','').\
        str.replace('sur ','').str.replace('par','').tolist()
    text = ' '.join(words_list)
    text = remove_stop_words(text)

    # Créer un masque circulaire
    mask = create_circular_mask(800)

    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Générer le word cloud avec le masque et un dégradé de couleurs rouge sang
    colormap = px.colors.sequential.Reds
    wordcloud = WordCloud(
        width=800, 
        height=800, 
        background_color=theme_colors['background'],
        mask=mask,
        contour_width=1,
        contour_color=theme_colors['gridLines'],
        colormap='Reds',  # Utiliser une palette de rouges
        prefer_horizontal=0.9,
        max_font_size=100,
        random_state=42,
        collocations=False  # Éviter les duplications
    ).generate(text)

    # Convertir le word cloud en image
    wordcloud_image = wordcloud.to_image()

    # Afficher le word cloud avec Plotly
    fig = px.imshow(wordcloud_image, title=translated_title, aspect='equal')
    
    # Styliser la figure
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        margin=dict(t=50, l=0, r=0, b=0),
        font={'color': theme_colors['text'], 'family': 'Arial, sans-serif'}
    )
    
    return fig

def return_wordmap_indispo(data=data_final, language="fr", theme='light'):
    """Génère un nuage de mots élégant à partir des raisons d'indisponibilité."""
    # Traduction
    title = "Nuage de mots des raisons d'indisponibilité"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Récupération et nettoyage du texte
    words_list = data[data['Autre raisons,  preciser'].notna()]['Autre raisons,  preciser'].\
        str.lower().str.strip().str.replace('«\xa0diclojenal\xa0»','').\
        str.replace('«\xa0diclojenac\xa0»','')\
        .str.replace('et','').str.replace('pas ','').str.replace('aucune ','').tolist()
    text = ' '.join(words_list)
    text = remove_stop_words(text)

    # Créer un masque circulaire
    mask = create_circular_mask(800)

    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Générer le word cloud avec le masque et un dégradé de couleurs orange/ambre
    wordcloud = WordCloud(
        width=800, 
        height=800, 
        background_color=theme_colors['background'],
        mask=mask,
        contour_width=1,
        contour_color=theme_colors['gridLines'],
        colormap='YlOrBr',  # Utiliser une palette orange/ambre
        prefer_horizontal=0.9,
        max_font_size=100,
        random_state=42,
        collocations=False  # Éviter les duplications
    ).generate(text)

    # Convertir le word cloud en image
    wordcloud_image = wordcloud.to_image()

    # Afficher le word cloud avec Plotly
    fig = px.imshow(wordcloud_image, title=translated_title, aspect='equal')
    
    # Styliser la figure
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        margin=dict(t=50, l=0, r=0, b=0),
        font={'color': theme_colors['text'], 'family': 'Arial, sans-serif'}
    )
    
    return fig

def elegibilite_raison_plot(data=data_final, language="fr", theme='light'):
    """Crée un graphique en camembert amélioré pour la répartition du statut d'éligibilité."""
    # Traduction
    title = "Répartition du statut d'éligibilité au don"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Créer un DataFrame pour les valeurs d'éligibilité
    elegibilite_counts = data['ÉLIGIBILITÉ AU DON.'].value_counts().to_frame('total').reset_index()
    elegibilite_counts.columns = ['ÉLIGIBILITÉ AU DON', 'Total']
    
    # Palette de couleurs spécifiques pour chaque statut d'éligibilité
    color_map = {
        'Eligible': theme_colors['eligible'],
        'Temporairement Non-eligible': theme_colors['temp_ineligible'],
        'Définitivement non-eligible': theme_colors['ineligible']
    }
    
    # Créer une liste de couleurs dans l'ordre des valeurs du DataFrame
    colors = [color_map.get(status, '#BDBDBD') for status in elegibilite_counts['ÉLIGIBILITÉ AU DON']]
    
    # Créer un graphique en camembert avec trous
    fig = px.pie(
        elegibilite_counts, 
        values='Total', 
        names='ÉLIGIBILITÉ AU DON', 
        hole=0.6,  # Trou plus grand pour un look moderne
        title=translated_title,
        color_discrete_sequence=colors  # Utiliser notre palette personnalisée
    )
    
    # Mettre en valeur certaines parties du camembert
    pull_values = []
    for status in elegibilite_counts['ÉLIGIBILITÉ AU DON']:
        if status == 'Eligible':
            pull_values.append(0.1)  # Tirer légèrement le segment "Eligible"
        else:
            pull_values.append(0.0)
    
    fig.update_traces(
        pull=pull_values,
        marker=dict(
            line=dict(color=theme_colors['gridLines'], width=2)
        ),
        opacity=0.9,
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(
            family='Arial, sans-serif',
            size=14,
            color='white'
        ),
        hoverinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>%{percent}<br>Nombre: %{value}<extra></extra>'
    )
    
    # Ajouter des annotations pour un look plus professionnel
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            ),
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin=dict(t=80, l=0, r=0, b=40),
        annotations=[
            dict(
                text='STATUT<br>D\'ÉLIGIBILITÉ',
                x=0.5,
                y=0.5,
                font=dict(
                    family='Arial, sans-serif',
                    size=16,
                    color=theme_colors['text']
                ),
                showarrow=False
            )
        ]
    )
    
    return fig

def plot_status_principal_raison(data=data_final, language="fr", theme='light'):
    """Génère un graphique en entonnoir élégant pour les raisons de non-éligibilité."""
    # Traduction
    title = "Raisons de non eligibilite par status d'éligibilité"
    reason_label = "Raison"
    count_label = "Effectif"
    eligibility_label = "Éligibilité"
    
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    translated_reason = GRAPH_TRANSLATIONS[language].get(reason_label, reason_label)
    translated_count = GRAPH_TRANSLATIONS[language].get(count_label, count_label)
    translated_eligibility = GRAPH_TRANSLATIONS[language].get(eligibility_label, eligibility_label)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Traitement des données pour le graphique en entonnoir
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
    
    # Créer un dégradé de couleurs basé sur la palette primaire
    colors_gradient = px.colors.sequential.Reds_r  # Dégradé de rouges inversé
    
    # Nettoyer les noms des raisons pour plus de lisibilité
    data_elegibi_value['raison_indispo'] = data_elegibi_value['raison_indispo'].str.replace('Raison de non-eligibilité totale  \[', '')
    data_elegibi_value['raison_indispo'] = data_elegibi_value['raison_indispo'].str.replace('\]', '')
    
    # Créer un graphique en entonnoir amélioré
    fig = px.funnel(
        data_elegibi_value.sort_values(by='Total', ascending=False),
        x='Total',
        y='raison_indispo',
        title=translated_title,
        color_discrete_sequence=colors_gradient,
        opacity=0.9,
        height=500
    )
    
    # Ajouter des bordures et des effets visuels pour améliorer l'esthétique
    fig.update_traces(
        marker=dict(
            line=dict(
                color=theme_colors['gridLines'],
                width=1
            )
        ),
        textposition="auto",
        texttemplate='%{x}',
        textfont=dict(
            family='Arial, sans-serif',
            size=12,
            color='white'
        ),
        hovertemplate='<b>%{y}</b><br>Nombre: %{x}<extra></extra>'
    )
    
    # Améliorer la mise en page pour un aspect professionnel
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        yaxis_title={
            'text': translated_reason,
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': theme_colors['text']
            }
        },
        xaxis_title={
            'text': translated_count,
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': theme_colors['text']
            }
        },
        legend_title={
            'text': translated_eligibility,
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': theme_colors['text']
            }
        },
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin=dict(t=80, l=0, r=0, b=0),
        yaxis=dict(
            gridcolor=theme_colors['gridLines'],
            tickfont=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            )
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=theme_colors['gridLines'],
            zeroline=True,
            zerolinecolor=theme_colors['gridLines'],
            tickfont=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            )
        ),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    return fig

def plot_elegibi_raison_elegibi(data=data_final, language="fr", theme='light'):
    """Crée une figure avec deux sous-graphiques améliorés pour l'éligibilité et les raisons d'inéligibilité."""
    # Traduction
    subtitle1 = "Répartition du statut d'éligibilité"
    subtitle2 = "Raisons de non éligibilité"
    
    translated_subtitle1 = GRAPH_TRANSLATIONS[language].get(subtitle1, subtitle1)
    translated_subtitle2 = GRAPH_TRANSLATIONS[language].get(subtitle2, subtitle2)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Créer une figure avec deux sous-parcelles
    fig = make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=(
            f'<b>{translated_subtitle1}</b>',
            f'<b>{translated_subtitle2}</b>'
        ),
        specs=[[{'type': 'pie'}, {'type': 'bar'}]],
        horizontal_spacing=0.1
    )

    # Ajouter le pie chart à la première sous-parcelle
    pie_fig = elegibilite_raison_plot(data=data, language=language, theme=theme)
    fig.add_trace(pie_fig.data[0], row=1, col=1)

    # Ajouter le bar chart à la deuxième sous-parcelle
    bar_fig = plot_status_principal_raison(data=data, language=language, theme=theme)
    fig.add_trace(bar_fig.data[0], row=1, col=2)
    
    # Améliorer la mise en page globale
    fig.update_layout(
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        font=dict(
            family='Arial, sans-serif',
            size=12,
            color=theme_colors['text']
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1,
            font=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ),
        margin=dict(t=80, l=0, r=0, b=40),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    # Mettre à jour les propriétés du graphique en camembert
    fig.update_traces(
        hole=0.6,
        marker=dict(
            line=dict(color=theme_colors['gridLines'], width=1)
        ),
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(
            family='Arial, sans-serif',
            size=11,
            color='white'
        ),
        selector=dict(type='pie')
    )
    
    # Mettre à jour les propriétés du graphique en barres
    fig.update_traces(
        marker=dict(
            color=px.colors.sequential.Reds_r,
            line=dict(color=theme_colors['gridLines'], width=1)
        ),
        texttemplate='%{x}',
        selector=dict(type='funnel')
    )
    
    # Mettre à jour les axes du graphique en barres
    fig.update_yaxes(
        title_text="",
        tickfont=dict(
            family='Arial, sans-serif',
            size=10,
            color=theme_colors['text']
        ),
        gridcolor=theme_colors['gridLines'],
        row=1, 
        col=2
    )
    
    fig.update_xaxes(
        title_text="",
        showticklabels=False,
        gridcolor=theme_colors['gridLines'],
        zeroline=True,
        zerolinecolor=theme_colors['gridLines'],
        row=1, 
        col=2
    )
    
    return fig

def plot_indispo_eligi(data=data_final, language="fr", theme='light'):
    """Génère un graphique en entonnoir amélioré pour les raisons d'indisponibilité."""
    # Traduction
    title = "Raisons d'indisponibilité par status d'éligibilité"
    reason_label = "Raison"
    count_label = "Effectif"
    eligibility_label = "Éligibilité"
    
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    translated_reason = GRAPH_TRANSLATIONS[language].get(reason_label, reason_label)
    translated_count = GRAPH_TRANSLATIONS[language].get(count_label, count_label)
    translated_eligibility = GRAPH_TRANSLATIONS[language].get(eligibility_label, eligibility_label)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Traitement des données pour le graphique en entonnoir
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

    # Nettoyer et formater les labels pour plus de lisibilité
    data_rindi_elegibi_value['raison_indispo'] = data_rindi_elegibi_value['raison_indispo'].str.replace(' ', '<br>', 2)
    
    # Palette de couleurs pour les différents statuts d'éligibilité
    color_map = {
        'Eligible': theme_colors['eligible'],
        'Temporairement Non-eligible': theme_colors['temp_ineligible'],
        'Définitivement non-eligible': theme_colors['ineligible']
    }
    
    # Créer une liste de couleurs distinctes pour chaque statut d'éligibilité
    color_discrete_map = {status: color_map.get(status, '#BDBDBD') for status in data_rindi_elegibi_value['elegibilite'].unique()}
    
    # Créer un graphique en entonnoir amélioré
    fig = px.funnel(
        data_rindi_elegibi_value.sort_values(by='Total', ascending=False),
        y='raison_indispo',
        x='Total',
        color='elegibilite',
        title=translated_title,
        color_discrete_map=color_discrete_map,
        opacity=0.9,
        height=500
    )
    
    # Ajouter des bordures et des effets visuels pour améliorer l'esthétique
    fig.update_traces(
        marker=dict(
            line=dict(
                color=theme_colors['gridLines'],
                width=1
            )
        ),
        textposition="auto",
        texttemplate='%{x}',
        textfont=dict(
            family='Arial, sans-serif',
            size=12,
            color='white'
        ),
        hovertemplate='<b>%{y}</b><br>%{fullData.name}: %{x}<extra></extra>'
    )
    
    # Améliorer la mise en page pour un aspect professionnel
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        yaxis_title={
            'text': translated_reason,
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': theme_colors['text']
            }
        },
        xaxis_title={
            'text': translated_count,
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': theme_colors['text']
            }
        },
        legend_title={
            'text': translated_eligibility,
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': theme_colors['text']
            }
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1,
            font=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin=dict(t=80, l=0, r=0, b=40),
        yaxis=dict(
            gridcolor=theme_colors['gridLines'],
            tickfont=dict(
                family='Arial, sans-serif',
                size=11,
                color=theme_colors['text']
            )
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=theme_colors['gridLines'],
            zeroline=True,
            zerolinecolor=theme_colors['gridLines'],
            tickfont=dict(
                family='Arial, sans-serif',
                size=11,
                color=theme_colors['text']
            ),
            showticklabels=False  # Masquer les étiquettes de l'axe x
        ),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    return fig

def raison_indispo_plot(data=data_final, language="fr", theme='light'):
    """Crée une figure avec deux sous-graphiques améliorés pour l'éligibilité et les raisons d'indisponibilité."""
    # Traduction
    subtitle1 = "Répartition du statut d'éligibilité"
    subtitle2 = "Raisons d'indisponibilité"
    
    translated_subtitle1 = GRAPH_TRANSLATIONS[language].get(subtitle1, subtitle1)
    translated_subtitle2 = GRAPH_TRANSLATIONS[language].get(subtitle2, subtitle2)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Créer une figure avec deux sous-parcelles
    fig = make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=(
            f'<b>{translated_subtitle1}</b>',
            f'<b>{translated_subtitle2}</b>'
        ),
        specs=[[{'type': 'pie'}, {'type': 'bar'}]],
        horizontal_spacing=0.1
    )

    # Ajouter le pie chart à la première sous-parcelle
    pie_fig = elegibilite_raison_plot(data=data, language=language, theme=theme)
    fig.add_trace(pie_fig.data[0], row=1, col=1)

    # Ajouter le bar chart à la deuxième sous-parcelle
    bar_fig = plot_indispo_eligi(data=data, language=language, theme=theme)
    for trace in bar_fig.data:
        fig.add_trace(trace, row=1, col=2)
    
    # Améliorer la mise en page globale
    fig.update_layout(
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        font=dict(
            family='Arial, sans-serif',
            size=12,
            color=theme_colors['text']
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1,
            font=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ),
        margin=dict(t=80, l=0, r=0, b=60),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    # Mettre à jour les propriétés du graphique en camembert
    fig.update_traces(
        hole=0.6,
        marker=dict(
            line=dict(color=theme_colors['gridLines'], width=1)
        ),
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(
            family='Arial, sans-serif',
            size=11,
            color='white'
        ),
        selector=dict(type='pie')
    )
    
    # Mettre à jour les axes du graphique en barres
    fig.update_yaxes(
        title_text="",
        tickfont=dict(
            family='Arial, sans-serif',
            size=10,
            color=theme_colors['text']
        ),
        gridcolor=theme_colors['gridLines'],
        row=1, 
        col=2
    )
    
    fig.update_xaxes(
        title_text="",
        showticklabels=False,
        gridcolor=theme_colors['gridLines'],
        zeroline=True,
        zerolinecolor=theme_colors['gridLines'],
        row=1, 
        col=2
    )
    
    return fig

def plot_ruban(data_don=data_final, cols=['Genre', 'ÉLIGIBILITÉ AU DON.', 'Religion'], language="fr", theme='light'):
    """Crée un diagramme Sankey amélioré pour visualiser les relations entre variables démographiques et éligibilité."""
    # Traduction
    title = "Relations entre variables démographiques et éligibilité au don"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
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
    
    # Créer des couleurs personnalisées pour les nœuds
    node_colors = []
    for node in all_nodes:
        col_type, value = node.split(' - ', 1)
        
        if col_type == cols[0]:  # Premier niveau (ex: Genre)
            node_colors.append(BLOOD_PALETTE['primary'][1])  # Rouge
        elif col_type == cols[-1]:  # Dernier niveau (ex: Religion)
            node_colors.append(BLOOD_PALETTE['accent'][1])  # Turquoise
        else:  # Niveaux intermédiaires
            # Utiliser des couleurs différentes selon le statut d'éligibilité
            if value == 'Eligible':
                node_colors.append(theme_colors['eligible'])
            elif value == 'Temporairement Non-eligible':
                node_colors.append(theme_colors['temp_ineligible'])
            elif value == 'Définitivement non-eligible':
                node_colors.append(theme_colors['ineligible'])
            else:
                node_colors.append(BLOOD_PALETTE['secondary'][2])  # Bleu
    
    # Créer les liens entre les nœuds
    link_data = []
    link_colors = []
    
    for i in range(len(cols) - 1):
        source_col = cols[i]
        target_col = cols[i + 1]
        
        # Créer un tableau croisé pour obtenir les nombres
        cross_tab = pd.crosstab(df[source_col], df[target_col])
        
        for source_val, row in cross_tab.iterrows():
            for target_val, count in row.items():
                if count > 0:
                    source_node = f"{source_col} - {source_val}"
                    target_node = f"{target_col} - {target_val}"
                    source_idx = node_indices[source_node]
                    target_idx = node_indices[target_node]
                    
                    # Déterminer la couleur du lien
                    if target_node.startswith('ÉLIGIBILITÉ AU DON.'):
                        if target_val == 'Eligible':
                            link_color = hex_to_rgba(theme_colors['eligible'], 0.6)
                        elif target_val == 'Temporairement Non-eligible':
                            link_color = hex_to_rgba(theme_colors['temp_ineligible'], 0.6)
                        elif target_val == 'Définitivement non-eligible':
                            link_color = hex_to_rgba(theme_colors['ineligible'], 0.6)
                        else:
                            link_color = hex_to_rgba('#BDBDBD', 0.6)
                    else:
                        # Pour les autres liens, utiliser une couleur en fonction de la source
                        if source_node.startswith('ÉLIGIBILITÉ AU DON.'):
                            if source_val == 'Eligible':
                                link_color = hex_to_rgba(theme_colors['eligible'], 0.6)
                            elif source_val == 'Temporairement Non-eligible':
                                link_color = hex_to_rgba(theme_colors['temp_ineligible'], 0.6)
                            elif source_val == 'Définitivement non-eligible':
                                link_color = hex_to_rgba(theme_colors['ineligible'], 0.6)
                            else:
                                link_color = hex_to_rgba('#BDBDBD', 0.6)
                        else:
                            # Couleur par défaut pour les autres liens
                            link_color = hex_to_rgba(BLOOD_PALETTE['neutral'][2], 0.6)
                    
                    link_data.append({
                        'source': source_idx,
                        'target': target_idx,
                        'value': count
                    })
                    link_colors.append(link_color)
    
    # Création du diagramme Sankey amélioré
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',  # Arrangement amélioré
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color=theme_colors['gridLines'],
                width=0.5
            ),
            label=all_nodes,
            color=node_colors,
            hovertemplate='<b>%{label}</b><br>Total: %{value}<extra></extra>'
        ),
        link=dict(
            source=[link['source'] for link in link_data],
            target=[link['target'] for link in link_data],
            value=[link['value'] for link in link_data],
            color=link_colors,
            hovertemplate='<b>%{source.label}</b> → <b>%{target.label}</b><br>Valeur: %{value}<extra></extra>'
        )
    )])
    
    # Mise en page améliorée
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': theme_colors['text']
            }
        },
        font=dict(
            family='Arial, sans-serif',
            size=12,
            color=theme_colors['text']
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        width=900,
        height=550,
        margin=dict(t=80, l=20, r=20, b=20),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    # Ajouter une légende personnalisée
    #fig.add_annotation(
        #text=f"<b>Légende:</b><br>• Genre<br>• {cols[1]}<br>• {cols[2]}",
        #x=0.01,
        #y=0.99,
        #xref="paper",
        #yref="paper",
        #showarrow=False,
        #bgcolor=theme_colors['cardBackground'],
        #bordercolor=theme_colors['gridLines'],
        #borderwidth=1,
        #borderpad=6,
        #font=dict(
            #family='Arial, sans-serif',
            #size=10,
            #color=theme_colors['text']
        #),
        #align="left"
    #)
    
    return fig



def plot_combined_eligibility_heatmap(df, numeric_vars=['Age'],
                                      cat_vars=['Genre', 'Situation Matrimoniale (SM)', 'Religion',"Niveau d'etude", 'A-t-il (elle) déjà donné le sang'] ,
                                      eligibility_column='ÉLIGIBILITÉ AU DON.',
                                      language="fr", theme='light',
                                      significance_threshold=0.4): 
    """Trace une heatmap simplifiée des profils d'éligibilité par cluster et statut d'éligibilité."""
    # Traduction
    title = "Comparaison des profils par cluster et statut d'éligibilité"
    cluster_status_label = "Cluster - Statut d'éligibilité"
    variable_label = "Modalité"
    value_label = "Valeur"
    legend_label = "Légende"
    
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    translated_cluster_status = GRAPH_TRANSLATIONS[language].get(cluster_status_label, cluster_status_label)
    translated_variable = GRAPH_TRANSLATIONS[language].get(variable_label, variable_label)
    translated_value = GRAPH_TRANSLATIONS[language].get(value_label, value_label)
    translated_legend = GRAPH_TRANSLATIONS[language].get(legend_label, legend_label)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
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
                        'Variable': f"{var}",  # Afficher seulement le nom de la variable
                        'Valeur': norm_value,
                        'Cluster': cluster,
                        'Status': status,
                        'Type': 'numeric'
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
                            'Variable': f"{cat}",  # Afficher seulement la modalité
                            'Valeur': prop,
                            'Cluster': cluster,
                            'Status': status,
                            'Type': 'categorical',
                            'Parent': var  # Stocker la variable parente pour regroupement
                        })
    
    # Convertir en dataframe
    profile_df = pd.DataFrame(profiles)
    
    # Filtrer les modalités qui ne sont pas significatives
    significant_vars = []
    
    # Pour chaque modalité, vérifier si elle est significative dans au moins un cluster-statut
    for var in profile_df['Variable'].unique():
        var_data = profile_df[profile_df['Variable'] == var]
        
        # Une modalité est significative si sa valeur est supérieure au seuil dans au moins une combinaison
        if var_data['Valeur'].max() >= significance_threshold or var_data['Type'].iloc[0] == 'numeric':
            significant_vars.append(var)
    
    # Filtrer le dataframe pour ne garder que les variables significatives
    profile_df = profile_df[profile_df['Variable'].isin(significant_vars)]
    
    # Pivoter pour créer une matrice
    heatmap_df = profile_df.pivot(index='Variable', columns='Combinaison', values='Valeur')
    
    # Organiser les colonnes par cluster puis par statut d'éligibilité
    ordered_cols = []
    for cluster in sorted(df['Cluster'].unique()):
        for status in eligibility_statuses:
            col = f"C{cluster}-{status}"
            if col in heatmap_df.columns:
                ordered_cols.append(col)
    
    heatmap_df = heatmap_df[ordered_cols]
    
    # Choisir une palette de couleurs adaptée au thème
    if theme == 'dark':
        color_scale = [
            [0.0, "#081d58"],
            [0.1, "#253494"],
            [0.2, "#225ea8"],
            [0.3, "#1d91c0"],
            [0.4, "#41b6c4"],
            [0.5, "#7fcdbb"],
            [0.6, "#c7e9b4"],
            [0.7, "#edf8b1"],
            [0.8, "#ffffd9"],
            [1.0, "#ffffff"]
        ]
    else:
        color_scale = [
            [0.0, "#f7fbff"],
            [0.1, "#deebf7"],
            [0.2, "#c6dbef"],
            [0.3, "#9ecae1"],
            [0.4, "#6baed6"],
            [0.5, "#4292c6"],
            [0.6, "#2171b5"],
            [0.7, "#08519c"],
            [0.8, "#08306b"],
            [1.0, "#081d58"]
        ]
    
    # Créer la heatmap simplifiée (sans annotations textuelles)
    fig = px.imshow(
        heatmap_df,
        labels=dict(x=translated_cluster_status, y=translated_variable, color=translated_value),
        x=heatmap_df.columns,
        y=heatmap_df.index,
        color_continuous_scale=color_scale,
        aspect="auto",
        height=max(600, 25 * len(heatmap_df.index)),  # Ajuster la hauteur selon le nombre de variables
        width=max(800, 80 * len(ordered_cols))  # Ajuster la largeur selon le nombre de colonnes
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
                    line=dict(color=theme_colors['text'], width=2)
                )
            )
        curr_cluster = cluster
    
    # Créer une légende personnalisée pour les statuts d'éligibilité
    status_map = {
        'Eligible': 'E',
        'Temporairement Non-eligible': 'TNE',
        'Définitivement non-eligible': 'DNE'
    }
    
    # Créer des étiquettes plus courtes pour l'axe x
    x_ticks = []
    for combo in ordered_cols:
        parts = combo.split('-')
        cluster = parts[0].replace('C', '')
        status = '-'.join(parts[1:])
        # Utiliser l'abréviation du statut si disponible
        status_abbr = status_map.get(status, status)
        x_ticks.append(f"{cluster}-{status_abbr}")
    
    # Mise en page améliorée
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        shapes=shapes,  # Pas d'annotations textuelles
        xaxis=dict(
            tickangle=-45,
            tickmode='array',
            tickvals=list(range(len(ordered_cols))),
            ticktext=x_ticks,
            tickfont=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            ),
            gridcolor=theme_colors['gridLines'],
            title_font=dict(
                family='Arial, sans-serif',
                size=14,
                color=theme_colors['text']
            )
        ),
        yaxis=dict(
            tickfont=dict(
                family='Arial, sans-serif',
                size=9,
                color=theme_colors['text']
            ),
            gridcolor=theme_colors['gridLines'],
            title_font=dict(
                family='Arial, sans-serif',
                size=14,
                color=theme_colors['text']
            )
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin={"r": 20, "t": 80, "l": 0, "b": 40},
        coloraxis_colorbar=dict(
            title=translated_value,
            title_font=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            ),
            tickfont=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    return fig

def plot_cluster_distribution(df, language="fr", theme='light'):
    """Crée un graphique en camembert amélioré pour la distribution des clusters."""
    # Traduction
    title = "Répartition des donneurs de sang par Cluster"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    df['Cluster'] = df['Cluster'].astype(str)
    data_clus = ('Cluster ' + df.Cluster.astype(str)).value_counts().reset_index()
    data_clus.columns = ['Cluster', 'count']
    
    # Créer une palette de couleurs personnalisée et harmonieuse
    colors = px.colors.qualitative.Bold
    if len(data_clus) > len(colors):
        colors = colors * (len(data_clus) // len(colors) + 1)
    
    # Créer un graphique en camembert avec trous amélioré
    fig = px.pie(
        data_clus, 
        values='count', 
        names='Cluster', 
        hole=0.6,  # Trou plus grand pour un look moderne
        title=translated_title,
        color_discrete_sequence=colors,
        labels={'count': 'Nombre de donneurs'}
    )
    
    # Mettre en valeur certaines parties du camembert
    pull_values = []
    for i in range(len(data_clus)):
        if i == 0:  # Mettre en valeur le premier cluster (le plus grand)
            pull_values.append(0.1)
        else:
            pull_values.append(0.0)
    
    fig.update_traces(
        pull=pull_values,
        marker=dict(
            line=dict(color=theme_colors['gridLines'], width=2)
        ),
        opacity=0.9,
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(
            family='Arial, sans-serif',
            size=14,
            color='white'
        ),
        hoverinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>%{percent}<br>Nombre: %{value}<extra></extra>'
    )
    
    # Ajouter des annotations pour un look plus professionnel
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            ),
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin=dict(t=80, l=0, r=0, b=40),
        annotations=[
            dict(
                text='DISTRIBUTION<br>DES CLUSTERS',
                x=0.5,
                y=0.5,
                font=dict(
                    family='Arial, sans-serif',
                    size=16,
                    color=theme_colors['text']
                ),
                showarrow=False
            )
        ],
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    return fig

def create_treemap(df=data_final, language="fr", theme='light'):
    """Crée un treemap hiérarchique amélioré pour les dons de sang."""
    # Traduction
    title = "Hiérarchie et Composition des Donneurs de Sang"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Définir une palette de couleurs harmonieuse qui rappelle le sang
    if theme == 'dark':
        color_scale = [
            [0, "#67001f"],
            [0.1, "#b2182b"],
            [0.2, "#d6604d"],
            [0.3, "#f4a582"],
            [0.4, "#fddbc7"],
            [0.5, "#d1e5f0"],
            [0.6, "#92c5de"],
            [0.7, "#4393c3"],
            [0.8, "#2166ac"],
            [1, "#053061"]
        ]
    else:
        color_scale = [
            [0, "#053061"],
            [0.1, "#2166ac"],
            [0.2, "#4393c3"],
            [0.3, "#92c5de"],
            [0.4, "#d1e5f0"],
            [0.5, "#fddbc7"],
            [0.6, "#f4a582"],
            [0.7, "#d6604d"],
            [0.8, "#b2182b"],
            [1, "#67001f"]
        ]
    
    # Créer le treemap avec des options visuelles améliorées
    fig = px.treemap(
        df,
        path=['Sexe', 'Type de donation', 'Groupe Sanguin ABO / Rhesus'],
        values='Age',
        color='Age',
        color_continuous_scale=color_scale,
        title=translated_title,
        hover_data={
            'Sexe': True,
            'Type de donation': True,
            'Groupe Sanguin ABO / Rhesus': True,
            'Age': ':.1f'  # Afficher l'âge avec une décimale
        },
        branchvalues='total'  # Pour une meilleure hiérarchie
    )
    
    # Personnalisation avancée du layout pour un aspect plus médical/professionnel
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        font=dict(
            family='Arial, sans-serif',
            size=12,
            color=theme_colors['text']
        ),
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        margin=dict(t=40, l=10, r=10, b=10),
        coloraxis_colorbar=dict(
            title='Âge moyen',
            title_font=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            ),
            tickfont=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        )
    )
    
    # Améliorer les éléments du treemap
    fig.update_traces(
        marker=dict(
            line=dict(
                width=1,
                color=theme_colors['gridLines']
            ),
            pattern=dict(
                shape=""  # Pas de motif pour garder ça propre
            )
        ),
        textfont=dict(
            family='Arial, sans-serif',
            size=12
        ),
        hovertemplate='<b>%{label}</b><br>' +
                       'Âge moyen: %{color:.1f} ans<br>' +
                       'Total: %{value}<extra></extra>'
    )
    
    # Ajouter une annotation explicative
    fig.add_annotation(
        text="La taille de chaque bloc représente le nombre de donneurs<br>La couleur représente l'âge moyen",
        x=0.5,
        y=-0.05,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            family='Arial, sans-serif',
            size=10,
            color=theme_colors['text']
        ),
        align="center"
    )
    
    return fig

def create_age_distribution(df=data_final, language="fr", theme='light'):
    """Crée un graphique en violon amélioré pour la distribution de l'âge des donneurs par sexe."""
    # Traduction
    title = "Distribution de l'Âge des Donneurs par Sexe"
    age_label = "Âge"
    translated_title = GRAPH_TRANSLATIONS[language].get(title, title)
    translated_age = GRAPH_TRANSLATIONS[language].get(age_label, age_label)
    
    # Couleurs adaptées au thème
    theme_colors = THEME_PALETTES[theme]
    
    # Palette de couleurs médicales améliorée
    if theme == 'dark':
        color_map = {
            'M': '#5A9BD5',  # Bleu plus clair pour les hommes
            'F': '#FF7F7F'   # Rose plus clair pour les femmes
        }
    else:
        color_map = {
            'M': '#3366CC',  # Bleu pour les hommes
            'F': '#D53E4F'   # Rouge pour les femmes
        }
    
    # Créer une mise en page avec deux violons côte à côte
    fig = go.Figure()
    
    # Distribution par sexe avec violons améliorés
    for sexe in sorted(df['Sexe'].unique()):
        subset = df[df['Sexe'] == sexe]
        
        # Afficher étiquette sexe
        sex_label = "Hommes" if sexe == "M" else "Femmes" if sexe == "F" else sexe
        
        fig.add_trace(go.Violin(
            x=subset['Sexe'],
            y=subset['Age'],
            name=sex_label,
            legendgroup=sex_label,
            line_color=color_map[sexe],
            fillcolor=hex_to_rgba(color_map[sexe], 0.6),
            opacity=0.8,
            box_visible=True,
            meanline_visible=True,
            points='all',
            pointpos=0,
            jitter=0.05,
            marker=dict(
                size=4,
                opacity=0.6,
                color=color_map[sexe],
                line=dict(width=1, color=theme_colors['gridLines'])
            ),
            hoverinfo='y+name',
            hovertemplate='<b>%{x}</b><br>Âge: %{y} ans<extra></extra>'
        ))
    
    # Statistiques par sexe pour annotations
    stats_by_sex = df.groupby('Sexe')['Age'].agg(['mean', 'median', 'min', 'max', 'count'])
    
    # Mise en page améliorée
    fig.update_layout(
        title={
            'text': translated_title,
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 22,
                'color': theme_colors['text']
            }
        },
        yaxis_title={
            'text': translated_age + " (ans)",
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': theme_colors['text']
            }
        },
        xaxis_title="",
        violinmode='group',
        paper_bgcolor=theme_colors['background'],
        plot_bgcolor=theme_colors['background'],
        font=dict(
            family='Arial, sans-serif',
            size=12,
            color=theme_colors['text']
        ),
        legend=dict(
            title=dict(
                text="Sexe",
                font=dict(
                    family='Arial, sans-serif',
                    size=12,
                    color=theme_colors['text']
                )
            ),
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1,
            font=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ),
        margin=dict(t=80, l=40, r=40, b=80),
        hoverlabel=dict(
            bgcolor=theme_colors['cardBackground'],
            font_size=12,
            font_family="Arial, sans-serif"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=theme_colors['gridLines'],
            zeroline=True,
            zerolinecolor=theme_colors['gridLines'],
            tickfont=dict(
                family='Arial, sans-serif',
                size=12,
                color=theme_colors['text']
            )
        )
    )
    
    # Ajouter des annotations pour les statistiques
    annotations = []
    
    # Statistiques générales
    for i, sexe in enumerate(sorted(stats_by_sex.index)):
        stats = stats_by_sex.loc[sexe]
        
        # Annotation détaillée par sexe
        annotations.append(dict(
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.07 - (i * 0.05),
            text=(
                f"<b>{sexe}</b>: Moy={stats['mean']:.1f} ans, "
                f"Méd={stats['median']:.1f} ans, "
                f"Min={stats['min']:.0f} ans, "
                f"Max={stats['max']:.0f} ans, "
                f"n={stats['count']:.0f}"
            ),
            showarrow=False,
            align="center",
            bgcolor=theme_colors['cardBackground'],
            bordercolor=theme_colors['gridLines'],
            borderwidth=1,
            borderpad=4,
            font=dict(
                family='Arial, sans-serif',
                size=10,
                color=theme_colors['text']
            )
        ))
    
    fig.update_layout(annotations=annotations)
    
    return fig