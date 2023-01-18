from dash import Dash, html
import dash_bootstrap_components as dbc
from dash import dcc

app = Dash(__name__)

def category_layout(app:Dash) -> html.Div:
    return html.Div(
        className="category-container",
        children=[
            html.Div(
                className="content",
                children=[
                    html.H4("Understanding the severity of harmful language"),
                    html.P("Harm can be created at different levels. We differentiate between offensive speech, hateful speech, threatening speech, and calls to violence. It is anticipated that the less aggressive levels (offensive speech) will be the more prevalent. "),
                ]
            ),
            #insert horizontal chart here
            html.Div([
                dcc.Graph(id = 'horizontalbar_chart', figure={}, config={'displayModeBar': 'hover'}),
                dcc.Graph(id = 'line_chart', figure={}, config={'displayModeBar': 'hover'}),
            ])
        ]
    )