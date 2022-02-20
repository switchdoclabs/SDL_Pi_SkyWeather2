import os, sys, glob
# import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


import pandas as pd
import MySQLdb as mdb
import datetime
import time


import plotly.graph_objs as go
# from dash.dependencies import Input, Output, MATCH, ALL, State

os.makedirs("static/SkyCam", exist_ok=True)


# build the path to import config.py from the parent directory
sys.path.append('../')
import config

# how long before you ignore the camera information
IGNOREAFTERDAYS = 7

def build_picture_figure(cameraID):

    return "../static/CurrentPicture/"+cameraID+".jpg"



def build_graph1_figure(cameraID):
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
    
    query = "SELECT timestamp, cameraID, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent FROM SkyCamSensors WHERE (TimeStamp > '%s') AND (cameraID = '%s') ORDER BY timestamp"% (before,cameraID) 
    # print("query=", query)
    df = pd.read_sql(query, con )


    trace1 = go.Scatter(x=df.timestamp, y=df.batteryvoltage, name='battery voltage')
    trace2 = go.Scatter(x=df.timestamp, y=df.solarvoltage, name='solar voltage')
    trace3 = go.Scatter(x=df.timestamp, y=df.loadvoltage, name='load voltage')

    figure={
    'data': [trace1, trace2, trace3 ],
    'layout':
    go.Layout(title='SkyCamera '+cameraID+' Solar Voltages', xaxis_title="Updated at: "+nowTime, yaxis_title="Voltage (V)") }
    con.close()

    return figure


def build_graph2_figure(cameraID):
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
    
    query = "SELECT timestamp, cameraID, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent FROM SkyCamSensors WHERE (TimeStamp > '%s') AND (cameraID = '%s') ORDER BY timestamp"% (before, cameraID) 
    df = pd.read_sql(query, con )
    trace1c = go.Scatter(x=df.timestamp, y=df.batterycurrent, name='battery current')
    trace2c = go.Scatter(x=df.timestamp, y=df.solarcurrent, name='solar current')
    trace3c = go.Scatter(x=df.timestamp, y=df.loadcurrent, name='load current')
    figure={
    'data': [trace1c, trace2c, trace3c],
    'layout':
    go.Layout(title='SkyCamera '+cameraID+'  Solar Currents', xaxis_title="Updated at: "+nowTime, yaxis_title="Current (mA)") }

    con.close()

    return figure

def getSkyCamList():

    dir_path = '../static/SkyCam/'
    devices = os.listdir(dir_path)
    devices = sorted(devices)
    timeDelta = datetime.timedelta(days= IGNOREAFTERDAYS )
    now = datetime.datetime.now()
    before = now - timeDelta
    #before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    newdevices = []
    for device in devices:
        lastMod= time.ctime(max(os.path.getmtime(root) for root,_,_ in os.walk(dir_path+device)))
        lastMod = datetime.datetime.strptime(lastMod, "%a %b %d %H:%M:%S %Y")
        #print ("last modified: %s" % lastMod) 
        if (lastMod > before):
            newdevices.append(device)

       
    #print(newdevices)
    return newdevices

def getTimeLapseList(cam):
    output = []
    try:
    
        dir_path = "../static/TimeLapses/"+cam
    
        myFiles = os.listdir(dir_path) 
        myFiles = [os.path.join(dir_path, f) for f in myFiles] # add path to each file
        #myFiles.sort(reverse=True)
        myFiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        #print(myFiles) 
        if (len(myFiles) > 14):
            myRange = range(0, 14)
        else:
            myRange = range(0,len(myFiles))
    
        #print(myRange)
        for i in myRange: 
            singleName = os.path.basename(myFiles[i])
            #output.append(html.P(singleName))
            output.append(dcc.Link(singleName, href="/static/TimeLapses/"+cam+"/"+singleName, target='blank'))
            output.append(html.Br())
        #print(output)
    except:
        pass 

    return output 


def buildPics(SkyCamList):

    output = []
    index = 0

    for cam in SkyCamList:
        output.append( html.H3("SkyCam "+cam))
        #output.append( html.Img( 
            #id={'type' : 'SkyCamPic', 'index' : index},
            #height=350, width=350*1.77, src="/assets/"+cam+".jpg"))
        picname = glob.glob("assets/"+cam+"*.jpg")
        #print("picname=", picname)
        output.append( 
            html.Div(        [
                dbc.Row(
                [
                    dbc.Col(html.Div(
                        html.Img( 
                            id={'type' : 'SkyCamPic', 'index' : index},
                            height=350, width=350*1.77, src="/"+picname[0]))
                        ),
                    dbc.Col(html.Div([html.H4("Time Lapses"),
                    html.Br(),
                    html.Div(children = getTimeLapseList(cam))
                        ]
                            )
                            ),
                ]
                  ),
              ]  )
              )
        index = index+1
    #print(output)    
    return output

def build_solar_graphs(SkyCamList):

    output = [html.Br(), html.Br()]
    index = 0
    for cam in SkyCamList:  
       
       output.append( html.H2("SkyCam "+cam + " Solar Charts"))
    
       output.append ( dcc.Graph(
        id={'type' : 'SkyCamGraph', 'index' : index},
        figure = build_graph1_figure(cam),
        ))
       index=index+1

       output.append( dcc.Graph(
        id={'type' : 'SkyCamGraph', 'index' : index},
         figure = build_graph2_figure(cam),
         ) )

       index=index+1

    return output

def SkyCamPage():

    SkyCamList = getSkyCamList()

    layout = html.Div(children=[

    html.H1("SkyCam Pictures/Charts", style={'textAlign': 'center'}),

    html.Div(id={'type' : 'SkyCamPics', 'index' :0}, children= buildPics(SkyCamList)),

    html.Div(id={'type' : 'SkyCamGraphs', 'index' : 0}, children = build_solar_graphs(SkyCamList)),

    ], className="container" )

    # con.close()
    return layout
