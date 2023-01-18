from dash import Dash, html
import dash_bootstrap_components as dbc
from dash import dcc

app = Dash(__name__)

def barchart_layout(app:Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div(
                className="barchart-container",
                children=[
                    html.Div(
                        className="content",
                        children=[
                            html.P("The chart shows the number of messages spreading more concretely over the selected period of time: "),
                        ]
                    ),
                    #insert bar chart here
                    html.Div([
                        dcc.Graph(id = 'stackedbar_chart', figure={}, config={'displayModeBar': 'hover'})
                        
                    ])
                ]
            )
        ]
    )