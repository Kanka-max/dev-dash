import dash  # pip install dash
from dash import html
from dash import dcc
from dash import dash, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd  # pip install pandas
import glob
import os
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from datetime import date
import plotly.express as px

import boto3

# from wordcloud import wordcloud


########################################## READING IN THE DATA ##########################################

path = "Data/"  # Change path to your data path

all_files = glob.glob(path + "*.csv")

makesalist = [pd.read_csv(filename, encoding="latin-1") for filename in all_files]

combined_csv = pd.concat(makesalist, axis=0, ignore_index=True)


# Adding a column with seperated date and time
combined_csv["date"] = pd.to_datetime(combined_csv["datetime"]).dt.date
combined_csv["time"] = pd.to_datetime(combined_csv["datetime"]).dt.time

# Creating a dataframe that excludes all 'non-harmful' rows, leaving behind the 4 harmful categories
harmful_df = combined_csv[combined_csv["annotation"] != "non-harmful"]

# Capitalizing the first letter in the platform list
combined_csv["platform"] = [i.title() for i in (combined_csv["platform"])]

# Replacing the word none in the tweet version column
combined_csv["tweet_version"] = combined_csv["tweet_version"].replace(
    "none", "fboriginal"
)

######################################INITIALIZE##################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


app.layout = html.Div(
    [
        html.Div(
            children=[
                html.Div(
                    className="cards-container",
                    children=[
                        html.Div(
                            className="content",
                            children=[
                                html.H4("Overview of harmful language"),
                                html.P(
                                    "The following table shows the total number of messages collected over the selected time period and across the selected platform(s). It also shows the total number of active users vs the number of users that spread harmful content."
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5("Total Posts"),
                                                html.H2(
                                                    id="content-total-posts",
                                                    children="",
                                                ),  # the value of the total harmful users
                                                # html.H6("(5.53%)") #percentage
                                            ],
                                            className="card",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5("Total Harmful Posts"),
                                                html.H2(
                                                    id="content-harmful-posts",
                                                    children="",
                                                ),  # the value of the total harmful users
                                                # html.H6("(5.53%)") #percentage
                                            ],
                                            className="card",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5("Total Users"),
                                                html.H2(
                                                    id="content-total-users",
                                                    children="",
                                                ),  # the value of the total harmful users
                                                # html.H6("(5.53%)") #percentage
                                            ],
                                            className="card",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5("Total Harmful Users"),
                                                html.H2(
                                                    id="content-harmful-users",
                                                    children="",
                                                ),  # the value of the total harmful users
                                                # html.H6("(5.53%)") #percentage
                                            ],
                                            className="card",
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ],
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    className="filters-container",
                    children=[
                        html.Div(
                            className="content",
                            children=[
                                html.H4("Selection Options"),
                                html.P(
                                    "The Nigerian Harmful Language Monitor offers two selection options:"
                                ),
                                html.P(
                                    "- Select the date period (default setting will be the full date range of the data available) "
                                ),
                                html.P(
                                    "- Select the platform (default setting will be to see Twitter and Facebook data)"
                                ),
                            ],
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
                                                    id="select_daterange",
                                                    display_format="MMM Do, YY",
                                                    month_format="MMMM, YYYY",
                                                    start_date=pd.to_datetime(
                                                        ("2022/06/24"),
                                                        format="%Y/%m/%d",
                                                    ),
                                                    end_date=pd.to_datetime(
                                                        ("2022/08/07"),
                                                        format="%Y/%m/%d",
                                                    ),
                                                    start_date_placeholder_text="Start Date",
                                                    end_date_placeholder_text="End Date",
                                                    calendar_orientation="horizontal",
                                                    day_size=39,
                                                    with_portal=False,
                                                    first_day_of_week=0,
                                                    reopen_calendar_on_clear=True,
                                                    is_RTL=False,
                                                    clearable=True,
                                                    number_of_months_shown=1,
                                                    min_date_allowed=date(2022, 6, 24),
                                                    max_date_allowed=date(2022, 8, 7),
                                                    minimum_nights=1,
                                                    persistence=True,
                                                    persisted_props=["start_date"],
                                                    persistence_type="session",
                                                    updatemode="singledate",
                                                ),
                                            ],
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
                                                    id="platform",
                                                    multi=True,
                                                    searchable=False,
                                                    value="Twitter",
                                                    placeholder="Select Platform",
                                                    options=[
                                                        {"label": c, "value": c}
                                                        for c in (
                                                            combined_csv[
                                                                "platform"
                                                            ].unique()
                                                        )
                                                    ],
                                                ),
                                            ],
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ],
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    className="barchart-container",
                    children=[
                        html.Div(
                            className="content",
                            children=[
                                html.P(
                                    "The chart shows the number of messages spreading more concretely over the selected period of time: "
                                ),
                            ],
                        ),
                        # insert bar chart here
                        html.Div(
                            [
                                dcc.Graph(
                                    id="stackedbar_chart",
                                    figure={},
                                    config={"displayModeBar": "hover"},
                                )
                            ]
                        ),
                    ],
                )
            ]
        ),
        html.Div(
            className="category-container",
            children=[
                html.Div(
                    className="content",
                    children=[
                        html.H4("Understanding the severity of harmful language"),
                        html.P(
                            "Harm can be created at different levels. We differentiate between offensive speech, hateful speech, threatening speech, and calls to violence. It is anticipated that the less aggressive levels (offensive speech) will be the more prevalent. "
                        ),
                    ],
                ),
                # insert horizontal chart here
                html.Div(
                    [
                        dcc.Graph(
                            id="horizontalbar_chart",
                            figure={},
                            config={"displayModeBar": "hover"},
                        ),
                        dcc.Graph(
                            id="line_chart",
                            figure={},
                            config={"displayModeBar": "hover"},
                        ),
                    ]
                ),
            ],
        ),
    ]
)


############################################## TOTALS CARDS CALLBACKS ####################################################


@app.callback(
    Output("content-total-posts", "children"),
    Output("content-total-users", "children"),
    Input("select_daterange", "start_date"),
    Input("select_daterange", "end_date"),
    Input("platform", "value"),
)
def update_totals_cards(start_date, end_date, value_chosen):
    combined_c = combined_csv.copy()
    combined_c["user_id"] = combined_c["user_id"].astype(str)
    combined_c["date"] = pd.to_datetime(combined_c["date"], format="%Y/%m/%d")
    combined_c1 = combined_c[
        (combined_c["date"] >= start_date) & (combined_c["date"] <= end_date)
    ]

    if type(value_chosen) != str:
        combined_c2 = combined_c1[(combined_c1["platform"].isin(value_chosen))]
    else:
        combined_c2 = combined_c1[(combined_c1["platform"] == (value_chosen))]
    totalposts = "{:,}".format(len(combined_c2))
    totalusers = "{:,}".format(len(combined_c2["user_id"].unique()))

    return totalposts, totalusers


############################################# HARMFUL CARDS CALLBACKS ##########################################################


@app.callback(
    Output("content-harmful-posts", "children"),
    Output("content-harmful-users", "children"),
    Input("select_daterange", "start_date"),
    Input("select_daterange", "end_date"),
    Input("platform", "value"),
)
def update_harmful_cards(start_date, end_date, value_chosen):
    combined_h = combined_csv.copy()
    combined_h["user_id"] = combined_h["user_id"].astype(str)
    combined_h["date"] = pd.to_datetime(combined_h["date"], format="%Y/%m/%d")
    combined_h1 = combined_h[
        (combined_h["date"] >= start_date) & (combined_h["date"] <= end_date)
    ]
    combined_h2 = combined_h1.query("annotation != 'non-harmful'")

    if type(value_chosen) != str:
        combined_h3 = combined_h2[(combined_h2["platform"].isin(value_chosen))]
    else:
        combined_h3 = combined_h2[(combined_h2["platform"] == (value_chosen))]
    totalhate = "{:,}".format(len(combined_h3))
    totalhateusers = "{:,}".format(len(combined_h3["user_id"].unique()))

    return totalhate, totalhateusers


############################################## BAR CALLBACKS ####################################################


@app.callback(
    Output("stackedbar_chart", "figure"),
    Input("select_daterange", "start_date"),
    Input("select_daterange", "end_date"),
    Input("platform", "value"),
)
def update_stacked_chart(start_date, end_date, value_chosen):
    combined_t = combined_csv.copy()
    combined_t["user_id"] = combined_t["user_id"].astype(str)
    combined_t["date"] = pd.to_datetime(combined_t["date"], format="%Y/%m/%d")
    mapping = {
        "non-harmful": 0,
        "hate speech": 1,
        "offensive speech": 1,
        "threatening speech": 1,
        "calls for violence": 1,
    }
    combined_t["annotation"] = combined_t["annotation"].map(mapping)
    combined_t["tweet_version"] = combined_t["tweet_version"].replace(
        "none", "fboriginal"
    )
    combined_t = combined_t.groupby(
        ["date", "platform", "tweet_version"], as_index=False
    ).agg({"user_id": "count", "annotation": "sum"})
    combined_t_pivot = combined_t.pivot_table(
        index=["date", "platform"],
        columns="tweet_version",
        values={"user_id": "count", "annotation": "sum"},
    )
    combined_t_pivot.columns = [f"{i}{j}" for i, j in combined_t_pivot.columns]
    combined_t_pivot = combined_t_pivot.fillna(0)
    combined_t1 = combined_t_pivot.reset_index()
    combined_t1.loc[:, "harmfulcount"] = combined_t1[
        ["annotationfboriginal", "annotationoriginal", "annotationretweet"]
    ].sum(axis=1)
    combined_t1 = combined_t1.rename(columns=lambda x: x.strip())

    combined_t2 = combined_t1[
        (combined_t1["date"] >= start_date) & (combined_t1["date"] <= end_date)
    ]

    if type(value_chosen) != str:
        combined_t3 = combined_t2[(combined_t2["platform"].isin(value_chosen))]
    else:
        combined_t3 = combined_t2[(combined_t2["platform"] == (value_chosen))]
    return {
        "data": [
            go.Bar(
                x=combined_t3["date"],
                y=combined_t3["user_idoriginal"],
                offsetgroup=0,
                marker=dict(color="#5CB855"),  # Light Green
                name="Original Tweets",
                hoverinfo="text",
                opacity=0.7,
                hovertext="<b>Original Tweets</b>: "
                + "<b>Count</b>: "
                + combined_t3["user_idoriginal"].astype(str)
                + "<br>",
            ),
            go.Bar(
                x=combined_t3["date"],
                y=combined_t3["user_idretweet"],
                offsetgroup=0,
                base=combined_t3["user_idoriginal"],
                marker=dict(color="#295B28"),  # dark green
                name="Retweets",
                hoverinfo="text",
                hovertext="<b>Retweets</b>: "
                + "<b>Count</b>: "
                + combined_t3["user_idretweet"].astype(str)
                + "<br>",
            ),
            go.Bar(
                x=combined_t3["date"],
                y=combined_t3["user_idfboriginal"],
                offsetgroup=1,
                base=0,
                marker=dict(color="#4267B2"),
                # opacity = 0.7,# dark blue
                name="Facebook Posts",
                hovertext="<b>Facebook Posts</b>: "
                + "<b>Count</b>: "
                + combined_t3["user_idfboriginal"].astype(str)
                + "<br>",
            ),
            go.Scatter(
                x=combined_t3["date"],
                y=combined_t3["harmfulcount"],
                name="Total Harmful",
                marker=dict(color="red"),
                hovertext="<b>Total Harmful Posts</b>: "
                + "<b>Count</b>: "
                + combined_t3["harmfulcount"].astype(str)
                + "<br>",
            ),
        ],
        "layout": go.Layout(
            barmode="group",
            yaxis={"title": "<b>Total Posts </b>"},
            xaxis={"title": "<b>Date</b>"},
            titlefont=dict(family="v", color="#000000", size=13),
            font=dict(family="Arial", color="#000000", size=13),
            paper_bgcolor="#E0E1E0",
            plot_bgcolor="#E0E1E0",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="auto", x=1),
            # legend={'bgcolor': '#F6F6F6'},
            # 'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            # margin=dict(r=0),
            # xaxis=dict(title='<b>Date</b>'),
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
            # yaxis=dict(title='<b>Comparison of Harmful Posts to Total Posts</b>',
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
            # )
        ),
    }


############################################## CATEGORY 1 CALLBACKS ####################################################


@app.callback(
    Output("horizontalbar_chart", "figure"),
    Input("select_daterange", "start_date"),
    Input("select_daterange", "end_date"),
    Input("platform", "value"),
)
def update_horizontal_chart(start_date, end_date, value_chosen):
    combined_b = combined_csv.copy()
    combined_b["user_id"] = combined_b["user_id"].astype(str)
    combined_b["date"] = pd.to_datetime(combined_b["date"], format="%Y/%m/%d")
    combined_b1 = combined_b[
        (combined_b["date"] >= start_date) & (combined_b["date"] <= end_date)
    ]
    combined_b2 = combined_b1.query("annotation != 'non-harmful'")

    if type(value_chosen) != str:
        combined_b3 = combined_b2[(combined_b2["platform"].isin(value_chosen))]
    else:
        combined_b3 = combined_b2[(combined_b2["platform"] == (value_chosen))]
    combined_b4 = combined_b3["annotation"].value_counts().reset_index()
    combined_b4.columns = ["harm_annotations", "count"]

    colors = [
        "rgb(34, 173, 136)",
        "rgb(207, 96, 19)",
        "rgb(131, 10, 86)",
        "rgb(37, 103, 211)",
    ]

    return {
        "data": [
            go.Bar(
                x=combined_b4["count"],
                y=combined_b4["harm_annotations"],
                name="Harmful Categories",
                orientation="h",
                marker=dict(color=colors),
                hoverinfo="text",
                width=[0.8, 0.8, 0.8, 0.8, 0.8],
                hovertext="<b>Category</b>: "
                + combined_b4["harm_annotations"].astype(str)
                + "<br>"
                + "<b>Count</b>: "
                + combined_b4["count"].astype(str)
                + "<br>",
            )
        ],
        "layout": go.Layout(
            # yaxis={'title':'Total Count of Harmful Language Categories'},
            xaxis={"title": "<b>Levels Of Harmful Speech</b>", "showticklabels": True},
            titlefont=dict(family="Arial", color="#000000", size=13),
            yaxis=dict(showline=False),
            font=dict(family="Arial", color="#000000", size=13),
            hovermode="x",
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,  # gap between bars of the same location coordinate.
            paper_bgcolor="#E0E1E0",
            plot_bgcolor="#E0E1E0",
            legend={"bgcolor": "#F6F6F6"},
            margin=dict(l=150, b = 180),
        ),
    }


############################################## CATEGORY 2 CALLBACKS ####################################################


@app.callback(
    Output("line_chart", "figure"),
    Input("select_daterange", "start_date"),
    Input("select_daterange", "end_date"),
    Input("platform", "value"),
)
def update_line_chart(start_date, end_date, value_chosen):
    combined_t = combined_csv.copy()
    combined_t["user_id"] = combined_t["user_id"].astype(str)
    combined_t = combined_t.rename(columns={"user_id": "harmful_annotation_count"})
    combined_t["date"] = pd.to_datetime(combined_t["date"], format="%Y/%m/%d")
    combined_t1 = combined_t[
        (combined_t["date"] >= start_date) & (combined_t["date"] <= end_date)
    ]
    combined_t2 = combined_t1.query("annotation != 'non-harmful'")

    if type(value_chosen) != str:
        combined_t3 = combined_t2[(combined_t2["platform"].isin(value_chosen))]
    else:
        combined_t3 = combined_t2[(combined_t2["platform"] == (value_chosen))]
    combined_t4 = combined_t3.groupby(["date", "annotation"])[
        "harmful_annotation_count"
    ].count()
    combined_t5 = combined_t4.reset_index()

    fig_line = px.line(
        combined_t5,
        x="date",
        y="harmful_annotation_count",
        color="annotation",
        color_discrete_map={
            "offensive speech": "rgb(34, 173, 136)",
            "threatening speech": "rgb(207, 96, 19)",
            "calls for violence": "rgb(37, 103, 211)",
            "hate speech": "rgb(131, 10, 86)",
        },
        title="Harmful Categories by Date",
    )

    fig_line.update_traces(mode="markers+lines", connectgaps=True, hovertemplate=None)
    fig_line.update_layout(hovermode="x")
    fig_line.update_layout(
        margin=dict(l = 100, t= 100, r = 100),
        # r=20, t=30, b=20),
        yaxis=dict(
            title="<b>Frequency</b>",
            color="#000000",
            showline=True,
            linecolor="#000000",
            showticklabels=True,
            showgrid = False,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=14,
                color="rgb(82, 82, 82)",
            ),
        ),
        xaxis=dict(
            title="<b>Date</b>",
            color="#000000",
            showline=True,
            showgrid=False,
            linecolor="#000000",
            showticklabels=True,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=14,
                color="rgb(82, 82, 82)",
            ),
        ),
        titlefont=dict(family="Arial", color="#000000", size=13),
        font=dict(family="Arial", color="#000000", size=13),
        paper_bgcolor="#E0E1E0",
        plot_bgcolor="#E0E1E0",
        legend=dict(
            x=1,
            y=1,
            traceorder="reversed",
            title_font_family="Arial",
            font=dict(family="Arial", size=12, color="black"),
            bgcolor="#F1F4F3",
            bordercolor="#058B54",
            borderwidth=1,
        ),
        
    )

    return fig_line


def main() -> None:
    app.title = "Monitor"


if __name__ == "__main__":
    main()
    app.run_server(debug=True, use_reloader=True, port=8080)
