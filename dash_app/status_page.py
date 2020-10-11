import random
import subprocess
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px 
import plotly.graph_objs as go

import datetime
import traceback
import sys
import psutil

# imports
sys.path.append("../")

import state
import config
import readJSON
import json

# demo mode
useRandom = False

# read JSON

readJSON.readJSON("../")

import MySQLdb as mdb



################
# Status Page
################

################
# Page Functions
################


def StatusPage():


    f = open("/proc/device-tree/model")
    piType = f.read()
    boottime =datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S") 
    
    Row1 = html.Div(
        [
                    dbc.Button(
                        ["Raspberry Pi", dbc.Badge(piType, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["SW2 Start Time ", dbc.Badge(boottime, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["Pi Boot Time ", dbc.Badge(boottime, color="light", className="ml-1")],
                        color="primary",),
        ])

    Row2 = dbc.Row(
                [
                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-loading'},
                        label="Pi CPU Loading",
                        value=0,
                        color={"gradient":True,"ranges":{"green":[0,50],"yellow":[50,85],"red":[85,100]}},
                        showCurrentValue=True,
                        units="%",
                        size=190,
                        max = 100,
                        min = 0,
                    ),
                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-memory'},
                        label="Pi Memory Usage",
                        value=0,
                        color={"gradient":True,"ranges":{"green":[0,50],"yellow":[50,85],"red":[85,100]}},
                        min = 0,
                        max=100,
                        size=190,
                        showCurrentValue=True,
                        units="%",

                    ),
                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-disk'},
                        label="Pi Disk Free",
                        value=0,
                        showCurrentValue=True,
                        units="%",
                        size=190,
                        color={"gradient":True,"ranges":{"red":[0,30],"yellow":[30,65],"green":[65,100]}},
                        max = 100,
                        min = 0,
                        ),


                ],
		no_gutters=True,

		)

    Row3 = html.Div(


         )

    Row4 = html.Div(
            [
    html.Div(id='log')
            ]
            )

    Row5 = html.Div(
                [
                    dbc.Alert("No Alarm", color="primary"),
        ],
		   style={'margin-top' : "-90px"}

    )
    #layout = dbc.Container([
    layout = dbc.Container([
        Row1, Row2, Row5, Row3, Row4],
        className="status-1",
    )
    return layout


####
# Callback functions
####

def updateGauges(id):
    myValue = 0
    #if (useRandom == True):
    #   myValue = random.randint(0,100)
    #   return myValue

    # update Lowest Percent Moisture Sensor
    if (id['GaugeType'] == "pi-disk"):
        #timeDelta = datetime.timedelta(days = 5)
        #myRecord = returnLowestSensorValue("C1", timeDelta)
        #print("driestValue=",myRecord)
        #return (myRecord[0][1],myRecord[0][2], myRecord[0][3],myRecord[0][5])
        myValue = psutil.disk_usage('/')
        myDPercent = myValue[3]
        print("myDPercent=", myDPercent)
        myDPercent = 100.0 - myDPercent
        print("myDPercent=", myDPercent)
        return myDPercent 

		
    # update CPU Loading
    if (id['GaugeType'] == "pi-loading"):
        myValue = psutil.cpu_percent()
        return myValue


    # update Pi Memory usage
    if (id['GaugeType'] == "pi-memory"):
    	myValue = psutil.virtual_memory().percent
    	return myValue



