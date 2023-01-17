import dash                                       #pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output 
import plotly.graph_objs as go
import pandas as pd                                #pip install pandas
import glob
import os
import dash_bootstrap_components as dbc            #pip install dash-bootstrap-components
from datetime import date
import plotly.express as px
# from wordcloud import wordcloud


path = "C:/Users/Jackie/Documents/VS Code Projects/nigeriadashboard/Data/" # Change path to your data path

all_files = glob.glob (path + "*.csv")

makesalist = [pd.read_csv(filename, encoding= 'latin-1') for filename in all_files]

combined_csv = pd.concat(makesalist, axis= 0, ignore_index= True)


# Adding a column with seperated date and time
combined_csv['date'] = pd.to_datetime(combined_csv['datetime']).dt.date
combined_csv['time'] = pd.to_datetime(combined_csv['datetime']).dt.time

# Creating a dataframe that excludes all 'non-harmful' rows, leaving behind the 4 harmful categories
harmful_df = combined_csv[combined_csv['annotation'] != 'non-harmful']

# Capitalizing the first letter in the platform list 
combined_csv['platform'] = [i.title() for i in (combined_csv['platform'])]

# Replacing the word none in the tweet version column 
combined_csv ['tweet_version'] = combined_csv['tweet_version'].replace('none','fboriginal')

FONT_AWESOME = 'https://use.fontawesome.com/releases/v6.2.1/css/all.css'
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=[FONT_AWESOME])


##############################################################################################
card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

app.layout = html.Div([
    # html.Div([
    #     html.Div([
    #         html.Img(src=app.get_asset_url('deq_logo.png'),
    #                  id = 'deq-image',
    #                  style={'height': '100px',
    #                         'width': 'auto',
    #                         'margin-bottom': '25px'})


    #     ], className='one-third column'),

    #     html.Div([
    #         html.Div([
    #             html.H3('Nigeria 2023 Election Database', style={'margin-bottom': '0px', 'color': 'white'}),
    #             html.H5('Social Media Analysis', style={'margin-bottom': '0px', 'color': 'white'})
    #         ])

    #     ], className='one-half column', id = 'title'),

    #     html.Div([
    #         html.H6('',
    #                 style={'color': 'white'})

    #     ], className='one-third column', id = 'title1'),

    # ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),

############################################# CARDS ################################################    

    html.Div([
        
        html.Div([
            dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(id='content-total-posts', children = "", className="card-title", style= {'color': 'white'}),
                    html.P("Total Posts", className="card-text", style= {'color': 'white'}),
                ], style={'textAlign': 'center'}
            )
        ),
        # dbc.Card(
        #     className="fa fa-globe", 
        #     style={"maxWidth": 75, "color": "white", "textAlign": "center", "fontSize": 30, "margin": "auto" },
        # ),
    ],className='card_container three columns'),]),

    html.Div([
            dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(id='content-harmful-posts', children = "", className="card-title", style= {'color': 'white'}),
                    html.P("Harmful Posts", className="card-text", style= {'color': 'white'}),
                ], style={'textAlign': 'center'}
            )
        ),
        # dbc.Card(
        #     className="fa-solid fa-triangle-exclamation",
        #     style={"maxWidth": 75, "color": "white", "textAlign": "center", "fontSize": 30, "margin": "auto" },
        # ),
    ],className='card_container three columns'),]),

    html.Div([
            dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(id='content-total-users', children = "", className="card-title", style= {'color': 'white'}),
                    html.P("Total Users", className="card-text",style= {'color': 'white'}),
                ], style={'textAlign': 'center'}
            )
        ),
        # dbc.Card(
        #     className="fa-solid fa-users",
        #     style={"maxWidth": 75, "color": "white", "textAlign": "center", "fontSize": 30, "margin": "auto" },
        # )
    ],className='card_container three columns'),]),

    html.Div([
            dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(id='content-harmful-users', children = "", className="card-title", style= {'color': 'white'}),
                    html.P("Harmful Users", className="card-text", style= {'color': 'white'}),
                ], style={'textAlign': 'center'}
            )
        ),
        # dbc.Card(
        #     className="fa-solid fa-triangle-exclamation",
        #     style={"maxWidth": 75, "color": "white", "textAlign": "center", "fontSize": 30, "margin": "auto" },
        # ), 
    ],className='card_container three columns'),]),

    ], className='row flex display'),

############################################## FILTERS ################################################ 

html.Div([
    html.Div([
            html.P('Select Platform', className='fix_label', style= {'color': 'white'}),
            dcc.Dropdown(id = 'platform',
                         multi = True,
                         searchable = False,
                         value ='Twitter',
                         placeholder= 'Select Platform',
                         options = [{'label': c, 'value': c}
                                   for c in (combined_csv['platform'].unique())], 
                                   className='dcc_compon'
                         ),
    ],className='create_container five columns'),

    html.Div([
        html.P('Select Date', className='fix_label', style= {'color': 'white'}),
            dcc.DatePickerRange(id = 'select_daterange',
                                display_format = 'MMM Do, YY',
                                month_format= 'MMMM, YYYY',
                                start_date = pd.to_datetime(("2022/06/24"), format="%Y/%m/%d"),
                                end_date = pd.to_datetime(("2022/08/07"), format="%Y/%m/%d"),
                                start_date_placeholder_text = 'Start Date',
                                end_date_placeholder_text = 'End Date',
                                calendar_orientation = 'horizontal',
                                day_size = 39,
                                with_portal = False,
                                first_day_of_week = 0,
                                reopen_calendar_on_clear = True,
                                is_RTL = False,
                                clearable= True,
                                number_of_months_shown=1,
                                min_date_allowed= date(2022, 6, 24),
                                max_date_allowed= date(2022, 8, 7),
                                minimum_nights=1, 

                                persistence= True,
                                persisted_props= ['start_date'],
                                persistence_type= 'session',

                                updatemode= 'singledate',
                                className= 'dcc_compon',
                                
                               ), 

        ], className='create_container five columns'),
        ], className='row flex display'),

############################################## WORDCLOUDS ################################################ 

#     html.Div([
#         html.Div([
#          dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.H5('Overall Speech',className='text-center',style= {'color': 'white'}),
#                     dcc.Graph(id='wordcloud1', figure={}),
#                 ])
#             ])
#         ],width={'size':12,"offset":0,'order':1},style={'padding-left' : 25,'padding-right' : 25},className='text-center')
#         ], className='create_container five columns'),

#     html.Div([
#          dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.H5('Harmful Speech',className='text-center', style= {'color': 'white'}),
#                     dcc.Graph(id='wordcloud2', figure={}),
#                 ])
#             ])
#         ],width={'size':12,"offset":0,'order':1},style={'padding-left' : 25,'padding-right' : 25},className='text-center')
#         ], className='create_container five columns')
# ], className='row flex display'),

############################################## SUMMARY GRAPHS ####################################################
# donut chart            for     harmful users vs total users
# #stacked bar chart     for     timeseries of twitter and facebook with a line of hate

html.Div([
    # html.Div([
    #      dcc.Graph(id = 'donut_chart',figure={}, config={'displayModeBar': 'hover'})

    #     ], className='create_container four columns'), ########  if you un-comment this donut is four cols, stacked bar eight columns

    html.Div([
            dcc.Graph(id = 'stackedbar_chart', figure={}, config={'displayModeBar': 'hover'})

        ], className='create_container twelve columns')

    ], className='row flex-display'),


############################################## HARMFUL GRAPHS ####################################################
# horizontal bar chart    for   categories
# line chart              for   timeseries of categories

html.Div([
    html.Div([
         dcc.Graph(id = 'horizontalbar_chart', figure={}, config={'displayModeBar': 'hover'})

        ], className='create_container four columns'),

    html.Div([
            dcc.Graph(id = 'line_chart', figure={}, config={'displayModeBar': 'hover'})

        ], className='create_container eight columns')

    ], className='row flex-display'),





    ], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


############################################## CALLBACKS ####################################################


@app.callback(
    Output('content-total-posts','children'),
    Output('content-total-users','children'),
    Input('select_daterange','start_date'),
    Input('select_daterange','end_date'),
    Input('platform','value')
)
def update_totals_cards(start_date, end_date, value_chosen):
    combined_c = combined_csv.copy()
    combined_c['user_id'] = combined_c['user_id'].astype(str)
    combined_c['date'] = pd.to_datetime(combined_c['date'], format="%Y/%m/%d")
    combined_c1 = combined_c[(combined_c['date']>= start_date) & (combined_c['date']<= end_date)]
    

    if type(value_chosen)!= str:
        combined_c2 = combined_c1[(combined_c1['platform'].isin(value_chosen))]
    else:
        combined_c2 = combined_c1[(combined_c1['platform'] == (value_chosen))]

    totalposts = '{:,}'.format(len(combined_c2))
    totalusers = '{:,}'.format(len(combined_c2['user_id'].unique()))

    return totalposts, totalusers

############################################# CALLBACKS ##########################################################

@app.callback(
    Output('content-harmful-posts','children'),
    Output('content-harmful-users','children'),
    Input('select_daterange','start_date'),
    Input('select_daterange','end_date'),
    Input('platform','value')
)
def update_harmful_cards(start_date, end_date, value_chosen):
    combined_h = combined_csv.copy()
    combined_h['user_id'] = combined_h['user_id'].astype(str)
    combined_h['date'] = pd.to_datetime(combined_h['date'], format="%Y/%m/%d")
    combined_h1 = combined_h[(combined_h['date']>= start_date) & (combined_h['date']<= end_date)]
    combined_h2 = combined_h1.query("annotation != 'non-harmful'")


    if type(value_chosen)!= str:
        combined_h3 = combined_h2[(combined_h2['platform'].isin(value_chosen))]
    else:
        combined_h3 = combined_h2[(combined_h2['platform'] == (value_chosen))]
    
    totalhate = '{:,}'.format(len(combined_h3))
    totalhateusers = '{:,}'.format(len(combined_h3['user_id'].unique()))

    return totalhate, totalhateusers



############################################## CALLBACKS ####################################################

@app.callback(
    Output('stackedbar_chart', 'figure'),
    Input('select_daterange','start_date'),
    Input('select_daterange','end_date'),
    Input('platform','value')
)
def update_stacked_chart(start_date, end_date, value_chosen):
    combined_t = combined_csv.copy()
    combined_t['user_id'] = combined_t['user_id'].astype(str)
    combined_t['date'] = pd.to_datetime(combined_t['date'], format="%Y/%m/%d")
    mapping = {'non-harmful': 0, 'hate speech': 1, 'offensive speech': 1, 'threatening speech': 1 , 'calls for violence' :1 }
    combined_t['annotation'] = combined_t['annotation'].map(mapping)
    combined_t['tweet_version'] = combined_t['tweet_version'].replace('none','fboriginal')
    combined_t = combined_t.groupby(['date','platform','tweet_version'], as_index = False).agg({'user_id': 'count', 'annotation': 'sum'})
    combined_t_pivot = combined_t.pivot_table(index = ['date','platform'], columns='tweet_version',
                                                values={'user_id':'count', 'annotation':'sum'})
    combined_t_pivot.columns = [f'{i}{j}' for i, j in combined_t_pivot.columns]
    combined_t_pivot = combined_t_pivot.fillna(0)
    combined_t1 = combined_t_pivot.reset_index()
    combined_t1.loc[:, 'harmfulcount'] = combined_t1[['annotationfboriginal','annotationoriginal','annotationretweet']].sum(axis=1)
    combined_t1 = combined_t1.rename(columns=lambda x: x.strip())

    combined_t2 = combined_t1[(combined_t1['date']>= start_date) & (combined_t1['date']<= end_date)]

    if type(value_chosen)!= str:
        combined_t3 = combined_t2[(combined_t2['platform'].isin(value_chosen))]
    else:
        combined_t3 = combined_t2[(combined_t2['platform'] == (value_chosen))]

    

    return {
        'data': [
            go.Bar(
                x=combined_t3['date'],
                y=combined_t3['user_idoriginal'],
                offsetgroup=0,
                marker = dict(color = '#5CB855'), #Light Green
                name='Original Tweets',
                hoverinfo='text',
                hovertext=
                         '<b>Category</b>: ' + combined_t3['user_idoriginal'].astype(str) + '<br>' +
                        '<b>Count</b>: ' + combined_t3['user_idoriginal'].astype(str) + '<br>'
            ),

            go.Bar(
                x=combined_t3['date'],
                y=combined_t3['user_idretweet'],
                offsetgroup=0,
                base= combined_t3['user_idoriginal'],
                marker = dict(color = '#295B28'), #dark green
                name='Retweets',
                hoverinfo='text',
                hovertext=
                         '<b>Category</b>: ' + combined_t3['user_idretweet'].astype(str) + '<br>' +
                        '<b>Count</b>: ' + combined_t3['user_idretweet'].astype(str) + '<br>' 
            ),

            go.Bar(
                x=combined_t3['date'],
                y=combined_t3['user_idfboriginal'],
                offsetgroup=1,
                base = 0,
                marker = dict(color = '#4267B2'), # dark blue
                name='Facebook Posts',
                hovertext=
                         '<b>Category</b>: ' + combined_t3['user_idfboriginal'].astype(str) + '<br>' +
                        '<b>Count</b>: ' + combined_t3['user_idfboriginal'].astype(str) + '<br>' 
                
            ),

            go.Scatter(
                x=combined_t3['date'],
                y=combined_t3['harmfulcount'], 
                name='Harmful Total',
                marker = dict(color='red'),
                hovertext=
                         '<b>Category</b>: ' + combined_t3['harmfulcount'].astype(str) + '<br>' +
                        '<b>Count</b>: ' + combined_t3['harmfulcount'].astype(str) + '<br>' 

                ),
        ],


        'layout': go.Layout(
            barmode = 'group',
            title={'text': 'Prevelance Of Harmful Language' ,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#000000',
                       'size': 12},
            font=dict(family='Questrial',
                      color='#000000',
                      size=12),
            paper_bgcolor='#F6F6F6',
            plot_bgcolor='#F6F6F6',
            legend={'bgcolor': '#F6F6F6'},
                    # 'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            #margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>'),
                    #    tick0 = 0,
                    #    dtick = 1,
                    #    color = '#000000',
                    #    showline=True,
                    #    showgrid=False,
                    # #    showticklabels=True,
                    #    linecolor='#000000',
                    #    linewidth=1,
                    # #    ticks='outside',
                    # #    tickfont=dict(
                    # #        family='Questrial',
                    # #        color='#000000',
                    # #        size=8)
                    #    ),
            yaxis=dict(title='<b>Comparison of Harmful Posts to Total Posts</b>',
                    #    color='#000000',
                    #    showline=True,
                    #    showgrid=False,
                    # #    showticklabels=True,
                    #    linecolor='#000000',
                    #    linewidth=1,
                    # #    ticks='outside',
                    # #    tickfont=dict(
                    # #        family='Questrial',
                    # #        color='white',
                    # #        size=8
                    # #    )
  
        )
        )

        }
############################################## CALLBACKS ####################################################

@app.callback(
    Output('horizontalbar_chart', 'figure'),
    Input('select_daterange','start_date'),
    Input('select_daterange','end_date'),
    Input('platform','value')
)
def update_horizontal_chart(start_date, end_date, value_chosen):
    combined_b = combined_csv.copy()
    combined_b['user_id'] = combined_b['user_id'].astype(str)
    combined_b['date'] = pd.to_datetime(combined_b['date'], format="%Y/%m/%d")
    combined_b1 = combined_b[(combined_b['date']>= start_date) & (combined_b['date']<= end_date)]
    combined_b2 = combined_b1.query("annotation != 'non-harmful'")


    if type(value_chosen)!= str:
        combined_b3 = combined_b2[(combined_b2['platform'].isin(value_chosen))]
    else:
        combined_b3 = combined_b2[(combined_b2['platform'] == (value_chosen))]

    combined_b4 = combined_b3['annotation'].value_counts().reset_index()
    combined_b4.columns = ['harm_annotations', 'count']

    colors = ['rgb(34, 173, 136)', 'rgb(207, 96, 19)',
          'rgb(131, 10, 86)', 'rgb(37, 103, 211)',
            ] 
    
    return {
        'data': [go.Bar(
            x = combined_b4['count'],
            y = combined_b4['harm_annotations'],
            name = 'Harmful Categories',
            orientation = 'h',
            marker = dict(color = colors),
            hoverinfo='text',
            hovertext=
            '<b>Category</b>: ' + combined_b4['harm_annotations'].astype(str) + '<br>' +
            '<b>Count</b>: ' + combined_b4['count'].astype(str) + '<br>' 
            
        )],
        
        'layout': go.Layout(
            title={'text': 'Harmful Language Categories' ,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#000000',
                       'size': 12},
            font=dict(family='Questrial',
                      color='#000000',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#F6F6F6',
            plot_bgcolor='#F6F6F6',
            legend={'bgcolor': '#F6F6F6'}
        )
    }

############################################## CALLBACKS ####################################################

@app.callback(
    Output('line_chart', 'figure'),
    Input('select_daterange','start_date'),
    Input('select_daterange','end_date'),
    Input('platform','value')
)
def update_line_chart(start_date, end_date, value_chosen):
    combined_t = combined_csv.copy()
    combined_t['user_id'] = combined_t['user_id'].astype(str)
    combined_t['date'] = pd.to_datetime(combined_t['date'], format="%Y/%m/%d")
    combined_t1 = combined_t[(combined_t['date']>= start_date) & (combined_t['date']<= end_date)]
    combined_t2 = combined_t1.query("annotation != 'non-harmful'")


    if type(value_chosen)!= str:
        combined_t3 = combined_t2[(combined_t2['platform'].isin(value_chosen))]
    else:
        combined_t3 = combined_t2[(combined_t2['platform'] == (value_chosen))]

    combined_t4 = combined_t3.groupby(['date','annotation'])['user_id'].count()
    combined_t5 = combined_t4.reset_index()

    fig_line = px.line(combined_t5, x= 'date', y = 'user_id', color='annotation', 
    color_discrete_map= {"offensive speech" : "rgb(34, 173, 136)" ,
                         "threatening speech": "rgb(207, 96, 19)", 
                         "calls for violence" : "rgb(37, 103, 211)",
                         "hate speech" : "rgb(131, 10, 86)"},
                    title= "Harmful Categories by Date" ,
                    )
    fig_line.update_traces(mode="lines", connectgaps=True)
    fig_line.update_layout( #margin=dict(l=20, r=20, t=30, b=20), 
                            yaxis={'title':'Harmful Categories'},xaxis={'title':'Date'},
                            titlefont={'color': '#000000','size': 12},
                            font=dict(family='Questrial',
                            color='#000000',
                            size=12),
                            paper_bgcolor='#F6F6F6',
                            plot_bgcolor='#F6F6F6',
                            legend={'bgcolor': '#F6F6F6'} )


    return fig_line




# ############################################## CALLBACKS ####################################################
# #word cloud 1

# @app.callback(
#     Output('wordcloud1', 'figure'),
#     Input('select_daterange','start_date'),
#     Input('select_daterange','end_date'),
#     Input('platform','value')
# )

# def update_totals_cards(start_date, end_date, value_chosen):
#     combined_c = combined_csv.copy()
#     combined_c['user_id'] = combined_c['user_id'].astype(str)
#     combined_c['date'] = pd.to_datetime(combined_c['date'], format="%Y/%m/%d")
#     combined_c1 = combined_c[(combined_c['date']>= start_date) & (combined_c['date']<= end_date)]
    

#     if type(value_chosen)!= str:
#         combined_c2 = combined_c1[(combined_c1['platform'].isin(value_chosen))]
#     else:
#         combined_c2 = combined_c1[(combined_c1['platform'] == (value_chosen))]

#     combined_c3 = combined_c2 ['text']    

#     my_wordcloud1 = wordcloud(
#         background_color='white',
#         height=275
#     ).generate(' '.join(combined_c3))

#     fig_wordcloud1 = px.imshow(my_wordcloud1, template='ggplot2',
#                               title="This shows some of the words that appear in the overall tweets collected")
#     fig_wordcloud1.update_layout(margin=dict(l=20, r=20, t=30, b=20))
#     fig_wordcloud1.update_xaxes(visible=False)
#     fig_wordcloud1.update_yaxes(visible=False)

#     return fig_wordcloud1



# ############################################## CALLBACKS ####################################################
# @app.callback(
#     Output('wordcloud1', 'figure'),
#     Input('select_daterange','start_date'),
#     Input('select_daterange','end_date'),
#     Input('platform','value')
# )

# def update_harmful_cards(start_date, end_date, value_chosen):
#     combined_h = combined_csv.copy()
#     combined_h['user_id'] = combined_h['user_id'].astype(str)
#     combined_h['date'] = pd.to_datetime(combined_h['date'], format="%Y/%m/%d")
#     combined_h1 = combined_h[(combined_h['date']>= start_date) & (combined_h['date']<= end_date)]
#     combined_h2 = combined_h1.query("annotation != 'non-harmful'")


#     if type(value_chosen)!= str:
#         combined_h3 = combined_h2[(combined_h2['platform'].isin(value_chosen))]
#     else:
#         combined_h3 = combined_h2[(combined_h2['platform'] == (value_chosen))]

#     combined_h4 = combined_h3 ['text']    

#     my_wordcloud1 = wordcloud(
#         background_color='white',
#         height=275
#     ).generate(' '.join(combined_h4))

#     fig_wordcloud2 = px.imshow(my_wordcloud1, template='ggplot2',
#                               title="This shows some of the words that appear in the harmful tweets collected")
#     fig_wordcloud2.update_layout(margin=dict(l=20, r=20, t=30, b=20))
#     fig_wordcloud2.update_xaxes(visible=False)
#     fig_wordcloud2.update_yaxes(visible=False)

#     return fig_wordcloud2





















if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)