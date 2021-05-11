import dash_html_components as html
from design_header import Header
from app import app

layout=html.Div(
        [
            Header(app),
            html.Div(
                [
            # Strona domowa
                    
        
                ],
                    className="sub_page",
                    ),
                    
        ],
        className="page",
        
    )