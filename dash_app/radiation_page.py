import os, sys
# import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import MySQLdb as mdb
import datetime

import plotly.graph_objs as go
# from dash.dependencies import Input, Output, MATCH, ALL, State

WSRADID = 1
# build the path to import config.py from the parent directory
sys.path.append('../')
import config


def build_graphRAD_figure():
    
    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )
 
    
    
    #last 7 days 
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp, uSVh, uSVh24Hour FROM RAD433MHZ WHERE (TimeStamp > '%s') ORDER BY timestamp"% (before) 
    df = pd.read_sql(query, con )
    trace1 = go.Scatter(x=df.timestamp, y=df.uSVh, name='uSVh')
    trace2 = go.Scatter(x=df.timestamp, y=df.uSVh24Hour, name='24HourRAD',line=dict(width=3,color = "red" ))

    figure={
    'data': [trace1, trace2 ],
    'layout':
    go.Layout(title='WeatherSense Radiation', xaxis_title="Updated at: "+nowTime, yaxis_title="uSv/h") }
    con.close()

    return figure


def build_graph1_figure():
    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )

    #last 7 days 
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM RAD433MHZ WHERE (TimeStamp > '%s') AND (deviceid = %d) ORDER BY timestamp"% (before,WSRADID) 
    # print("query=", query)
    df = pd.read_sql(query, con )


    trace1 = go.Scatter(x=df.timestamp, y=df.batteryvoltage, name='battery voltage')
    trace2 = go.Scatter(x=df.timestamp, y=df.solarvoltage, name='solar voltage')
    trace3 = go.Scatter(x=df.timestamp, y=df.loadvoltage, name='load voltage')
    trace4 = go.Scatter(x=df.timestamp, y=df.auxa, name='Aux State')

    figure={
    'data': [trace1, trace2, trace3, trace4],
    'layout':
    go.Layout(title='WeatherSenseRadSense Solar Voltages', xaxis_title="Updated at: "+nowTime, yaxis_title="Voltage (V)") }
    con.close()

    return figure


def build_graph2_figure():
    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )
 
    
    
    #last 7 days 
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM RAD433MHZ WHERE (TimeStamp > '%s') AND (deviceid = %d) ORDER BY timestamp"% (before, WSRADID) 
    df = pd.read_sql(query, con )
    trace1c = go.Scatter(x=df.timestamp, y=df.batterycurrent, name='battery current')
    trace2c = go.Scatter(x=df.timestamp, y=df.solarcurrent, name='solar current')
    trace3c = go.Scatter(x=df.timestamp, y=df.loadcurrent, name='load current')
    figure={
    'data': [trace1c, trace2c, trace3c],
    'layout':
    go.Layout(title='WeatherSense Radiation Solar Currents', xaxis_title="Updated at: "+nowTime, yaxis_title="Current (mA)") }

    con.close()

    return figure


def RadiationPage():

    layout = html.Div(children=[

    html.H1("Radiation Charts", style={'textAlign': 'center'}),

    dcc.Graph(
        id={'type': 'RADgraph', 'index': "1"},
        figure=build_graphRAD_figure(),
    ),

    dcc.Graph(
    id={'type' : 'RADgraph', 'index' : "2"},
    figure = build_graph1_figure(),
    ),

    dcc.Graph(
    id={'type' : 'RADgraph', 'index' : "3"},
    figure = build_graph2_figure(),
    ) ,

    ], className="container" )

    # con.close()
    return layout
