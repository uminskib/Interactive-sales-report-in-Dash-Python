import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
from design_header import Header
import pandas as pd
import pathlib
from dash.dependencies import Input, Output
from app import app
import json
import numpy as np

# Ustawienie folderu
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../Dane_do_strony").resolve()

#import danych
brand_podsumowanie = pd.read_csv(DATA_PATH.joinpath("brand_podsumowanie.csv"))
produkt_podsumowanie = pd.read_csv(DATA_PATH.joinpath("produkt_podsumowanie.csv"))

dane_wszystko=pd.read_csv(DATA_PATH.joinpath("dane_wszystko.csv"))

firmy=dane_wszystko["Brand"].unique().tolist()
produkty=dane_wszystko["Produkt"].unique().tolist()

def opis_strony():
    
    return html.Div(
        id="opis-strony",
        children=[
            html.H6("Analiza porównawcza 2 wybranych firm",style={'textAlign':'center','font-weight': 'bold','font-size': '1.83em'}),
                 ]
    )
#Funkcja tworząca formularze wyboru
def kontrola_prez():
    return html.Div(
        id="kontrola-prez",
        children=[
            html.Br(),
            html.Br(),
            html.Div(
                className='row',
                children=[
                   html.Div(
                       className='five columns',
                       id='wybor-firmy-1',
                       children=[
                              
                               html.Label("Wybierz pierwszą firmę"),
                               dcc.Dropdown(
                                       id="pierwsza-firma",
                                       options=[{"label": i, "value": i} for i in firmy],
                                       value=firmy[0],
                                           ),
                                ],
                        ),
                    html.Div(className='two columns',),
                    html.Div(
                        className='five columns',
                        id='wybor-firmy-2',
                        children=[
                            
                                html.Label("Wybierz drugą firmę"),
                                dcc.Dropdown(
                                        id="druga-firma",
                                        options=[{"label": i, "value": i} for i in firmy],
                                        value=firmy[1],
                                        
                                            ),
                                ],
                             ),
                        ],
                    ),
                    html.Div(            
                        id='wiersz-2',
                        className="row",
                        children=[
                            html.Div(
                                id='wybor-produkt',
                                children=[
                                        html.Label("Wybierz produkty"),
                                        dcc.Dropdown(
                                                id="produkty",
                                                options=[{"label": i, "value": i} for i in produkty],
                                                value=produkty[:],
                                                multi=True,
                                                    ),
                                         ],
                                    ),
                                ],
                            ),
                ],
            )

#Wygląd strony
layout = html.Div(
        [
            Header(app),
            # Strona druga
            html.Div(
                [ #Wiersz pierwszy
                    html.Div(
                        [
                            html.Div(
                                [
                                    opis_strony(), 
                                    kontrola_prez(),
                                ]
                                    ),
                            #Wiersz drugi
                             html.Div(
                                 [
                                 html.Div(
                                    [
                                    html.Br([]),
                                    html.H6(
                                        ["Porównanie sprzedaży obu firm w poszczególnych tygodniach"],
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(id='bar-graph'),
                                    ],
                       
                            ),
         
                                ],
                                    ),
                            #Wiersz trzeci
                             html.Div(
                                 [
                                 html.Div(
                                    [
                                    html.Br([]),
                                    html.H6(
                                        ["Sprzedaż wybranych produktów w podziale na województwa"],
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id='choropleth-map1'),
                                    html.Br([]),
                                    dcc.Graph(id='choropleth-map2')
                                    ],
                       className="six columns",
                            ),
                                            
                                html.Div(
                                    [
                                    html.Br([]),
                                    html.H6(
                                        ["Podstawowe statystyki sprzedaży dla obu firm"],
                                        className="subtitle padded",
                                    ),
                                   dcc.Graph(id='table-container')
                                               
                                    
                                    ],
                       className="six columns",
                            ),
                                ],
                                    ),
                                                ],
                        ),
                    ],
             className="sub_page",
             ),
            ],
            className="page",   
                )
#odwołania z pomocą ustanowionych id.
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('pierwsza-firma','value'),
     Input('druga-firma','value'),
     Input('produkty','value')])

#Podwójny wykres słupkowy
def bar_graph(firm1,firm2,produkty):
    weeks=dane_wszystko['Tydzien'].unique().tolist()
    produkty_firmy=dane_wszystko[dane_wszystko['Produkt'].isin(produkty) & dane_wszystko['Brand'].isin([firm1,firm2])].groupby(['Tydzien','Brand']).sum()
    produkty_firmy=produkty_firmy.reset_index(level=1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=weeks,
                y=produkty_firmy[produkty_firmy['Brand']==firm1]['Sprzedaz'].tolist(),
                name=firm1,
                marker_color='rgb(55, 83, 109)'
                ))
    fig.add_trace(go.Bar(x=weeks,
                y=produkty_firmy[produkty_firmy['Brand']==firm2]['Sprzedaz'].tolist(),
                name=firm2,
                marker_color='rgb(26, 118, 255)'
                ))

    fig.update_layout(
    xaxis=dict(tickfont_size=12, title='Tydzień',dtick=5),
    yaxis=dict(
        title='Sprzedana ilość',
        titlefont_size=14,
        tickfont_size=12,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, 
    bargroupgap=0.1 ,
    margin={  "r": 15,
                 "t": 10,
                 "b": 0,
                 "l": 0,},
    width=750,
    height=350,
)
    return fig

@app.callback(
    Output('choropleth-map1', 'figure'),
    [Input('pierwsza-firma','value'),
     Input('produkty','value')])

#Mapa sprzedażowa dla pierwszej firmy
def choropleth_map1(firm1,produkty):
    
    with open(DATA_PATH.joinpath("poland_woj.json"),encoding="utf-8-sig") as response:
        counties = json.load(response)
    wojewodztwa=dane_wszystko["Wojewodztwo"].unique().tolist()
    wojew_sprzedaz=dane_wszystko[dane_wszystko['Produkt'].isin(produkty) & dane_wszystko['Brand'].isin([firm1])].groupby(['Wojewodztwo','Brand']).agg({'Sprzedaz':'sum'})
    wojew_sprzedaz=wojew_sprzedaz.reset_index(level=0).reset_index(level=0)
    for i in list(wojewodztwa):
        if(i in list(wojew_sprzedaz["Wojewodztwo"])):
            continue
        else:
            wojew_sprzedaz=wojew_sprzedaz.append({"Brand":str(firm1),"Wojewodztwo":str(i),"Sprzedaz":0},ignore_index=True)
    wojew_sprzedaz=wojew_sprzedaz.append({"Brand":str(firm1),"Wojewodztwo":'Kujawsko-Pomorskie',"Sprzedaz":0},ignore_index=True)
    wojew_sprzedaz=wojew_sprzedaz.append({"Brand":str(firm1),"Wojewodztwo":'Warminsko-Mazurskie',"Sprzedaz":0},ignore_index=True)
    
    fig1 = go.Figure(data=go.Choropleth(z=wojew_sprzedaz["Sprzedaz"], geojson=counties,
                    locations=wojew_sprzedaz["Wojewodztwo"], featureidkey="properties.name",colorscale = 'Blues',
                   colorbar=dict(thickness=10,len=0.8)))
    fig1=fig1.update_geos(fitbounds="locations", visible=False)
    fig1=fig1.update_layout(
        title=dict(text=wojew_sprzedaz['Brand'].unique().tolist()[0], pad=dict(t=100,b=150,l=100)),
        geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='mercator'),
        margin={  "r": 0,
                 "t": 25,
                 "b": 0,
                 "l": 0
                 },
        height=210
        )
    return fig1

@app.callback(
    Output('choropleth-map2', 'figure'),
    [Input('druga-firma','value'),
     Input('produkty','value')])

#Mapa sprzedażowa dla drugiej firmy
def choropleth_map2(firm2,produkty):
    with open(DATA_PATH.joinpath("poland_woj.json"),encoding="utf-8-sig") as response:
        counties = json.load(response)
    wojewodztwa=dane_wszystko["Wojewodztwo"].unique().tolist()
    wojew_sprzedaz=dane_wszystko[dane_wszystko['Produkt'].isin(produkty) & dane_wszystko['Brand'].isin([firm2])].groupby(['Wojewodztwo','Brand']).agg({'Sprzedaz':'sum'})
    wojew_sprzedaz=wojew_sprzedaz.reset_index(level=0).reset_index(level=0)
    for i in list(wojewodztwa):
        if(i in list(wojew_sprzedaz["Wojewodztwo"])):
            continue
        else:
            wojew_sprzedaz=wojew_sprzedaz.append({"Brand":str(firm2),"Wojewodztwo":str(i),"Sprzedaz":0},ignore_index=True)
    wojew_sprzedaz=wojew_sprzedaz.append({"Brand":str(firm2),"Wojewodztwo":'Kujawsko-Pomorskie',"Sprzedaz":0},ignore_index=True)
    wojew_sprzedaz=wojew_sprzedaz.append({"Brand":str(firm2),"Wojewodztwo":'Warminsko-Mazurskie',"Sprzedaz":0},ignore_index=True)
    
    fig1 = go.Figure(data=go.Choropleth(z=wojew_sprzedaz["Sprzedaz"], geojson=counties,
                    locations=wojew_sprzedaz["Wojewodztwo"], featureidkey="properties.name",colorscale = 'Blues',
                   colorbar=dict(thickness=10,len=0.8)))
    fig1=fig1.update_geos(fitbounds="locations", visible=False)
    fig1=fig1.update_layout(
        title=dict(text=wojew_sprzedaz['Brand'].unique().tolist()[0], pad=dict(t=100,b=150,l=100)),
        geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='mercator'),
        margin={  "r": 0,
                 "t": 25,
                 "b": 0,
                 "l": 0
                 },
        height=210
        )
    return fig1
       
@app.callback(
        Output('table-container','figure'),
    [Input('pierwsza-firma','value'),
     Input('druga-firma','value'),
     Input('produkty','value')])

#Tabela z podstawowymi statystykami
def table_container(firma1,firma2,produkty):
    statystyki=dane_wszystko[dane_wszystko['Produkt'].isin(produkty) & dane_wszystko['Brand'].isin([firma1,firma2])][['Brand','Sprzedaz']]
    
    staty_opis=statystyki.groupby(['Brand']).agg({'Sprzedaz':[np.sum,np.mean,np.std,np.min,np.median,np.max]})
    staty_opis=staty_opis.T
    staty_opis=staty_opis.reset_index(level=0,drop=True)
    staty_opis=staty_opis.reset_index(level=0)
    staty_opis=staty_opis.rename(columns={'index':'Statystyki'})
    staty_opis=staty_opis.round(2)
    staty_opis['Statystyki']=staty_opis['Statystyki'].replace({'sum':'Suma','mean':'Średnia','std':'Odch. Stand.','amin':'Min','amax':'Max','median':'Mediana'})
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(staty_opis.columns),
                fill_color='skyblue',
                align='center',
                height=25,
                font=dict(size=13)),
    cells=dict(values=[staty_opis.iloc[:,0], staty_opis.iloc[:,1],staty_opis.iloc[:,2]],
               fill_color='lavender',
               align='center',
               height=25,
               font=dict(size=13)),columnwidth=30)
])
    fig=fig.update_layout(height=500,width=370,
                      margin={ "r": 20,
                               "t": 90,
                               "b": 0,
                               "l": 25
                 })
    return fig