import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#Uruchomienie pliku z przygotowaniem danych
exec(open('prepare_data.py').read())
#Import poszczególnych skryptów budujacych raport
from app import app

from pages import (
    page1,
    page2,
    pagehome,
)


# Wygląd strony z raportem
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Odwołanie się do plików z trescią stron
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/salesreport/podsumowanie":
        return page1.layout
    elif pathname == "/salesreport/porownanie":
        return page2.layout
    elif pathname == "/salesreport/pelny_widok":
        return (
            page1.layout,
            page2.layout,
        )
    else:
        return pagehome.layout


if __name__ == "__main__":
    app.run_server(debug=False)