# import os
import sys
# import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import MySQLdb as mdb
import datetime

import readJSON
import json



# read JSON

readJSON.readJSON("../")

import plotly.graph_objs as go
# from dash.dependencies import Input, Output, MATCH, ALL, State

sys.path.append("../")

import config
WSLGHTID = 1

LLJSON={}
LLJSON["LastLightning"]= "N/A"
LLJSON["LastLightningDistance"]= "N/A"
LLJSON["LightningCount"]= "N/A"
LLJSON["TotalLightningCount"]= "N/A"
LLJSON["DisturberCount"]= "N/A"
LLJSON["NoiseCount"]= "N/A"
LLJSON["UnitID"]= "N/A"
LLJSON["LastMessageID"]= "N/A"

def updateLightningLines():

    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )

    cur = con.cursor()
    # build the data array

    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    
    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')

    query = "SELECT timestamp, lightningcount, deviceid from TB433MHZ WHERE (irqsource = 8) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1 " % WSLGHTID
    print("queryA=", query)
    cur.execute(query)
    records = cur.fetchall()
    if (len(records) > 0):
        LLJSON["LastLightning"] = records[0][0].strftime("%d-%b-%Y %H:%M:%S")
    else:
        LLJSON["LastLightning"]= "N/A" 
         


    query = "SELECT timestamp, deviceid, lightninglastdistance, irqsource from TB433MHZ WHERE (timestamp > '%s') and (irqsource=8) AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1" % (before, WSLGHTID)
    cur.execute(query)
    print("queryD=", query)
    records = cur.fetchall()
    if (len(records) > 0):
        English_Metric = readJSON.getJSONValue("English_Metric")
        if (English_Metric == False):
            LLJSON["LastLightningDistance"] = str(records[0][2]*0.6214) + "miles"
        else:
            LLJSON["LastLightningDistance"] = str(records[0][2]) + "km"
    else:
        LLJSON["LastLightningDistance"]= "N/A"




    query = "SELECT timestamp, deviceid, lightningcount from TB433MHZ WHERE (timestamp > '%s') AND (irqsource = 8) and (deviceid = %d)" % (before, WSLGHTID)
    cur.execute(query)
    records = cur.fetchall()
         
    LLJSON["LightningCount"]= str(len(records)) 



    query = "SELECT timestamp, deviceid, lightningcount from TB433MHZ WHERE (timestamp > '%s') AND (deviceid = %d) ORDER BY timestamp DESC LIMIT 1" % (before, WSLGHTID)
    cur.execute(query)
    records = cur.fetchall()

         
    if (len(records) > 0):
            LLJSON["TotalLightningCount"]= str(records[0][2])
    else: 
            LLJSON["TotalLightningCount"]= "N/A" 



    query = "SELECT timestamp, irqsource from TB433MHZ WHERE (timestamp > '%s') AND  (irqsource = 4)" % before
    cur.execute(query)
    records = cur.fetchall()
    count = len(records)
    LLJSON["DisturberCount"] = str(count)


    query = "SELECT timestamp, irqsource, deviceid from TB433MHZ WHERE (timestamp > '%s') AND (irqsource = 1) AND deviceid = %d" % (before, WSLGHTID)
    cur.execute(query)
    records = cur.fetchall()
    count = len(records)
    LLJSON["NoiseCount"] = str(count)

    query = "SELECT timestamp, deviceid from TB433MHZ WHERE deviceid = %d ORDER BY timestamp DESC LIMIT 1" % WSLGHTID
    cur.execute(query)
    records = cur.fetchall()
    if (len(records) > 0):
        LLJSON["UnitID"] = str(records[0][1])
    else:
        LLJSON["UnitID"]= "N/A"


    query = "SELECT timestamp, messageID, deviceid from TB433MHZ WHERE deviceid = %d ORDER BY timestamp DESC LIMIT 1"  % WSLGHTID
    cur.execute(query)
    records = cur.fetchall()
    if (len(records) > 0):
        LLJSON["LastMessageID"] = "ID: "+str(records[0][1]) + " Timestamp: " + records[0][0].strftime("%d-%b-%Y %H:%M:%S")
    else:
        LLJSON["LastMessageID"]= "N/A"


def build_graphLightning_figure():
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
    
    query = "SELECT timestamp,deviceid, interruptcount, lightningcount, irqsource, lightninglastdistance  FROM TB433MHZ WHERE (TimeStamp > '%s') AND (irqsource = 8) AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID) 
    df = pd.read_sql(query, con )
    df['present'] = pd.Series([0 for x in range(len(df.index))]) 

    query = "SELECT timestamp, deviceid, interruptcount, lightningcount, irqsource, lightninglastdistance  FROM TB433MHZ WHERE (TimeStamp > '%s') AND (irqsource = 4) AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID) 
    df2 = pd.read_sql(query, con )
    df2['present'] = pd.Series([0 for x in range(len(df2.index))]) 

    query = "SELECT timestamp, deviceid, interruptcount, lightningcount, irqsource, lightninglastdistance  FROM TB433MHZ WHERE (TimeStamp > '%s') AND (irqsource = 0) AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID)
    df3 = pd.read_sql(query, con )
    df3['present'] = pd.Series([0 for x in range(len(df3.index))])
    
    English_Metric = readJSON.getJSONValue("English_Metric")
    if (English_Metric == False):
        trace1 = go.Scatter(x=df.timestamp, y=df.lightninglastdistance*0.6214, name='Lightning Distance', mode="markers", marker=dict(size=10, color="blue"))
       
    else:
        trace1 = go.Scatter(x=df.timestamp, y=df.lightninglastdistance, name='Lightning Distance', mode="markers", marker=dict(size=10, color="blue"))

    trace1 = go.Scatter(x=df.timestamp, y=df.lightninglastdistance, name='Lightning Distance', mode="markers", marker=dict(size=10, color="blue"))

    trace2 = go.Scatter(x=df.timestamp, y=df.present, name='Lightning Stroke', mode="markers", marker=dict(size=15, color = "red" ))

    trace3 = go.Scatter(x=df2.timestamp, y=df2.present, name='Disruptor', mode="markers", marker=dict(size=15, color = "orange" ), showlegend=True)

    trace4 = go.Scatter(x=df3.timestamp, y=df3.present, name='KeepAlive', mode="markers", marker=dict(size=10, color = "black" ))
    
    if (English_Metric == False):
       myTitle =  "Lightning Distance (miles)"
    else:
       myTitle =  "Lightning Distance (km)"


    figure={
    'data': [trace1, trace2, trace3, trace4 ],
    'layout':
    go.Layout(title='WeatherSense Lightning', xaxis_title="Updated at: "+nowTime,
        yaxis_range=[0,30],
        showlegend= True,
        yaxis_title=myTitle
 
    
    ) }
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
    
    query = "SELECT timestamp, deviceid, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM TB433MHZ WHERE (TimeStamp > '%s') AND (deviceid = %d) ORDER BY timestamp"% (before, WSLGHTID) 
    #print("query=", query)
    df = pd.read_sql(query, con )


    trace1 = go.Scatter(x=df.timestamp, y=df.batteryvoltage, name='battery voltage')
    trace2 = go.Scatter(x=df.timestamp, y=df.solarvoltage, name='solar voltage')
    trace3 = go.Scatter(x=df.timestamp, y=df.loadvoltage, name='load voltage')
    trace4 = go.Scatter(x=df.timestamp, y=df.auxa, name='Aux State')

    figure={
    'data': [trace1, trace2, trace3, trace4],
    'layout':
    go.Layout(title='WeatherSense Lightning Solar Voltages', xaxis_title="Updated at: "+nowTime, yaxis_title="Voltage (V)") }
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
    
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa, deviceid FROM TB433MHZ WHERE (TimeStamp > '%s') AND (deviceid = %d) ORDER BY timestamp"% (before,WSLGHTID) 
    df = pd.read_sql(query, con )
    trace1c = go.Scatter(x=df.timestamp, y=df.batterycurrent, name='battery current')
    trace2c = go.Scatter(x=df.timestamp, y=df.solarcurrent, name='solar current')
    trace3c = go.Scatter(x=df.timestamp, y=df.loadcurrent, name='load current')
    figure={
    'data': [trace1c, trace2c, trace3c],
    'layout':
    go.Layout(title='WeatherSense Lightning Solar Currents', xaxis_title="Updated at: "+nowTime , yaxis_title="Current (mA)") }

    con.close()

    return figure


def LightningPage():

    maintextsize = "2.0em"
    subtextcolor = "green"
    maintextcolor = "black"

    Row1 = html.Div(
        [
        #dbc.Row( dbc.Col(html.Div(id="Weather Instruments"))),
        dbc.Row( dbc.Col(html.Div(html.H6(id={'type' : 'LPdynamic', 'index': "StringTime"},children="Weather Instruments")))),

            dbc.Row(
                [ 
                    dbc.Col(html.Div(
                     [

                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "LastLightning"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Lightning Detection", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "LastLightningDistance"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Last Lightning Distance", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "LightningCount"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Lightning Count", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "TotalLightningCount"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Total Lightning Count Since Reboot", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "DisturberCount"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Disturber Count", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "NoiseCount"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Noise Count", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "UnitID"},
                            children=str("N/A"), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Unit ID", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'LPdynamic', 'index' : "LastMessageID"},
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

    html.H1("Lightning Charts (Last 7 Days)", style={'textAlign': 'center'}),

    dbc.Container([
        Row1, Row2, Row3 ],
        className="p-5",
        ),

   
    dcc.Graph(
    id={'type' : 'Lightninggraph', 'index' : "1"},
    figure = build_graphLightning_figure(),
    ),

    dcc.Graph(
    id={'type' : 'Lightninggraph', 'index' : "2"},
    figure = build_graph1_figure(),
    ),

    dcc.Graph(
    id={'type' : 'Lightninggraph', 'index' : "3"},
    figure = build_graph2_figure(),
    ) ,

    ], className="container" )

    return layout
