

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px 
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import datetime
import traceback
import sys

# SGS imports
sys.path.append("../")

import state
import config
import readJSON
import json



# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb



def CTUnits(temperature):

    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        temperature = (9.0/5.0 * temperature) +32.0
    return temperature

def TUnits():
    English_Metric = readJSON.getJSONValue("English_Metric")
    if (English_Metric == False):  # english units
        units = " F"
    else:
        units = " C"

    return units


################
# Build Graphs
################

def generateTHData(timeDelta):


        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT ChannelID, Temperature, Humidity, TimeStamp FROM `IndoorTHSensors` WHERE (TimeStamp > '%s') ORDER BY id ASC" % (before)
                print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                print ("Query Count = ", len(records)) 
                return records
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

def buildTemperatureGraph(data):

    # Create figure with secondary y-axis
    fig = go.Figure()
    if (len(data) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Indoor Temperature Data Available')
        return fig

    fig = make_subplots(specs=[[{"secondary_y": True}]])
  
    colors = ['red', 'blue', 'green', 'violet', 'brown',  'black', 'magenta', 'pink']
    minTemp = 1000
    maxTemp = -1000

    for i in range (1,9):
        Temperature = []
        Time = []
        
        for record in data:

            TRecord = CTUnits(record[1])
            if (record[0] == i):
                if (TRecord < minTemp):
                    minTemp = TRecord
                if (TRecord > maxTemp):
                    maxTemp = TRecord
                Time.append(record[3])
                Temperature.append(TRecord)
            
        print("minTemp=", minTemp)
        print("maxTemp=", maxTemp)

        print("len(Time)=", len(Time))
        if (len(Time) > 0):
            # Add traces
            fig.add_trace(
                go.Scatter(x=Time, y=Temperature, name="CHAN "+str(i),
                line = dict(
                    color = (colors[i-1]),
                    width = 2,
                    ),
                ),
                    secondary_y = False,
            )

    # Add figure title
    fig.update_layout(
        title_text="Indoor Temperature", height=400
    )

    units = TUnits() 
    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    minTemp = minTemp*0.9
    maxTemp = maxTemp*1.10

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Temperature ("+units+")</b>", range = (minTemp, maxTemp), secondary_y=False, side='left')
    #fig.update_yaxes(title_text="<b>Humidity (%)</b>", range = (0,100), secondary_y=True, side='right')

    return fig

def buildHumidityGraph(data):

    # Create figure with secondary y-axis
    fig = go.Figure()
    if (len(data) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Indoor Humidity Data Available')
        return fig

    fig = make_subplots(specs=[[{"secondary_y": True}]])
  
    colors = ['red', 'blue', 'green', 'violet', 'brown',  'black', 'magenta', 'pink']

    for i in range (1,9):
        Humidity = []
        Time = []
        
        for record in data:

            if (record[0] == i):
                Time.append(record[3])
                Humidity.append(record[2])
            

        print("len(Time)=", len(Time))
        if (len(Time) > 0):
            # Add traces
            fig.add_trace(
                go.Scatter(x=Time, y=Humidity, name="CHAN "+str(i),
                line = dict(
                    color = (colors[i-1]),
                    width = 2,
                    ),
                ),
                    secondary_y = False,
            )

    # Add figure title
    fig.update_layout(
        title_text="Indoor Humidity", height=400
    )

    units = "C"
    # Set x-axis title
    fig.update_xaxes(title_text="Time")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Humidity (%)</b>", range = (0,100), secondary_y=True, side='right')

    return fig

def buildTGraph():
    timeDelta = datetime.timedelta(days=7)
    data = generateTHData(timeDelta)
    
    fig1 = buildTemperatureGraph(data)

    graphT =  dcc.Graph(
                    id = {'type' : 'WPITHdynamic', 'index': 'temperature' },
                    figure=fig1,
                    animate = False
                    )
    graph = graphT

    return graph

def buildHGraph():
    timeDelta = datetime.timedelta(days=7)
    data = generateTHData(timeDelta)
    
    fig2 = buildHumidityGraph(data)

    graphH =  dcc.Graph(
                    id = {'type' : 'WPITHdynamic', 'index': 'humidity' },
                    figure=fig2,
                    animate = False
                    )
    graph = graphH

    return graph

################
# Page Functions
################


def IndoorTHPage():
    Row1 = html.Div(
        [ 
            dbc.Row(
                [
                    html.H3(children="Indoor Temperature and Humidity"),

                    dbc.Col(
                    [
                        buildTGraph(),
                        buildHGraph(),
                    ],
                    width = 12,
                    )
                ]
            ),
                ]
    )
    #layout = dbc.Container([
    layout = dbc.Container([
        Row1],
        className="p-5",
    )
    return layout







