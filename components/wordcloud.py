# from dash import Dash, html
# import dash_bootstrap_components as dbc

# app = Dash(__name__)

# def wordcloud_layout(app:Dash) -> html.Div:
#     return html.Div(
#         children=[
#             html.Div(
#                 className="wordcloud-container",
#                 children=[
#                     html.Div(
#                         className="content",
#                         children=[
#                             html.H4("Understanding the context"),
#                             html.P("Harmful language can be further understood by showing the concrete language used. Following is a xx chart that shows the main terms associated with harmful language."),
#                         ]
#                     ),
#                     dbc.Row(
#                         [
#                             dbc.Col(
#                                 [
#                                     html.Div(
#                                         children=[
#                                             html.P("Overall Speech"),
#                                             html.Div(
#                                                 className="overall-speech",
#                                             #Insert Wordcloud Here
#                                             )
#                                         ]
#                                     )
#                                 ]
#                             ),
#                             dbc.Col(
#                                 [
#                                     html.Div(
#                                         children=[
#                                             html.P("Harmful Speech"),
#                                             html.Div(
#                                                 className="harmful-speech",
#                                             #Insert Wordcloud Here
#                                             )
#                                         ]
#                                     )
#                                 ]
#                             ),
#                         ]
#                     )
#                 ]
#             )
#         ]
#     )