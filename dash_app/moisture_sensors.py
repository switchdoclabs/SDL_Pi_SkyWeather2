
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


from navbar import Navbar, Logo

# Moisture Graphs
################

def findDriestSensor(timeDelta):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT SensorValue, TimeRead FROM `Sensors` WHERE DeviceID = '%s' AND SensorNumber = %s AND (TimeStamp > '%s') ORDER BY id" % (myID, MSNumber, before)
                query = "SELECT SensorValue, TimeRead FROM `Sensors` WHERE DeviceID = '%s' AND SensorNumber = %s AND (TimeStamp > '%s') ORDER BY id" % (myID, MSNumber, before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                return records
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()


def returnLatestGraphSensorValues(myID, MSNumber, timeDelta):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT SensorValue, TimeRead FROM `Sensors` WHERE DeviceID = '%s' AND SensorNumber = %s AND (TimeStamp > '%s') ORDER BY id" % (myID, MSNumber, before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                return records
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()


def P1mydisplay_valve_graphs(myModCount):
    graphs = []
    
    myValves = config.SGSConfigurationJSON["Valves"]
    columnCount = 0
    for single in myValves:
        myValveNumber = single["ValveNumber"]
        if (single["ShowGraph"] == True):
            myControl = single["Control"]
            if (myControl[0:2] == "MS"):   # found Moisture sensor
                columnCount = columnCount +1
                mySplit = myControl.split("/")

                MSNumber = mySplit[0][3:]
                myName = mySplit[1]
                myID = mySplit[2]
                timeDelta = datetime.timedelta(days = 5)
                myValues = returnLatestGraphSensorValues(myID, MSNumber, timeDelta)
                #print ("myValue=", myValue) 
                Y = []
                Time = []
                for record in myValues:
                    Y.append(record[0])
                    Time.append(record[1])


                fig = go.Figure(
                            data=[go.Scatter(x=Time, y=Y)], layout=go.Layout(
                                   title = go.layout.Title( text = myName +"/"+ str(myID)+"/"+ str(myValveNumber)),
                                   yaxis= go.layout.YAxis( range = (0,101)),
                                   height= 300),
                                   )
                    
                graphs.append( dcc.Graph(
                    id = {'type' : 'MSGdynamic', 'index': myModCount, 'DeviceID' : myID, 'MSNumber': MSNumber, 'DeviceName': myName, 'ValveNumber': myValveNumber},
                    figure=fig,
                    animate = True
                    ))
                myModCount = myModCount + 1 

    
    return (myModCount, html.Div(graphs,style={'margin' : '10px'}))



###############
# Tanks
################


con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
cur = con.cursor()

def getNameFromID(myID):
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for singleWireless in wirelessJSON:
            if (str(myID).replace(" ","")  == str(singleWireless["id"]).replace(" ","")):
                return singleWireless["name"]

        

def returnLatestSensorValue(myID, MSNumber):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "SELECT * FROM `Sensors` WHERE DeviceID = '%s' AND SensorNumber = %s ORDER BY id DESC LIMIT 1" % (myID, MSNumber)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("records=", records)
                return (records[0][3])
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()
def returnTimeString():
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    return html.Div([html.H6(children="updated: "+nowString), html.Br()])
    
def P1mydisplay_valve_tanks(myModCount):
    tanks = []

    myValves = config.SGSConfigurationJSON["Valves"]
    
    columnCount = 0
    for single in myValves:
        myValveNumber = single["ValveNumber"]
        if (single["ShowGraph"] == True):
            myControl = single["Control"]
            if (myControl[0:2] == "MS"):   # found Moisture sensor
                columnCount = columnCount +1
                mySplit = myControl.split("/")

                MSNumber = mySplit[0][3:]
                myName = mySplit[1]
                myID = mySplit[2]
            
                myValue =returnLatestSensorValue(myID, MSNumber)
                #print ("myValue=", myValue) 
                tanks.append(daq.Tank(
                    min=0,
                    max=100,
                    value=myValue,
                    showCurrentValue=True,
                    units="percent",
                    #style={'marginLeft': '70px', 'marginBottom' : '10px', 'fontFamily': 'Arial'},

                    style = { 'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gridTemplateRows': '1fr', 'gridColumnGap': '0px', 'gridRowGap': '0px' },

                    label=myName +"/"+ str(myID)+"/"+ str(myValveNumber),
                    labelPosition='bottom',
                    id = {'type' : 'MSTdynamic', 'index': myModCount, 'DeviceID' : myID, 'MSNumber': MSNumber},
                    className='dark-theme-control',)
                    )
                myModCount = myModCount +1

                #print("columnCount=",columnCount)
    
    return (myModCount, html.Div(tanks,style={'margin' : '10px','columnCount': columnCount}))

def returnNumberTanksGraphs():
    return 10

def updateGraphs():
    myModCount = 0    
    returnValue = P1mydisplay_valve_tanks(myModCount)
    P1Tanks = returnValue[1]
    myModCount = returnValue[0]
    returnValue = P1mydisplay_valve_graphs(myModCount)
    P1Graphs = returnValue[1]
    myModCount = returnValue[0]

    P1tankLayout = html.Div(
        [
        returnTimeString(),
        #P1Tanks,
        P1Graphs
    
    ],
        id="current-page",
    )
    return P1tankLayout

####
# Callback functions
####
def updateTank(id):

    #print ("Updating Tank: {}".format(id))
    myValue = returnLatestSensorValue(id["DeviceID"], id["MSNumber"])
    #print("New Value =%f / ID %s" % (myValue, id["DeviceID"]))
    
    return myValue

def updateGraph(id):

    #print ("Updating Graph: {}".format(id))
    timeDelta = datetime.timedelta(days = 5)
    records= returnLatestGraphSensorValues(id["DeviceID"], id["MSNumber"], timeDelta)
    #print ("records=", records)
    print("Record Count =%d / ID %s" % (len(records), id["DeviceID"]))
    Y = []
    Time = []
    for record in records:
          Y.append(record[0])
          Time.append(record[1])
    return (Time, Y)



################
# Page Functions
################

def MoistureSensorPage():
    P1tankLayout = updateGraphs()
    #nav = Navbar()
    #logo = Logo()
    ################

    Row1 = html.Div(
        [ 
            dbc.Row(
                [
                    dbc.Col(html.Div(P1tankLayout))
                ],
            ),
        
       
 
            ])

    #layout = dbc.Container([
    #layout = dbc.Container(
    #        [
    #    Row1],
    #    className="p-5",
    #    id='moisturesensorpage',
    #)
    return Row1







