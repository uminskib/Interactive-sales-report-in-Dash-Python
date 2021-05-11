import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
from design_header import Header, make_dash_table
import pandas as pd
import pathlib
from app import app

# Ustanowienie folderu
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../Dane_do_strony").resolve()

#Tabele z danymi
brand_podsumowanie = pd.read_csv(DATA_PATH.joinpath("brand_podsumowanie.csv"))
produkt_podsumowanie = pd.read_csv(DATA_PATH.joinpath("produkt_podsumowanie.csv"))
woj_sprzedaz= pd.read_csv(DATA_PATH.joinpath("woj_sprzedaz.csv"))

#Mapa sprzedażowa
import json
with open(DATA_PATH.joinpath("poland_woj.json"),encoding="utf-8-sig") as response:
    counties = json.load(response)

fig = go.Figure(data=go.Choropleth(z=woj_sprzedaz["Sprzedaz"], geojson=counties,
                    locations=woj_sprzedaz["Wojewodztwo"], featureidkey="properties.name",colorscale = 'Reds'
                   ))
fig=fig.update_geos(fitbounds="locations", visible=False)
fig=fig.update_layout(
        geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ), margin={  "r": 40,
                 "t": 20,
                 "b": 40,
                 "l": 40,},)


#Budowa strony
layout= html.Div(
        [
            Header(app),
            #Wiersz pierwszy
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Wniosek"),
                                    html.Br([]),
                                    html.P(
                                        '''\
                                        Na podstawie danych, które posłużyły do stworzenia
                                        raportu można uzyskać interesujące wnioski na temat rocznej sprzedaży na rynku
                                        elektronicznym w Polsce. W analizie znalazło się 6 najpopularniejszych
                                        firm: LG, Panasonic, Philips, Samsung, Sony oraz Toshiba. Prezentacja poniższych
                                        informacji pokazała, że najwięcej sprzedanych towarów w Polsce posiada firma
                                        Panasonic a tóż za nią jest LG. Najczęściej kupowanym przez klientów produktami były sprzęty HiFi.
                                        Przyglądając się poszczególnym województwom to najwyższe wyniki sprzedażowe są osiągane na zachodzie kraju, 
                                        czyli w województwie opolskim, lubuskim i dolnośląskim.''',
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Wiersz drugi
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Suma sprzedaży danej firmy"],
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(           #Wykres słupkowy
                                        id="graph-6",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=brand_podsumowanie["Brand"],
                                                    y=brand_podsumowanie["Sprzedaz"],
                                                    marker={"color": "#97151c"},
                                                    name="A",
                                                    )
                                                    ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                height=300,
                                                width=320,
                                                bargap=0.4,
                                                barmode="stack",
                                                hovermode="closest",
                                                margin={
                                                    "r": 40,
                                                    "t": 20,
                                                    "b": 40,
                                                    "l": 40,
                                                        },
                                            ),
                                                        },
                                                    ),
                                                    ],          
                            className="seven columns",
                                
                            ),
                             html.Div(   #Tabela z srednia sprzedażą
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Średnia sprzedaż poszczególnych produktów"],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(produkt_podsumowanie.T.reset_index().T),
                                               
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="five columns",
                            )
                        ],      
        
                        className="row ",
                    ),
            #Wiersz drugi
                html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Sprzedaż produktów w podziale na województwa"],
                                        className="subtitle padded",
                                    ),
                                  dcc.Graph(
                                        id='choropleth_map',
                                        figure=fig,  #Mapa sprzedażowa
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
                                        