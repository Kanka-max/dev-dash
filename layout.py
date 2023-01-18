from dash import Dash, html                                       
import dash_bootstrap_components as dbc            
from . import cards, filter, wordcloud, barchart, category,region


def create_layout(app:Dash) -> html.Div:
    return dbc.Container(
        className="app-layout",
        children=[
            cards.cards_layout(app),
            filter.filter_layout(app),
            # wordcloud.wordcloud_layout(app),
            barchart.barchart_layout(app),
            category.category_layout(app),
            # region.region_layout(app)
        ]
    )