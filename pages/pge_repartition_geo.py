from packages.pkg_localisation_geo import *
from dash import html, dcc, callback_context,ctx
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from packages.pkg_kpi import *
from prossess_data.prossess import data_final
from app import *
from dash.dependencies import Input, Output, State

card_style={}

def page_une(theme, plot_font_color, plot_bg, plot_paper_bg, plot_grid_color, light_theme, dark_theme):
    
    global card_style
    
    if theme == 'light':
        card_style = {'backgroundColor': light_theme['cardBg']}
        style_dropdow = {'width': '150px', 'backgroundColor': '#D9DADC ', 'border': 'none','fontSize': '12px'}
    else:
        card_style = {'backgroundColor':   dark_theme['cardBg'],'color':'white'}
        style_dropdow = {'width': '150px', 'backgroundColor': 'black', 'border': 'none','fontSize': '12px','color':'black'}
            
    liste_arrondissement = data_final['Arrondissement de résidence'].unique()
    geo_vars=["Niveau d'etude", "Genre",'Situation Matrimoniale (SM)','A-t-il (elle) déjà donné le sang','ÉLIGIBILITÉ AU DON.'] 
    
    # Création des quatre cartes avec dbc.Card
    card1 = dbc.Card([
        dbc.CardHeader(
            html.Div(
                [
                    # Icône avec DashIconify
                    DashIconify(
                        icon="mdi:account-group", 
                        width=20 
                    ),
                    html.Span("Caracteristique demographique"),

                    # Dropdown personnalisé
                    dcc.Dropdown(
                        id='caract-demo1',
                        options=[
                            {'label': 'Religion', 'value': 'Religion'},
                            {'label': 'Situation Matrimoniale', 'value': 'Situation Matrimoniale (SM)'},
                            {'label': 'Age', 'value': 'Age'}
                        ],
                        clearable=False,
                        value='Religion',  # Option par défaut
                        style=style_dropdow
                    )
                ],
                # Alignement horizontal et espacement via Bootstrap
                className="d-flex justify-content-between align-items-center"
            )
        ),
        dbc.CardBody([
            dcc.Graph(
                id='var-demograp',
                figure=Etude_repartition_var_dem(
                    data=data_final,
                    var_='Religion',
                    title='Repartition des Religions des candidats aux don'
                ),
                responsive=True,
                style={'height': '370px'}
            )
        ], style={'height': '380px', "padding-top": "0px"})
    ],style=card_style)

    card2 = dbc.Card([
    dbc.CardHeader(
        html.Div(
            [
                # Partie gauche avec icône et titre
                html.Div(
                    [
                        # Icône avec DashIconify
                        DashIconify(
                            icon="mdi:gender-male-female", 
                            width=20
                        ),
                        html.Span("Sexe et Nationalité"),
                    ],
                    className="d-flex align-items-center gap-2"
                ),
                
                # Partie centrale avec dropdown
                dcc.Dropdown(
                    id='arrondissement',
                    options=[
                        {'label': i, 'value': i} for i in liste_arrondissement
                    ],
                    clearable=True,
                    multi=True,maxHeight=100,
                    value=liste_arrondissement[0],  # Option par défaut
                    style={**style_dropdow,'width':'300px'}
                ),
                
                # Partie droite avec bouton effacer filtre
                html.Button(
                    [
                        DashIconify(icon="mdi:filter-remove", width=16, style={"marginRight": "5px"}),
                        "Effacer filtre"
                    ],
                    id="clear-filter-button",
                    className="btn btn-outline-secondary btn-sm",
                    style={
                        'fontSize': '12px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'padding': '4px 8px'
                    }
                )
            ],
            # Alignement horizontal et espacement via Bootstrap
            className="d-flex justify-content-between align-items-center"
        )
    ),
    dbc.CardBody([
        dcc.Graph(
            id='sexe_nationna',
            figure=return_stat_enqueteur(data=data_final),
            responsive=True,
            style={'height': '370px'}
        )
    ], style={'height': '380px', "padding-top": "0px"})
],style=card_style)
    
    card3 = dbc.Card([
        dbc.CardHeader(
            html.Div(
                [
                    DashIconify(icon="mdi:chart-bar", width=20),
                    html.Span("Arrondissement de don")
                ],
                className="d-flex align-items-center gap-2"
            )
        ),
        dbc.CardBody(
            dcc.Graph(
                figure=create_blood_donation_sankey(data=data_final),
                responsive=True,
                style={'height': '370px'}
            ), style={'height': '390px'})
    ],style=card_style)

    
    card4 = dbc.Card([
                dbc.CardHeader(
                    html.Div(
                        [
                            # Partie gauche avec icône et titre
                            html.Div(
                                [
                                    DashIconify(icon="mdi:map-marker", width=20),
                                    html.Span("Cartographie des zones enquêtes",style={'fontsize':'10px'})
                                ],
                                className="d-flex align-items-center gap-2"
                            ),
                            
                            # Partie droite avec dropdowns et boutons
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id="variable",
                                        options=[
                                            {"label": i, "value": i} for i in geo_vars
                                        ],
                                        placeholder="variable",
                                        className="me-2",
                                        style={**style_dropdow,'width':'100px'}
                                    ),
                                    dcc.Dropdown(
                                        id="var-1",
                                        options=[
                                            {"label": "Option 1", "value": "opt1"}
                                        ],
                                        placeholder="modalite1",
                                        className="me-2",
                                        style={**style_dropdow,'width':'100px'}
                                    ),
                                    dcc.Dropdown(
                                        id="var-2",
                                        options=[
                                            {"label": "Option 1", "value": "opt1"},
                                        ],
                                        placeholder="modalite2",
                                        style={**style_dropdow,'width':'100px'}
                                    ),
                                    # Boutons de localisation et plein écran
                                    html.Div([
                                        html.Button(
                                            DashIconify(icon="mdi:crosshairs-gps", width=20),
                                            id="btn-location",
                                            className="btn btn-outline-primary ms-2",
                                            style={"height": "38px", "width": "38px", "padding": "6px"}
                                        ),
                                        html.Button(
                                            DashIconify(icon="mdi:fullscreen", width=20),
                                            id="btn-fullscreen",
                                            className="btn btn-outline-primary ms-2",
                                            style={"height": "38px", "width": "38px", "padding": "6px"}
                                        ),
                                        html.Button(
                                            DashIconify(icon="mdi:fullscreen-exit", width=20),
                                            id="btn-exit-fullscreen",
                                            className="btn btn-outline-primary ms-2",
                                            style={
                                                "height": "38px", 
                                                "width": "38px", 
                                                "padding": "6px", 
                                                "display": "none"
                                            }
                                        )
                                    ], className="d-flex align-items-center")
                                ],
                                className="d-flex align-items-center justify-content-end flex-wrap"
                            ),
                        ],
                        className="d-flex justify-content-between align-items-center w-100"
                    )
                ),
                dbc.CardBody(
                    dcc.Graph(
                        figure=Carte_arrondissement(data_name=communes,variable_name="Prop Candidats aux dons",titre="Proportion des candidats aux dons",label_name='Arrondissement de résidence',legend_name="donnateurs"),
                        id='carto-graph',
                        responsive=True,
                        style={'height': '360px'}
                    ), 
                    style={'height': '380px'},
                    id='carte'
                )
            ],style=card_style, id='card4')
    
    
    return html.Div([
        # Texte explicatif
        dbc.Row([
            # Carte pour le total des enquêtes
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            DashIconify(
                                icon="mdi:clipboard-text-outline",
                                width=40,
                                height=40,
                                style={"color": "white"}
                            ),
                        ], style={"float": "left", "margin-right": "15px", "background-color": "#F7A93B", "padding": "15px", "border-radius": "5px"}),
                        html.Div([
                            html.H2(total_enquetes(data_final), className="card-title",id='total_enquet'),  ### indicateur
                            html.P("Total enquêtes"),
                        ]),
                    ])
                ], className="mb-4 shadow-sm",style=card_style)
            ], md=4),
            
            # Carte pour le nombre d'arrondissements
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            DashIconify(
                                icon="mdi:map-marker-multiple",
                                width=40,
                                height=40,
                                style={"color": "white"}
                            ),
                        ], style={"float": "left", "margin-right": "15px", "background-color": "#3A7AB9", "padding": "15px", "border-radius": "5px"}),
                        html.Div([
                            html.H2(nombre_arrondissement(data_final), className="card-title",id='nombre_arrondissem'),  ### indicateur
                            html.P("Nombre d'arrondissements"),
                        ]),
                    ])
                ], className="mb-4 shadow-sm",style=card_style)
            ], md=4),
            
            # Carte pour le total des quartiers
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            DashIconify(
                                icon="mdi:city-variant-outline",
                                width=40,
                                height=40,
                                style={"color": "white"}
                            ),
                        ], style={"float": "left", "margin-right": "15px", "background-color": "#48B95E", "padding": "15px", "border-radius": "5px"}),
                        html.Div([
                            html.H2(total_quartiers(data_final), className="card-title",id='total_quart'),  ### indicateur
                            html.P("Total quartiers"),
                        ]),
                    ])
                ], className="mb-4 shadow-sm",style=card_style)
            ], md=4),
        ]),
        
        dbc.Row([
            dbc.Col(card1, width=5, className="mb-4"),
            dbc.Col(card2, width=7, className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(card3, width=5),
            dbc.Col(card4, width=7)
        ])
    ])
    



    
@app.callback(
    Output('var-demograp', 'figure'),
    Output('total_enquet', 'children'),
    [Input('caract-demo1', 'value'),
     Input('arrondissement','value')
    ] 
)
def update_caractdemo(selected_val,selected_arr):
    if isinstance(selected_arr, str):
        selected_arr = [selected_arr]
    # Mise à jour du graphique en fonction de la sélection 
    if selected_val == 'Religion':
        a = Etude_repartition_var_dem(
            data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)],
            var_='Religion',
            title='Repartition des Religions des candidats aux don'
        )
        b=total_enquetes(data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])
    elif selected_val == 'Situation Matrimoniale (SM)':
        a = Etude_repartition_var_dem(
            data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)],
            var_='Situation Matrimoniale (SM)',
            title='Repartition de la situation matrimonial des candidats aux dons'
        )
        b=total_enquetes(data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])
    elif selected_val == 'Age':
        a = classe_age_plot(data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])
        b=total_enquetes(data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])
    if not ctx.triggered:
        b=total_enquetes(data_final)    
    return a,b




######pour le statut matrimonial
@app.callback(
    Output('sexe_nationna', 'figure'),
    Input('arrondissement','value')  
)
def update_graph(selected_arr):
    if isinstance(selected_arr, str):
        selected_arr = [selected_arr]
    return return_stat_enqueteur(data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])



###### pour effacer les filtres
@app.callback(
    Output('sexe_nationna', 'figure',allow_duplicate=True),
    Output('var-demograp', 'figure',allow_duplicate=True),
    Output('total_enquet', 'children',allow_duplicate=True),
    Output('nombre_arrondissem', 'children',allow_duplicate=True),
    Output('total_quart', 'children',allow_duplicate=True),
    [Input('clear-filter-button', 'n_clicks'),
     Input('arrondissement','value'),
     Input('caract-demo1', 'value'),],
    prevent_initial_call=True
)
def reset_arrondissement_dropdown(n_clicks,selected_arr,select_caract):
    if isinstance(selected_arr, str):
        selected_arr = [selected_arr]
    if n_clicks:
        # Réinitialise le dropdown à sa valeur par défaut
        if select_caract == 'Religion':
            a = Etude_repartition_var_dem(
                data=data_final,
                var_='Religion',
                title='Repartition des Religions des candidats aux don'
            )
        elif select_caract == 'Situation Matrimoniale (SM)':
            a = Etude_repartition_var_dem(
                data=data_final,
                var_='Situation Matrimoniale (SM)',
                title='Repartition de la situation matrimonial des candidats aux dons'
            )
        elif select_caract == 'Age':
            a = classe_age_plot(data=data_final)
            
        return return_stat_enqueteur(data=data_final),a,\
            total_enquetes(data_final),nombre_arrondissement(data_final),\
            total_quartiers(data_final)    
    else:
        if select_caract == 'Religion':
            a = Etude_repartition_var_dem(
                data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)],
                var_='Religion',
                title='Repartition des Religions des candidats aux don'
            )
        elif select_caract == 'Situation Matrimoniale (SM)':
            a = Etude_repartition_var_dem(
                data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)],
                var_='Situation Matrimoniale (SM)',
                title='Repartition de la situation matrimonial des candidats aux dons'
            )
        elif select_caract == 'Age':
            a = classe_age_plot(data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])
    

    return return_stat_enqueteur(data=data_final[data_final['Arrondissement de résidence'].isin(selected_arr)]),a,\
                    total_enquetes(data_final[data_final['Arrondissement de résidence'].isin(selected_arr)]),\
                    nombre_arrondissement(data_final[data_final['Arrondissement de résidence'].isin(selected_arr)]),\
                    total_quartiers(data_final[data_final['Arrondissement de résidence'].isin(selected_arr)])        


#####pour reinitaliser le boutton
@app.callback(
    Output('clear-filter-button', 'n_clicks'),
    Input('arrondissement', 'value'),
    prevent_initial_call=True
)
def reset_clicks_on_dropdown(value):
    # Lorsque l'utilisateur change la valeur du Dropdown, réinitialiser `n_clicks` du bouton
    return None  # Réinitialise n_clicks à None


#####pour reinitaliser le boutton2
@app.callback(
    Output('clear-filter-button', 'n_clicks',allow_duplicate=True),
    Input('caract-demo1', 'value'),
    prevent_initial_call=True
)
def reset_clicks_on_dropdown(value):
    # Lorsque l'utilisateur change la valeur du Dropdown, réinitialiser `n_clicks` du bouton
    return None  # Réinitialise n_clicks à None


### variables cartographie
@app.callback(
    Output('var-1', 'options'),
    Output('var-2','options'),
    Input('variable', 'value'),
    prevent_initial_call=True
)
def update_dropdown(value):
    
    x = [ {'label':i,'value':i}  for i in data_final[value].unique().tolist()]
    
    return x,x


### modalite des variables de la cartographie
@app.callback(
    Output('var-2', 'options',allow_duplicate=True),
    [Input('var-1', 'value'),
    Input('variable', 'value')],
    prevent_initial_call=True
)
def update_dropdown(value,var):
    if value is None:
        return []  # Retourne une liste vide si aucune valeur n'est sélectionnée

    if var not in data_final.columns:
        return []  # Retourne une liste vide si la colonne n'existe pas

    try:
        unique_values = data_final[var].unique().tolist()
        options = [{'label': i, 'value': i} for i in unique_values if i != value]
        return options
    except KeyError:
        return [] #retourne une liste vide si il y a une erreur dans la clef


### mise a jours de la carte
@app.callback(
    Output("carte", "children"),
    [Input('var-1', 'value'),
    Input('var-2','value')],
    prevent_initial_call=True
)
def update_dropdown(value1,value2):
    
    return dcc.Graph(
                figure=cartographie_quartier(var1=value1,var2 =value2 ),
                responsive=True,
                style={'height': '360px'}
            )



@app.callback(
    Output("carte", "children",allow_duplicate=True),
    Input("btn-location", "n_clicks"),
    prevent_initial_call=True
)
def update_map(n_clicks):
    if n_clicks:
        # Assurez-vous que coord_quart est disponible dans ce scope
        # Vous pourriez avoir besoin de le charger ici ou de le passer via un State
        return html.Iframe(
            id='map', 
            srcDoc=CarteFolium(coord_quart, "Femme", "Homme"), 
            width='100%', 
            height='340'
        )
        





@app.callback(
    [Output('card4', 'style'),  # Target the entire card
     Output('btn-fullscreen', 'style'),
     Output('btn-exit-fullscreen', 'style')],
    [Input('btn-fullscreen', 'n_clicks'),
     Input('btn-exit-fullscreen', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_card_fullscreen(n_clicks_fullscreen, n_clicks_exit):
    ctx = callback_context
    
    # Default card style (matching the original)
    default_card_style = {
        'backgroundColor': card_style.get('backgroundColor', 'white'),
        'width': '100%',  # Ensure full width of container
        'height': 'auto',  # Allow content to define height
        'transition': 'all 0.3s ease'
    }
    
    # Fullscreen style that preserves original card characteristics
    fullscreen_card_style = {
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'width': '100vw',
        'height': '100vh',
        'zIndex': '1000',
        'backgroundColor': card_style.get('backgroundColor', 'white'),
        'padding': '20px',
        'boxSizing': 'border-box',
        'transition': 'all 0.3s ease',
        'display': 'flex',
        'flexDirection': 'column'
    }
    
    # Consistent button styles
    fullscreen_btn_style = {
        'height': '38px', 
        'width': '38px', 
        'padding': '6px',
        'display': 'block'
    }
    
    exit_fullscreen_btn_style = {
        'height': '38px', 
        'width': '38px', 
        'padding': '6px',
        'display': 'none'
    }
    
    if not ctx.triggered:
        return default_card_style, fullscreen_btn_style, exit_fullscreen_btn_style
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'btn-fullscreen':
        # Fullscreen mode
        fullscreen_btn_style['display'] = 'none'
        exit_fullscreen_btn_style['display'] = 'block'
        return fullscreen_card_style, fullscreen_btn_style, exit_fullscreen_btn_style
    
    elif button_id == 'btn-exit-fullscreen':
        # Normal mode
        fullscreen_btn_style['display'] = 'block'
        exit_fullscreen_btn_style['display'] = 'none'
        return default_card_style, fullscreen_btn_style, exit_fullscreen_btn_style
    
    return default_card_style, fullscreen_btn_style, exit_fullscreen_btn_style  
   
   
   
   
   
   
   
   
   