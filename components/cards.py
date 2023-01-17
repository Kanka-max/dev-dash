from dash import Dash, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output 
import pandas as pd                               #pip install pandas
import glob


app = Dash(__name__)

def cards_layout(app:Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div(
                className="cards-container",
                children=[
                    html.Div(
                        className="content",
                        children=[
                            html.H4("Overview of harmful language"),
                            html.P("The following table shows the total number of messages collected over the selected time period and across the selected platform(s). It also shows the total number of active users vs the number of users that spread harmful content."),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        className="card",
                                        id='content-total-posts',
                                        children=[
                                            html.H5("Total Posts"),
                                            html.H2(""), #the value of the total posts
                                            # html.H6("(5.53%)") #percentage
                                        ]
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        className="card",
                                        id='content-harmful-posts',
                                        children=[
                                            html.H5("Total Harmful Posts"),
                                            html.H2(""), #the value of the total harmful posts
                                            # html.H6("(5.53%)") #percentage
                                        ]
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        className="card",
                                        id='content-total-users',
                                        children=[
                                            html.H5("Total Users"),
                                            html.H2(""), #the value of the total users
                                            # html.H6("(5.53%)") #percentage
                                        ]
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        className="card",
                                        id='content-harmful-users',
                                        children=[
                                            html.H5("Total Harmful Users"),
                                            html.H2(""), #the value of the total harmful users
                                            # html.H6("(5.53%)") #percentage
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            )
        ]
    )

########################################## READING IN THE DATA ##########################################

path = "C:/Users/Jackie/Documents/Pull From Github/dash-layout/Data/" # Change path to your data path

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

############################################# HARMFUL CARDS CALLBACKS ##########################################################

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