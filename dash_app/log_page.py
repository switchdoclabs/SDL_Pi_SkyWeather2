

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



################
# Log Page
################
def buildTableFig(data, title):
    if (title=="System Log"):
        fig = go.Figure(data=[
		go.Table(
                   header = dict(
                     values = [['<b>TimeStamp</b>'], ['<b>Level</b>'],
                                   ['<b>Description</b>']],
                     line_color='darkslategray',
                     fill_color='royalblue',
                     align=['left','center'],
                     font=dict(color='white', size=12),
                     height=40
                   ),
                   cells=dict(
                     values=data,
                     line_color='darkslategray',
                     fill=dict(color=['paleturquoise', 'white']),
                     align=['left', 'center'],
                     font_size=12,
                     height=30),
                     ) 
		 ],
		 layout= {"title" : title, "autosize" : True},
                     )
        return fig
	
    if (title=="Valve Log"):
        fig = go.Figure(data=[
		go.Table(
                   header = dict(
                     values = [
		                   ['<b>TimeStamp</b>'], 
		                   ['<b>DeviceID</b>'],
                                   ['<b>Valve Number</b>'],
                                   ['<b>State</b>'],
                                   ['<b>Source</b>'],
                                   ['<b>Seconds On</b>'],
                                   ['<b>Valve Type</b>'],
				   ],
                     line_color='darkslategray',
                     fill_color='royalblue',
                     align=['left','center'],
                     font=dict(color='white', size=12),
                     height=40
                   ),
                   cells=dict(
                     values=data,
                     line_color='darkslategray',
                     fill=dict(color=['paleturquoise', 'white']),
                     align=['left', 'center'],
                     font_size=12,
                     height=30),
                     ) 
		 ],
		 layout= {"title" : title, "autosize" : True},
                     )
        return fig
    
    if (title=="Sensor Log"):
        fig = go.Figure(data=[
		go.Table(
                   header = dict(
                     values = [
		                   ['<b>TimeStamp</b>'], 
				   ['<b>DeviceID</b>'],
                                   ['<b>Sensor Number</b>'],
                                   ['<b>Sensor Value</b>'],
                                   ['<b>Sesnor Type On</b>'],
                                   ['<b>TimeStamp Type</b>'],
				   ],
                     line_color='darkslategray',
                     fill_color='royalblue',
                     align=['left','center'],
                     font=dict(color='white', size=12),
                     height=40
                   ),
                   cells=dict(
                     values=data,
                     line_color='darkslategray',
                     fill=dict(color=['paleturquoise', 'white']),
                     align=['left', 'center'],
                     font_size=12,
                     height=30),
                     ) 
		 ],
		 layout= {"title" : title, "autosize" : True},
                     )

        return fig
	
    fig = html.H1(children="Error in print system log")

def convertLevelToName(level):

       if (level == 50):
       	return "CRITICAL"
       
       if (level == 40):
       	return "ERROR"
       
       if (level == 30):
       	return "WARNING"
       
       if (level == 20):
       	return "INFO"

       if (level == 15):
       	return "JSON"
       
       if (level == 10):
       	return "DEBUG"
       
       if (level == 0):
       	return "NOTSET"

       return "UNKNOWN" 


def fetchSystemLog():

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "SELECT * FROM SystemLog ORDER BY ID DESC LIMIT 20" 
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()

                #print(records)
                Time = []
                Level = []
                Description = []

                for item in records:
                   Time.append(item[3])
                   myLevel = convertLevelToName(item[1])
                   Level.append(myLevel)
                   if (myLevel == "JSON"):
                   	Description.append("{JSON code}")
                   else:
                        Description.append(item[2])
                return Time, Level, Description
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

def fetchValveLog():

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "SELECT * FROM ValveChanges ORDER BY ID DESC LIMIT 20" 
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()

                Time = []
                DeviceID = []
                ValveNumber = []
                State = []
                Sources = []
                SecondsOn = []
                ValveType = []

                for item in records:
                     Time.append(item[7])
                     DeviceID.append(item[1])
                     ValveNumber.append(item[2])
                     State.append(item[3])
                     Sources.append(item[4])
                     SecondsOn.append(item[6])
                     ValveType.append(item[5])
                
                return Time, DeviceID, ValveNumber, State, Sources, SecondsOn, ValveType 
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

def fetchSensorLog():

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "SELECT * FROM Sensors ORDER BY ID DESC LIMIT 20" 
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()

                Time = []
                DeviceID = []
                SensorNumber = []
                SensorValue = []
                SensorType = []
                TimeRead = []

                for item in records:
                     Time.append(item[6])
                     DeviceID.append(item[1])
                     SensorNumber.append(item[2])
                     SensorValue.append(item[3])
                     SensorType.append(item[4])
                     TimeRead.append(item[5])
                
                return Time, DeviceID,  SensorNumber, SensorValue, SensorType, TimeRead 
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()






def updateLogs(): 
      layout = [] 

      data = fetchSystemLog()
      fig = buildTableFig(data,"System Log")
      layout.append(dcc.Graph(id={"type": "LPdynamic", "index": "systemlog"},figure=fig))	

      data = fetchValveLog()
      fig = buildTableFig(data,"Valve Log")
      layout.append(dcc.Graph(id={"type": "LPdynamic", "index": "sensorlog"},figure=fig))	

      data = fetchSensorLog()
      fig = buildTableFig(data,"Sensor Log")
      layout.append(dcc.Graph(id={"type": "LPdynamic", "index": "valvelog"},figure=fig))	


      return layout

################
# Page Functions
################


def LogPage():
    Row1 = html.Div(
        [ 
            #dbc.Row(
                #[
			html.Div(updateLogs())
                #]
            #),
        ]
    )
    #layout = dbc.Container([
    layout = dbc.Container([
        Row1],
        className="p-5",
    )
    return layout







