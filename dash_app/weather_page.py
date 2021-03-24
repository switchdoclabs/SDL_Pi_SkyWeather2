
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

# imports
sys.path.append("../")

import state
import config
import readJSON
import json
import util


# read JSON

readJSON.readJSON("../")

import MySQLdb as mdb


################
# Weather Status
################

def returnCardinalBucket(windDirection):
      if (windDirection >= 337.5) or (windDirection < 22.5):
      	return 0
      if (windDirection >= 22.5) and (windDirection < 67.5):
      	return 1
      if (windDirection >= 67.5) and (windDirection < 112.5):
      	return 2
      if (windDirection >= 112.5) and (windDirection < 157.5):
      	return 3
      if (windDirection >= 157.5) and (windDirection < 202.5):
      	return 4
      if (windDirection >= 202.5) and (windDirection < 247.5):
      	return 5
      if (windDirection >= 247.5) and (windDirection < 292.5):
      	return 6
      if (windDirection >= 292.5) and (windDirection < 337.5):
      	return 7

      return 0


def returnSpeedBucket(windSpeed):
      # in meters/second
      if (windSpeed < 1.0):
           return 0     
      if (windSpeed < 2.3):
           return 1     
      if (windSpeed < 4.4):
           return 2     
      if (windSpeed < 8.5):
           return 3     
      if (windSpeed < 11.0):
           return 4     
      # greater than 11.00
      return 5     

################
# Conversion Functions
################
def CRUnits(rain):

    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        rain = rain/25.4
    return rain

def RUnits():
    English_Metric = readJSON.getJSONValue("English_Metric")
    if (English_Metric == False):  # english units
        units = " in"
    else:
        units = " mm"

    return units

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

def CBUnits(barometricpressure):

    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        barometricpressure = barometricpressure * .2953
    return barometricpressure

def BUnits():
    English_Metric = readJSON.getJSONValue("English_Metric")
    if (English_Metric == False):  # english units
        units = " in"
    else:
        units = " hPa"

    return units

def CWUnits(wind):

    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        wind = wind * 2.23694 
    return wind

def WUnits():
    English_Metric = readJSON.getJSONValue("English_Metric")
    if (English_Metric == False):  # english units
        units = " mph"
    else:
        units = " m/s"

    return units




def getWSAQIs():
    
    #read AQI from WeatherSense

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            con = util.getWeatherSenseConnection()      
            cur = con.cursor()

            query = "SELECT timestamp, AQI, AQI24Hour FROM AQI433MHZ ORDER BY timestamp DESC LIMIT 1;"
            cur.execute(query)
            
            myAQIRecords = cur.fetchall()
            if (len(myAQIRecords) > 0):
                return myAQIRecords[0][1], myAQIRecords[0][2]
            else:
                return 0.0, 0.0

        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            # sys.exit(1)


    return 0.0, 0.0




def generateCurrentWeatherJSON():
        try:
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                query = "SELECT * FROM `WeatherData` ORDER BY id DESC LIMIT 1" 
                #print("query=", query)
                cur.execute(query)
                records = cur.fetchall()
                weatherRecordCount = len(records)
                
                #print ("queryrecords=",records)
                # get column names
                query = "SHOW COLUMNS FROM WeatherData"
                cur.execute(query)
                names = cur.fetchall()
                fieldcount = len (names)
                CWJSON = {}
                for i in range(0,fieldcount):
                    if (names[i][0] == "TimeStamp"):
                        if (weatherRecordCount == 0): 
                            CWJSON[names[i][0]] = 0;
                        else:
                            CWJSON[names[i][0]] = records[0][i]
                    else:
                      if (names[i][0] == "BatteryOK"):
                       if (weatherRecordCount == 0): 
                              CWJSON[names[i][0]] = "LOW";
                       else:
                              CWJSON[names[i][0]] = records[0][i]
                      else:
                       if (weatherRecordCount == 0): 
                              CWJSON[names[i][0]] = 0;
                       else:
                              CWJSON[names[i][0]] = float(records[0][i])
                if (weatherRecordCount == 0): 
                    CWJSON["StringTime"] = "" 
                else:
                    CWJSON["StringTime"] = records[0][1].strftime("%d-%b-%Y %H:%M:%S") 
                CWJSON["StringTimeUnits"] = ""

                # now calculate rain 
                
                # calendar day rain
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE DATE(TimeStamp) = CURDATE() ORDER by id ASC"
                cur.execute(query)
                rainspanrecords = cur.fetchall()
                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                else:
                    rainspan = 0
                CWJSON["CalendarDayRain"] = round(rainspan,2)

                # Calendar Month 
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE MONTH(TimeStamp) = MONTH(NOW()) AND YEAR(TimeStamp) = YEAR(NOW())"
                cur.execute(query)
                rainspanrecords = cur.fetchall()

                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                else:
                    rainspan = 0
                CWJSON["CalendarMonthRain"] = round(rainspan,2)
                
                # last 30 days 
                timeDelta = datetime.timedelta(days=30)
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

                cur.execute(query)
                rainspanrecords = cur.fetchall()

                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                else:
                    rainspan = 0
                CWJSON["30DayRain"] = round(rainspan,2)
                
                
                # last 24 hours 
                timeDelta = datetime.timedelta(days=1)
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

                cur.execute(query)
                rainspanrecords = cur.fetchall()

                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                else:
                    rainspan = 0
                CWJSON["24HourRain"] = round(rainspan,2)
                
                
                # last 7 days 
                timeDelta = datetime.timedelta(days=7)
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

                cur.execute(query)
                rainspanrecords = cur.fetchall()

                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                else:
                    rainspan = 0
                CWJSON["7DaysRain"] = round(rainspan,2)
                
            
                                
                
                con.commit()
                
                # convert to appropiate units and add units
                # set units
                
                English_Metric = readJSON.getJSONValue("English_Metric")
                
                if (English_Metric == False):
                    # deal with English Units
                    # temperature
                    CWJSON["OutdoorTemperature"]= round(CTUnits(CWJSON["OutdoorTemperature"]),1)
                    CWJSON["OutdoorTemperatureUnits"] = TUnits() 
                    CWJSON["IndoorTemperature"]= round(CTUnits(CWJSON["IndoorTemperature"]),1)
                    CWJSON["IndoorTemperatureUnits"] = TUnits() 
                    CWJSON["BarometricTemperature"]= round(CTUnits(CWJSON["BarometricTemperature"]),1)
                    CWJSON["BarometricTemperatureUnits"] = TUnits() 

                    # wind units
                    CWJSON["WindSpeed"]= round(CWUnits(CWJSON["WindSpeed"]),1)
                    CWJSON["WindSpeedUnits"] = WUnits() 
                    CWJSON["WindGust"]= round(CWUnits(CWJSON["WindGust"]),1)
                    CWJSON["WindGustUnits"] = WUnits() 

                    # rain units
                    CWJSON["TotalRain"]= round(CRUnits(CWJSON["TotalRain"]),1)
                    CWJSON["TotalRainUnits"] = RUnits() 
                    CWJSON["CalendarDayRain"]= round(CRUnits(CWJSON["CalendarDayRain"]),1)
                    CWJSON["CalendarDayRainUnits"] = RUnits() 
                    CWJSON["CalendarMonthRain"]= round(CRUnits(CWJSON["CalendarMonthRain"]),1)
                    CWJSON["CalendarMonthRainUnits"] = RUnits() 
                    CWJSON["30DayRain"]= round(CRUnits(CWJSON["30DayRain"]),1)
                    CWJSON["30DayRainUnits"] = RUnits() 
                    CWJSON["24HourRain"]= round(CRUnits(CWJSON["24HourRain"]),1)
                    CWJSON["24HourRainUnits"] = RUnits() 
                    CWJSON["7DaysRain"]= round(CRUnits(CWJSON["7DaysRain"]),1)
                    CWJSON["7DaysRainUnits"] = RUnits() 

                    # Barometric Pressure
                    CWJSON["BarometricPressureSeaLevel"]= round(CBUnits(CWJSON["BarometricPressureSeaLevel"]),2)
                    CWJSON["BarometricPressureSeaLevelUnits"] = BUnits() 
                    CWJSON["BarometricPressure"]= round(CBUnits(CWJSON["BarometricPressure"]),2)
                    CWJSON["BarometricPressureUnits"] = BUnits() 
                    
                else:
                    # temperature units
                    CWJSON["OutdoorTemperatureUnits"] = TUnits() 
                    CWJSON["IndoorTemperatureUnits"] = TUnits() 
                    CWJSON["BarometricTemperatureUnits"] = TUnits() 
                    # wind units
                    CWJSON["WindSpeedUnits"] = WUnits() 
                    CWJSON["WindGustUnits"] = WUnits() 
                    # rain units
                    CWJSON["TotalRainUnits"] = RUnits() 
                    CWJSON["CalendarDayRainUnits"] = RUnits() 
                    CWJSON["CalendarMonthRainUnits"] = RUnits() 
                    CWJSON["30DayRainUnits"] = RUnits() 
                    CWJSON["24HourRainUnits"] = RUnits() 
                    CWJSON["7DaysRainUnits"] = RUnits() 
                    # Barometric Pressure
                    CWJSON["BarometricPressureSeaLevelUnits"] = BUnits() 
                    CWJSON["BarometricPressureUnits"] = BUnits() 

                # always same units
                CWJSON["OutdoorHumidityUnits"] = "%"
                CWJSON["IndoorHumidityUnits"] = "%"
                CWJSON["SunlightVisibleUnits"] = "lux"
                CWJSON["SunlightUVIndexUnits"] = ""
                CWJSON["AQIUnits"] = ""
                CWJSON["AQI24AverageUnits"] = ""
                CWJSON["WindDirectionUnits"] = "deg"
                
                # adjust for WS AQI
                if(config.USEWSAQI):
                    myAQI = getWSAQIs()
                    CWJSON["AQI24Average"] = myAQI[1] 
                    CWJSON["AQI"] = myAQI[0]


                return CWJSON
        except: 
                traceback.print_exc()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()
        print("done generating CWJSON=", CWJSON)
        return CWJSON



def fetchWindData(timeDelta):
        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT WindSpeed, WindDirection FROM WeatherData WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                print ("number of Records =",len(records))
                totalRecords = len(records)
                # now calculate buckets
                # 8 cardinal directions 0 - 360
                # 6 wind buckets
                df = [[],[],[],[],[],[]]
                for i in range(0,6):
                    df[i] = [0,0,0,0,0,0,0,0]
                
                for single in records:
                      windSpeed = single[0]
                      windDirection = single[1]
                      CB = returnCardinalBucket(windDirection)
                      SB = returnSpeedBucket(windSpeed)
                      #print("SB, CB=", SB, CB)
                      df[SB][CB] = df[SB][CB] + 1
                #print ("df=", df)
                #print("number of records=", totalRecords)      
                # normalize df
                if (totalRecords == 0):
                    return df
                for single in df:
                     for i in range(0,8):
                          single[i] = round(100.0*float(single[i])/float(totalRecords), 2)
		  

		
                return df
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()


	

        return df

def returnNumberConverted(speed):
    speed = CWUnits(speed)
    return str(round(speed,1))

def figCompassRose(df):

        '''
	df = [77.5, 72.5, 70.0, 45.0, 22.5, 42.5, 40.0, 62.5]
        fig = px.bar_polar(df, r="frequency", theta="direction",
              color="strength", template="plotly_dark",
              color_discrete_sequence= px.colors.sequential.Plasma_r)
        '''
        #print("df =", df) 
        fig = go.Figure(
           )
        fig.add_trace(go.Barpolar(
            r=df[5],

            name='> ' + returnNumberConverted(11) + " " + WUnits(),
            marker_color='rgb(40,0,163)'
        ))
        fig.add_trace(go.Barpolar(
            r=df[4],
            name=returnNumberConverted(8.5) +'-'+returnNumberConverted(11) + " " + WUnits(),
            marker_color='rgb(80,0,163)'
        ))
        
        fig.add_trace(go.Barpolar(
            r=df[3],
            name=returnNumberConverted(4.4) +'-'+returnNumberConverted(8.5) + " " + WUnits(),
            marker_color='rgb(120,0,163)'
        ))
        fig.add_trace(go.Barpolar(
            r=df[2],
            name=returnNumberConverted(2.2) +'-'+returnNumberConverted(4.4) + " " + WUnits(),
            marker_color='rgb(160,0,163)'
        ))
        fig.add_trace(go.Barpolar(
            r=df[1],
            name=returnNumberConverted(1.0) +'-'+returnNumberConverted(2.3) + " " + WUnits(),
            marker_color='rgb(200,0,163)'
        ))
        fig.add_trace(go.Barpolar(
            r=df[0],
            name=returnNumberConverted(0.0) +'-'+returnNumberConverted(1) + " " + WUnits(),
            marker_color='rgb(240,0,163)'
        ))
       
        fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
        fig.update_layout(
            title='Wind Speed Distribution Past Week',
            #font_size=16,
            legend_font_size=16,
            #polar_radialaxis_ticksuffix='%',
            #polar_angularaxis_rotation=90,
            font=dict(size=16), 
            polar=dict(
               radialaxis=dict(ticksuffix="%",angle=45,tickfont=dict(size=12)),
               angularaxis=dict(direction="clockwise",tickfont=dict(size=14)),
	       ),
              #color_discrete_sequence= go.colors.sequential.Plasma_r,
	    
	    template='plotly_dark',

        )
        return fig

def buildCompassRose():

      layout = []
      myLabelLayout = []

      timeDelta = datetime.timedelta(days=7)
      data = fetchWindData(timeDelta)
      fig = figCompassRose(data)
      layout.append(dcc.Graph(id={"type": "WPRdynamic", "index": "compassrose"},figure=fig))	
      return layout

###################
#### OTH Graph ####
###################

def fetchOTH(timeDelta):

        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT OutdoorTemperature, OutdoorHumidity, TimeStamp FROM `WeatherData` WHERE (TimeStamp > '%s') ORDER BY id ASC" % (before)
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



def buildOutdoorTemperature_Humidity_Graph_Figure():
    
    timeDelta = datetime.timedelta(days=7)
    records = fetchOTH(timeDelta)

    Time = []
    Temperature = []
    Humidity = []
    for record in records:
        Time.append(record[2])
        Temperature.append(record[0])
        Humidity.append(record[1])

    if (len(records) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Weather Data Available')
        return fig

    # set units
    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        for i in range(0, len(Temperature)):
            Temperature[i] = (9.0/5.0 * Temperature[i]) +32.0
        units = "F"
    else:
        units = "C"
    
    # Create figure with secondary y-axis
    fig = go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=Time, y=Temperature, name="Temperature",
        line = dict(
                    color = ('red'),
                    width = 2,
                    ),
       ), 
                    secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x=Time, y=Humidity, name="Humidity", 
        line = dict(
                    color = ('blue'),
                    width = 2,
                    ),
        ),
                    secondary_y = True
    )

    # Add figure title
    fig.update_layout(
        title_text="Outdoor Temperature and Humidity ", height=400
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")
   
    minTemp = min(Temperature)*0.9
    maxTemp = max(Temperature)*1.10
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Temperature ("+units+")</b>", range = (minTemp, maxTemp), secondary_y=False, side='left')
    fig.update_yaxes(title_text="<b>Humidity (%)</b>", range = (0,100), secondary_y=True, side='right')
    
    return fig

def buildOutdoorTemperature_Humidity_Graph():

    fig = buildOutdoorTemperature_Humidity_Graph_Figure()

    graph =  dcc.Graph(
                    id = {'type' : 'WPGdynamic', 'index': 'graph-oth' },
                    figure=fig,
                    animate = False
                    )
    return graph

###################
#### BP Graph ####
###################

def fetchBP(timeDelta):

        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT BarometricPressure, BarometricPressureSeaLevel, TimeStamp FROM `WeatherData` WHERE (TimeStamp > '%s') ORDER BY id ASC" % (before)
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


def buildBP_Graph_Figure():
    
    timeDelta = datetime.timedelta(days=7)
    records = fetchBP(timeDelta)

    Time = []
    BP = []
    BPSL = []
    # TODO bad data needs cleanup
    for record in records:
        Time.append(record[2])
        if (record[0] > 900):
            BP.append(record[0])
        else:     
            BP.append(record[0] * 10)
        if (record[1] > 900):
            BPSL.append(record[1])
        else:    
            BPSL.append(record[1] * 10)

    if (len(records) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Weather Data Available')
        return fig

    # TODO set units
    # English_Metric = readJSON.getJSONValue("English_Metric")
    
    # Create figure with secondary y-axis
    fig = go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=Time, y=BP, name="Barometric Pressure",
        line = dict(
                    color = ('red'),
                    width = 2,
                    ),
       ), 
                    secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x=Time, y=BPSL, name="Barometric Pressure SL", 
        line = dict(
                    color = ('blue'),
                    width = 2,
                    ),
        ),
                    secondary_y = True
    )

    # Add figure title
    fig.update_layout(
        title_text="Barometric Pressure", height=400
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")
   
    minBP = min(BP)*0.95
    maxBP = max(BP)*1.05
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Barometric Pressure (hPa)</b>", range = (minBP, maxBP), secondary_y=False, side='left')
    fig.update_yaxes(title_text="<b>Barometric Pressure SL (hPa)</b>", range = (minBP,maxBP), secondary_y=True, side='right')
    
    return fig

def buildPB_Graph():

    fig = buildBP_Graph_Figure()

    graph =  dcc.Graph(
                    id = {'type' : 'WPGdynamic', 'index': 'graph-oth' },
                    figure=fig,
                    animate = False
                    )
    return graph

###################
### CPU Graph ####
###################

def fetchCPU(timeDelta):

        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT CPUTemperature, TimeStamp FROM `WeatherData` WHERE (TimeStamp > '%s') ORDER BY id ASC" % (before)
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

def buildCPU_Figure():
    
    timeDelta = datetime.timedelta(days=7)
    records = fetchCPU(timeDelta)

    Time = []
    Temperature = []
    for record in records:
        Time.append(record[1])
        Temperature.append(record[0])
 
    if (len(records) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Weather Data Available')
        return fig

    # set units
    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        for i in range(0, len(Temperature)):
            Temperature[i] = (9.0/5.0 * Temperature[i]) +32.0
        units = "F"
    else:
        units = "C"
    
    # Create figure
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=Time, y=Temperature, name="CPU Temperature",
        line = dict(
                    color = ('red'),
                    width = 2,
                    ),
       ), 
                    secondary_y = False,
    )

 
    # Add figure title
    fig.update_layout(
        title_text="CPU Temperature", height=400
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")
   
    minTemp = min(Temperature)*0.9
    maxTemp = max(Temperature)*1.10
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>CPU Temperature ("+units+")</b>", range = (minTemp, maxTemp), secondary_y=False, side='left')
    
    return fig

def buildCPU_Graph():

    fig = buildCPU_Figure()

    graph =  dcc.Graph(
                    id = {'type' : 'WPGdynamic', 'index': 'graph-oth' },
                    figure=fig,
                    animate = False
                    )
    return graph

###################
####  AQI Graph ####
###################

def fetchAQI(timeDelta):

    if (config.USEWSAQI):
        try:
                #print("trying database")
                con = util.getWeatherSenseConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT AQI, AQI24Hour, timestamp FROM `AQI433MHZ` WHERE (timestamp > '%s') ORDER BY id ASC" % (before)
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

    else:
        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT AQI, AQI24Average, TimeStamp FROM `WeatherData` WHERE (TimeStamp > '%s') ORDER BY id ASC" % (before)
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



def buildAQIGraphFigure():
    
    timeDelta = datetime.timedelta(days=7)
    records = fetchAQI(timeDelta)

    Time = []
    AQI = []
    AQI24 = []
    for record in records:
        Time.append(record[2])
        AQI.append(record[0])
        AQI24.append(record[1])

    units = ""
   
    # Create figure with secondary y-axis
    fig = go.Figure()
    if (len(records) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Weather Data Available')
        return fig


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=Time, y=AQI24, name="AQI 24 Hour Ave",
        line = dict(
                    color = ('red'),
                    width = 2,
                    ),
       ), 
                    secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x=Time, y=AQI, name="AQI", 
        line = dict(
                    color = ('blue'),
                    width = 2,
                    ),
        ),
                    secondary_y = True
    )

    # Add figure title
    fig.update_layout(
        title_text="AQI", height=400
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")
   
    minTemp = min(AQI)*0.9
    maxTemp = max(AQI)*1.10
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>AQI 24H Ave</b>", range = (minTemp, maxTemp), secondary_y=False, side='left')
    fig.update_yaxes(title_text="<b>AQI </b>", range = (minTemp,maxTemp), secondary_y=True, side='right')
    
    return fig


########################

def buildAQI_Graph():

    fig = buildAQIGraphFigure()

    graph =  dcc.Graph(
                    id = {'type' : 'WPGdynamic', 'index': 'graph-aqi' },
                    figure=fig,
                    animate = False
                    )
    return graph

################################
def fetchSUV(timeDelta):

        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()      
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT SunlightVisible, SunlightUVIndex, TimeStamp FROM `WeatherData` WHERE (TimeStamp > '%s') ORDER BY id ASC" % (before)
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


def buildSunlightUVIndexGraphFigure():
    Time = []
    Sunlight = []
    UVIndex = []

    timeDelta = datetime.timedelta(days=7)
    records = fetchSUV(timeDelta)

    for record in records:
        Time.append(record[2])
        Sunlight.append(record[0])
        UVIndex.append(record[1])

    # Create figure with secondary y-axis
    fig = go.Figure()
    if (len(records) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No Weather Data Available')
        return fig


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=Time, y=Sunlight, name="Sunlight",
        line = dict(
                    color = ('red'),
                    width = 2,
                    ),
       ),
       secondary_y = False
    )

    fig.add_trace(
        go.Scatter(x=Time, y=UVIndex, name="UV Index", 
        line = dict(
                    color = ('blue'),
                    width = 2,
                    ),
        ),
       secondary_y = True
    )

    # Add figure title
    fig.update_layout(
        title_text="Sunlight and UV Index "
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Sunlight (Lux)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>UV Index </b>", secondary_y=True, range= (0,10))
    
    return fig


def buildSunlight_UVIndex_Graph():


    fig = buildSunlightUVIndexGraphFigure()

    graph =  dcc.Graph(
                    id = {'type' : 'WPGdynamic', 'index': 'graph-suv' },
                    figure=fig,
                    animate = False
                    )
    return graph

################################

# WS AQI Select Functions



################
# Page Functions
################

def WeatherPage():
    global CWJSON
    maintextsize = "2.0em"
    subtextcolor = "green"
    maintextcolor = "black"

    Cols = []


    Cols.append(buildOutdoorTemperature_Humidity_Graph())
    Cols.append(buildSunlight_UVIndex_Graph())
    Cols.append(buildPB_Graph())
    if(config.USEWSAQI):
        Cols.append(buildAQI_Graph())
    Cols.append(buildCPU_Graph()) 

    print("WP-CWSJON=", CWJSON)
    Row1 = html.Div(
        [ 
        #dbc.Row( dbc.Col(html.Div(id="Weather Instruments"))),
        dbc.Row( dbc.Col(html.Div(html.H6(id={'type' : 'WPdynamic', 'index': "StringTime"},children="Weather Instruments")))),
            
            dbc.Row(
                [ 
                    dbc.Col(html.Div(
                     [

                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "OutdoorTemperature"},
                            children=str(CWJSON["OutdoorTemperature"])+TUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                            #children=str(round(CTUnits(CWJSON["OutdoorTemperature"]),1))+TUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Outdoor Temperature", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "OutdoorHumidity"},
                            children=str(round(CWJSON["OutdoorHumidity"],1))+" %", style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Outdoor Humidity", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "IndoorTemperature"},
                            children=str(CWJSON["IndoorTemperature"])+TUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Indoor Temperature", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "IndoorHumidity"},
                            children=str(round(CWJSON["IndoorHumidity"],1))+" %", style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Indoor Humidity", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "SunlightVisible"},
                            children=str(round(CWJSON["SunlightVisible"]))+" lux", style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Sunlight", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     ],
                     ),
                     width=3,
                    ),
                     dbc.Col(html.Div(
                     [
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "BarometricPressureSeaLevel"},
                            children=str(CWJSON["BarometricPressureSeaLevel"])+BUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Barometric Pressure", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "WindSpeed"},
                            children=str(CWJSON["WindSpeed"])+WUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Wind Speed", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "WindGust"},
                            children=str(CWJSON["WindGust"])+WUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Wind Gust", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "WindDirection"},
                            children=str(CWJSON["WindDirection"])+" deg", style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Wind Direction", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "SunlightUVIndex"},
                            children=str(round(CWJSON["SunlightUVIndex"],1)), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Sunlight UV Index", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                        
                     ],
                     ),
                     width=3,
                    ),
		            dbc.Col(html.Div(buildCompassRose())),
      
	            ],
            ),
        ]
	    )

    Row2 = html.Div(
        [
        dbc.Row(
            [
                dbc.Col(html.Div("Rain / Air Quality")),
            ]
        ),
	    dbc.Row(
	    [
                     dbc.Col(html.Div(
                     [
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "TotalRain"},
                            children=str(CWJSON["TotalRain"])+RUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                            
                         html.P("Total Rain", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "CalendarDayRain"},
                            children=str(CWJSON["CalendarDayRain"])+RUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Daily Rain", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "CalendarMonthRain"},
                            children=str(CWJSON["CalendarMonthRain"])+RUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                            
                         html.P("Calendar Month", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),

                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "30DayRain"},
                            children=str(CWJSON["30DayRain"])+RUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                            
                         html.P("Last 30 Days", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                    ],
                     ),
                     width=3,
                     ),
                     dbc.Col(html.Div(
                     [
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "24HourRain"},
                            children=str(CWJSON["24HourRain"])+RUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                            
                         html.P("Last 24 Hours", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "7DaysRain"},
                            children=str(CWJSON["7DaysRain"])+RUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                            
                         html.P("Last 7 Days", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "AQI"},
                            children=str(CWJSON["AQI"]), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Current AQI", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),

                     html.Div(
                         [html.H1(id={'type' : 'WPdynamic', 'index' : "AQI24Average"},
                            children=str(CWJSON["AQI24Average"]), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("24 Hour AQI Average", style={"color":subtextcolor})
                         ], id="ot1", className="mini_container",),
                    ]
                    ),
                     width=3,
                    ),
                     dbc.Col( html.Div(html.Figure(
                     [
                     html.Div(id={'type' : 'WPIdynamic', 'index' : "SkyCamImage"},
                          children = [
                            html.Img( height=350, width=350*1.77, src="/assets/skycamera.jpg"),
                            html.Figcaption("SkyWeather Cam"),
                            ]),

                     ]
                     ),
                    ),
                     width=6, align="center",
                    ),
            ],
                   ),


        ]
    )

# graphs
    Row3 = html.Div(
    [
            dbc.Row(
            [
                dbc.Col(Cols,width = 12)
            ]
            )
   ]
   )



#########
# combined layout
#########


    layout = dbc.Container([
        Row1, Row2, Row3 ],
        className="p-5",
    )
    return layout


CWJSON = generateCurrentWeatherJSON()