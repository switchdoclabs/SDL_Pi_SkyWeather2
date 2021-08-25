# import os
import sys
# import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import MySQLdb as mdb
import datetime

import plotly.graph_objs as go
# from dash.dependencies import Input, Output, MATCH, ALL, State

# build the path to import config.py from the parent directory
sys.path.append('../')
import config

WSLGHTID = 1

ASJSON={}
ASJSON["LastEarthquake"]= "N/A"
ASJSON["LastEQSI"]= "N/A"
ASJSON["LastEQPGA"]= "N/A"
ASJSON["InstantEQSI"]= "N/A"
ASJSON["InstantEQPGA"]= "N/A"
ASJSON["EQCount"]= "N/A"
ASJSON["UnitID"]= "N/A"
ASJSON["LastMessageID"]= "N/A"

def updateAfterShockLines():

    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )

    cur = con.cursor()
    # build the data array

    timeDelta = datetime.timedelta(days=14)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')

    query = "SELECT timestamp, eqcount, deviceid, keepalivemessage from AS433MHZ WHERE (keepalivemessage = 0) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1 " % WSLGHTID
    #print("queryA=", query)
    cur.execute(query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["LastEarthquake"] = records[0][0].strftime('%Y-%m-%d %H:%M:%S')
        ASJSON["EQCount"] = records[0][1]
    else:
        ASJSON["LastEarthquake"]= "N/A" 
        ASJSON["EQCount"] = "N/A"
         


    query = "SELECT timestamp, deviceid, instanteq_si, keepalivemessage from AS433MHZ WHERE (timestamp > '%s') and (keepalivemessage=0) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1" % (before, WSLGHTID)
    cur.execute(query)
    #print("queryD=", query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["LastEQSI"] = str(records[0][2]) + " m/s"
    else:
        ASJSON["LastEQSI"]= "N/A"


    query = "SELECT timestamp, deviceid, instanteq_pga, keepalivemessage from AS433MHZ WHERE (timestamp > '%s') and (keepalivemessage=0) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1" % (before, WSLGHTID)
    cur.execute(query)
    #print("queryD=", query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["LastEQPGA"] = str(records[0][2]) + " m/s**2"
    else:
        ASJSON["LastEQPGA"]= "N/A"


    query = "SELECT timestamp, deviceid, instanteq_pga, keepalivemessage from AS433MHZ WHERE (timestamp > '%s') and (keepalivemessage=0) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1" % (before, WSLGHTID)
    cur.execute(query)
    #print("queryD=", query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["InstantEQPGA"] = str(records[0][2]) + " m/s**2"
    else:
        ASJSON["LastEQPGA"]= "N/A"

    query = "SELECT timestamp, deviceid, instanteq_si, keepalivemessage from AS433MHZ WHERE (timestamp > '%s') and (keepalivemessage=0) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1" % (before, WSLGHTID)
    cur.execute(query)
    #print("queryD=", query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["InstantEQSI"] = str(records[0][2]) + " m/s"
    else:
        ASJSON["InstantEQSI"]= "N/A"





    query = "SELECT timestamp, deviceid from AS433MHZ WHERE deviceid = %d ORDER BY timestamp DESC LIMIT 1" % WSLGHTID
    cur.execute(query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["UnitID"] = str(records[0][1])
    else:
        ASJSON["UnitID"]= "N/A"


    query = "SELECT timestamp, messageID, deviceid from AS433MHZ WHERE deviceid = %d ORDER BY timestamp DESC LIMIT 1"  % WSLGHTID
    cur.execute(query)
    records = cur.fetchall()
    if (len(records) > 0):
        ASJSON["LastMessageID"] = "ID: "+str(records[0][1]) + " Timestamp: " + records[0][0].strftime('%Y-%m-%d %H:%M:%S')
    else:
        ASJSON["LastMessageID"]= "N/A"


def build_graphAfterShock_figure():
    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )



    #last 14 days
    timeDelta = datetime.timedelta(days=14)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp,deviceid, eqcount, instanteq_si, instanteq_pga, keepalivemessage FROM AS433MHZ WHERE (timestamp > '%s') AND (keepalivemessage = 0) AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID) 
    #print("Query=", query)
    df = pd.read_sql(query, con )
    df['present'] = pd.Series([0 for x in range(len(df.index))]) 

    query = "SELECT timestamp, deviceid, eqcount, keepalivemessage FROM AS433MHZ WHERE (timestamp > '%s') AND (keepalivemessage = 1) AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID) 
    df2 = pd.read_sql(query, con )
    df2['present'] = pd.Series([0 for x in range(len(df2.index))]) 

    trace1 = go.Scatter(x=df.timestamp, y=df.instanteq_si, name='AfterShock SI Strength', mode="markers", marker=dict(size=10, color="blue"))
    trace2 = go.Scatter(x=df.timestamp, y=df.present, name='AfterShock Quake', mode="markers", marker=dict(size=20, color = "red" ))

    trace3 = go.Scatter(x=df2.timestamp, y=df2.present, name='KeepAlive', mode="markers", marker=dict(size=15, color = "black" ))

    figure={
    'data': [trace1, trace2, trace3 ],
    'layout':
    go.Layout(title='WeatherSense AfterShock', xaxis_title="Updated at: "+nowTime, yaxis_title="Earthquake Strength (SI)") }
    con.close()

    return figure

def build_graph1_figure():
    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )

    #last 14 days
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp, deviceid, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM AS433MHZ WHERE (timestamp > '%s') AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID) 
    #print("query=", query)
    df = pd.read_sql(query, con )


    trace1 = go.Scatter(x=df.timestamp, y=df.batteryvoltage, name='battery voltage')
    trace2 = go.Scatter(x=df.timestamp, y=df.solarvoltage, name='solar voltage')
    trace3 = go.Scatter(x=df.timestamp, y=df.loadvoltage, name='load voltage')
    trace4 = go.Scatter(x=df.timestamp, y=df.auxa, name='Aux State')

    figure={
    'data': [trace1, trace2, trace3, trace4],
    'layout':
    go.Layout(title='WeatherSense AfterShock Solar Voltages', xaxis_title="Updated at: "+nowTime, yaxis_title="Voltage (V)") }
    con.close()

    return figure

def build_graph2_figure():
    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )

    #last 14 days
    timeDelta = datetime.timedelta(days=14)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa, deviceid FROM AS433MHZ WHERE (timestamp > '%s') AND (deviceid = %d) ORDER BY timestamp"% (before,WSLGHTID) 
    df = pd.read_sql(query, con )
    trace1c = go.Scatter(x=df.timestamp, y=df.batterycurrent, name='battery current')
    trace2c = go.Scatter(x=df.timestamp, y=df.solarcurrent, name='solar current')
    trace3c = go.Scatter(x=df.timestamp, y=df.loadcurrent, name='load current')
    figure={
    'data': [trace1c, trace2c, trace3c],
    'layout':
    go.Layout(title='WeatherSense AfterShock Solar Currents', xaxis_title="Updated at: "+nowTime, yaxis_title="Current (mA)") }

    con.close()

    return figure


def AfterShockPage():

    maintextsize = "2.0em"
    subtextcolor = "green"
    maintextcolor = "black"

    Row1 = html.Div(
        [
        #dbc.Row( dbc.Col(html.Div(id="Weather Instruments"))),
        dbc.Row( dbc.Col(html.Div(html.H6(id={'type' : 'ASdynamic', 'index': "StringTime"},children="Weather Instruments")))),

            dbc.Row(
                [ 
                    dbc.Col(html.Div(
                     [

                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "LastEarthquake"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Earthquake Detection", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "LastEQSI"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Earthquake Seismic Intensity (m/s)", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "LastEQPGA"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Earthquake Peak Acceleration Value (m/s^2)", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "EQCount"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Earthquake Count", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "InstantEQSI"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Instantaneous Seismic Intensity (m/s)", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "InstantEQPGA"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Instantaneous Peak Acceleration Value (m/s^2)", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "UnitID"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Unit ID", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'ASdynamic', 'index' : "LastMessageID"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Message ID", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                    ],
                    ),
                    ),
            ],
            ),

            ],
            )
    Row2 = html.Div()
    Row3 = html.Div()

    layout = html.Div(children=[

    html.H1("AfterShock Charts (Last 14 Days)", style={'textAlign': 'center'}),

    dbc.Container([
        Row1, Row2, Row3 ],
        className="p-5",
        ),

   
    dcc.Graph(
    id={'type' : 'AfterShockgraph', 'index' : "1"},
    figure = build_graphAfterShock_figure(),
    ),

    dcc.Graph(
    id={'type' : 'AfterShockgraph', 'index' : "2"},
    figure = build_graph1_figure(),
    ),

    dcc.Graph(
    id={'type' : 'AfterShockgraph', 'index' : "3"},
    figure = build_graph2_figure(),
    ) ,

    ], className="container" )

    return layout
