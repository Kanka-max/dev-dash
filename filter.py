from dash import Dash, html
import dash_bootstrap_components as dbc
from dash import dcc
import pandas as pd
from datetime import date
import glob

path = "C:/Users/Jackie/Documents/Pull From Github/dash-layout/Data/" # Change path to your data path

all_files = glob.glob (path + "*.csv")

makesalist = [pd.read_csv(filename, encoding= 'latin-1') for filename in all_files]

combined_csv = pd.concat(makesalist, axis= 0, ignore_index= True)

# Capitalizing the first letter in the platform list 
combined_csv['platform'] = [i.title() for i in (combined_csv['platform'])]

app = Dash(__name__)

def filter_layout(app:Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div(
                className="filters-container",
                children=[
                    html.Div(
                        className="content",
                        children=[
                            html.H4("Selection Options"),
                            html.P("The Nigerian Harmful Language Monitor offers two selection options:"),
                            html.P("- Select the date period (default setting will be the full date range of the data available) "),
                            html.P("- Select the platform (default setting will be to see Twitter and Facebook data)"),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        className="filter",
                                        children=[
                                            html.Label("Date"),
                                            dcc.DatePickerRange(
                                                id = 'select_daterange',
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
            
                                                
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        className="filter",
                                        children=[
                                            html.Label("Platform"),
                                              dcc.Dropdown(
                                                id = 'platform',
                                                multi = True,
                                                searchable = False,
                                                value ='Twitter',
                                                placeholder= 'Select Platform',
                                                options=[{'label': c, 'value': c}
                                                        for c in (combined_csv['platform'].unique())
                                                ],
                                            )
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