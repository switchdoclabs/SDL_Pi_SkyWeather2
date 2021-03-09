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


GREEN = "#2bff00"

################
# Status Page
################

################
# Page Functions
################

def getWR2Status():
   
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SkyWeather2');
                cur = con.cursor()
                now = datetime.datetime.now()
                timeDelta = datetime.timedelta(minutes=30)


                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT BatteryOK FROM WeatherData WHERE TimeStamp > '%s' ORDER BY TimeStamp DESC LIMIT 1" % (before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                if (len(records) == 0):
                    return "gray"
                    
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        if (records[0][0] == "OK"):
            return GREEN
        else:

            return "red"

def getWSAQIStatus():
   
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'WeatherSenseWireless');
                cur = con.cursor()
                now = datetime.datetime.now()
                timeDelta = datetime.timedelta(minutes=60)


                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT batteryvoltage FROM AQI433MHZ WHERE timestamp > '%s' ORDER BY timestamp DESC LIMIT 1" % (before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                if (len(records) == 0):
                    return "gray"
                    
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        if (float(records[0][0]) > 2.9):
            return GREEN
        else:

            return "red"

def getWSLightningStatus():
   
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'WeatherSenseWireless');
                cur = con.cursor()
                now = datetime.datetime.now()
                timeDelta = datetime.timedelta(minutes=60)


                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT batteryvoltage FROM TB433MHZ WHERE timestamp > '%s' ORDER BY timestamp DESC LIMIT 1" % (before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                if (len(records) == 0):
                    return "gray"
                    
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        if (float(records[0][0]) > 2.9):
            return GREEN
        else:

            return "red"

def getWSSolarMAXStatus():
   
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'WeatherSenseWireless');
                cur = con.cursor()
                now = datetime.datetime.now()
                timeDelta = datetime.timedelta(minutes=60)


                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT batteryvoltage FROM SolarMax433MHZ WHERE timestamp > '%s' ORDER BY timestamp DESC LIMIT 1" % (before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                if (len(records) == 0):
                    return "gray"
                    
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        if (float(records[0][0]) > 11.2):
            return GREEN
        else:

            return "red"

def getIndoorStatus(channel):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SkyWeather2');
                cur = con.cursor()
                now = datetime.datetime.now()
                timeDelta = datetime.timedelta(minutes=30)


                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT BatteryOK FROM IndoorTHSensors WHERE (TimeStamp > '%s' AND ChannelID = %d) ORDER BY TimeStamp DESC LIMIT 1" % (before, channel)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                if (len(records) == 0):
                    return "gray"
                    
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()
        if (records[0][0] == "OK"):
            return GREEN
        else:

            return "red"


def returnOutdoorIndicator():

     totalLayout = []
     myLabelLayout = [] 
     myIndicatorLayout = []
        
     myLabelLayout.append(
                    
                     html.H6("WeatherSense Battery Status (Green=Good, Red=Low, Gray=Off Air)" )
                     ,
		     )
     
     myColor = getWR2Status() 
     
     myIndicatorLayout.append( 
            daq.Indicator(
                        id = {'type' : 'SPdynamic', 'index': 0}  , 
                        color = myColor,
                        label="WeatherRack2",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )
   
     myColor = getWSAQIStatus() 
     myIndicatorLayout.append( 
            daq.Indicator(
                        id = {'type' : 'SPdynamic', 'index': 10}  , 
                        color = myColor,
                        label="WS Air Quality",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )
   
     myColor = getWSLightningStatus() 
     myIndicatorLayout.append( 
            daq.Indicator(
                        id = {'type' : 'SPdynamic', 'index': 11}  , 
                        color = myColor,
                        label="WS Lightning",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )
   
     myColor = getWSSolarMAXStatus() 
     myIndicatorLayout.append( 
            daq.Indicator(
                        id = {'type' : 'SPdynamic', 'index': 12}  , 
                        color = myColor,
                        label="WS SolarMAX2",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )
   
     totalLayout.append(dbc.Row( myLabelLayout))
     totalLayout.append(dbc.Row(myIndicatorLayout))

     return totalLayout




def returnIndoorIndicators():

     totalLayout = []
     myLabelLayout = [] 
     myIndicatorLayout = []
        
   
     myLabelLayout.append(
                 
                     html.H6("Indoor Sensor Battery Channels" )
                     ,
		     )
     

     for IndoorSensor in range(1,9):


            myColor = getIndoorStatus(IndoorSensor)
            
            myIndicatorLayout.append( daq.Indicator(
                        id = {'type' : 'SPdynamic', 'index': IndoorSensor}  , 
                        color = myColor,
                        label="Channel "+str(IndoorSensor),
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )
            
     totalLayout.append(dbc.Row( myLabelLayout))
     totalLayout.append(dbc.Row(myIndicatorLayout))

     return totalLayout


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
    OutdoorIndicator = returnOutdoorIndicator()
    IndoorIndicators = returnIndoorIndicators()
   
    Row6 = html.Div(
        OutdoorIndicator, 
    )
    Row7 = html.Div(
        IndoorIndicators,
    )
    #layout = dbc.Container([
    layout = dbc.Container([
        Row1, Row2, Row5, Row3, Row4, Row6, Row7],
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
        #print("myDPercent=", myDPercent)
        myDPercent = 100.0 - myDPercent
        return myDPercent 

		
    # update CPU Loading
    if (id['GaugeType'] == "pi-loading"):
        myValue = psutil.cpu_percent()
        return myValue


    # update Pi Memory usage
    if (id['GaugeType'] == "pi-memory"):
    	myValue = psutil.virtual_memory().percent
    	return myValue

def updateIndicators(id):    # update indicators

    color = "gray"
    if (id['index'] == 0):
        color = getWR2Status()
    if (id['index'] == 10):
        color = getWSAQIStatus()
    if (id['index'] == 11):
        color = getWSLightningStatus()
    if (id['index'] == 12):
        color = getWSSolarMAXStatus()
    if ((id['index'] > 0) and (id['index'] < 10)):
        color = getIndoorStatus(id['index'])
    return color

        


