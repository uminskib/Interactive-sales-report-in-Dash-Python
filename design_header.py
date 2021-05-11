import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

#Nagłówek strony
def get_header(app):
    header = html.Div(
        [   html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("raportlogo.png"),
                        className="logo"
                    ),
    
                ],
                className="row",
                ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Raport sprzedażowy na temat polskiego rynku elektronicznego",style={'font-weight': 'bold'})],
                        className="eight columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Pełny widok",
                                href="/salesreport/pelny_widok",
                                className="full-view-link",
                            )
                        ],
                        className="four columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header

#Linki do podstron
def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Podsumowanie",
                href="/salesreport/podsumowanie",
                className="tab first",
            ),
            dcc.Link(
                "Porównanie",
                href="/salesreport/porownanie",
                className="tab",
            )
        ],
        className="row all-tabs",
    )
    return menu

#Funkcja do tworzenia tabeli statycznej
def make_dash_table(df):
    """ Zwraca tabele html dla danego dataframe  """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
