import os
import shutil
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, MATCH, ALL, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import traceback
import datetime
import base64

import time

import threading

import status_page 
import log_page
import weather_page
import indoorth

from non_impl import NotImplPage 

from navbar import Navbar, Logo
logo = Logo()
print("new navbar=")
nav = Navbar()

UpdateCWJSONLock = threading.Lock()
SGSDASHSOFTWAREVERSION = "005"



newValveState = ""
# state of previous page
previousPathname = ""

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE])

app.config.suppress_callback_exceptions = True

app.layout =  html.Div(

        [

       html.Div(id='my-output-interval'),

       dcc.Interval(
            id='main-interval-component',
            interval=10*1000, # in milliseconds - leave as 10 seconds
            n_intervals=0
            ) ,
       #dcc.Interval(
       #     id='weather-update-interval-component',
       #     interval=5*1000, # in milliseconds
       #     n_intervals=0
       #     ) ,
       
        #dbc.Spinner(id="main-spinner", color="white" ),
        #dcc.Location(id = 'url', refresh = True),
        dcc.Location(id = 'url', refresh = False),

        html.Div(id = 'page-content'),
        #html.Div(id = 'wp-placeholder', style={'display':'none'}) 
        ],

        id="mainpage"

    )


@app.server.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    #r.headers["Cache-Control"] = 'no-store'
    #r.headers["Pragma"] = "no-store"
    #r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'must-revalidate, max-age=10' 
    return r


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])


def display_page(pathname):
    global previousPathname

    print("--------------------->>>>>>>>>>>>>>>>new page")
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    print("begin=",nowString)
    
    print("pathname=", pathname)
    print("previousPathname=", previousPathname)
    i = [i['prop_id'] for i in dash.callback_context.triggered]
    print('i=', i)
    print('TRIGGER(S):', [i['prop_id'] for i in dash.callback_context.triggered])
    if (i[0] == '.'):
        print("---no page change--- ['.']")
        raise PreventUpdate	
    #if (pathname == previousPathname):
    #    print("---no page change---Equal Pathname")
    #    raise PreventUpdate	
    previousPathname = pathname
    
    myLayout = NotImplPage()
    myLayout2 = ""
    if pathname == '/status_page':
        myLayout = status_page.StatusPage() 
        myLayout2 = ""
    if pathname == '/log_page':
        myLayout = log_page.LogPage()
        myLayout2 = ""
    if pathname == '/weather_page':
        myLayout = weather_page.WeatherPage()
        myLayout2 = ""
    if pathname == '/indoorth':
        myLayout = indoorth.IndoorTHPage()
        myLayout2 = ""
    
    #print("myLayout= ",myLayout)
    #print("myLayout2= ",myLayout2)
    print("page-content= ",app.layout)
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    print("end=",nowString)
    return (logo, nav,myLayout, myLayout2 )

##################
# Log Page 
##################
@app.callback(Output({'type' : 'LPdynamic', 'index' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'LPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'LPdynamic', 'index' : MATCH}, 'value'  )]
              )

def logpageupdate(n_intervals, id, value):
    
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    print ("---->inputs:",dash.callback_context.inputs) 
    print(">log_page table Update started",id['index'])
    print("LG-n_intervals=", n_intervals) 
    if (id['index'] == "systemlog"):
        data = log_page.fetchSystemLog()
        fig = log_page.buildTableFig(data,"System Log")
    
    if (id['index'] == "valvelog"):
        data = log_page.fetchValveLog()
        fig = log_page.buildTableFig(data,"Valve Log")
        return fig
    
    if (id['index'] == "sensorlog"):
        data = log_page.fetchSensorLog()
        fig = log_page.buildTableFig(data,"Sensor Log")

    print("<log_page table Update complete",id['index'])
    return fig
   else:
    raise PreventUpdate

##################
# Status Page
##################

@app.callback(
	      [
	      Output({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'value' ),
	      Output({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'label' )
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'id' )],
              [State({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'value'  )]
              )

def update_gauges(n_intervals, id, value):
   if (True): # 1 minutes -10 second timer
   #if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
     #print(">status_page Gauge Update started",id['GaugeType'])
     newValue = status_page.updateGauges(id) 
     if (id['GaugeType'] == 'pi-disk'):
        myName = "Pi SD Card Free" 
     if (id['GaugeType'] == 'pi-memory'):
        myName = "Pi Memory Usage" 
     if (id['GaugeType'] == 'pi-loading'):
        myName = "Pi CPU Loading" 
     #print("<status_page Gauge Update complete",id['GaugeType'])

     return newValue, myName 
   else:
    raise PreventUpdate


@app.callback(Output({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color'  )]
              )

def update_statuspage(n_intervals, id, color):
   global newValveState
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    #print(">status_page Indicator Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    #print("newValveState=", newValveState)
    #print("n_intervals=", n_intervals)
    #print ('Indicator id {} / n_intervals = {}'.format(id['index'], n_intervals))
    if (newValveState == ""):
        newValveState = status_page.returnLatestValveRecord(id['DeviceID'] )

    status  = status_page.returnIndicatorValue(newValveState, id['index'])
    color = status_page.updateIndicator(status)

    if (id['index'] == 7):
        newValveState = ""    
    #print("<status_page Indicator Update complete",id['index'], id['DeviceID'])
    return color
   else:
    raise PreventUpdate

 
##################
# Weather Page
##################




#################
# Callbacks
#################
@app.callback(
	      [
	      Output({'type' : 'WPIdynamic', 'index' : 'SkyCamImage'}, 'children' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPIdynamic', 'index' : 'SkyCamImage'}, 'id' )],
              [State({'type' : 'WPIdynamic', 'index' : 'SkyCamImage'}, 'value'  )]
              )

def updateWeatherImagePage(n_intervals,id, value):
    print("+++++++++++++updateWImageP n_intervals", n_intervals)
    print("+++++++++++++updateWImageP (n_intervals %6)", n_intervals% 6)
    if ((n_intervals % (1*6)) == 0) or (n_intervals ==0): # 1 minutes -10 second timer
        print("--->>>updateSkyCamImage", datetime.datetime.now(), n_intervals)
        try:
            '''
            # delete old file names

            fileList = glob.glob("/home/pi/SDL_Pi_SkyWeather2/dash_app/assets/imagedisplay*")
            # Iterate over the list of filepaths & remove each file.
            for filePath in fileList:
                    os.remove(filePath)
                        
            # build names
            basename = "imagedisplay"+str(n_intervals)+".jpg?"
            htmlname =  "/assets/"+ basename
            newname = "/home/pi/SDL_Pi_SkyWeather2/dash_app/assets/"+basename 
            # move camera file to new name
            shutil.copy('/home/pi/SDL_Pi_SkyWeather2/dash_app/assets/skycamera.jpg', newname)

            '''
            htmlname =  "/assets/skycamera.jpg?"
            value = html.Div( [
                          html.Img( height=350, width=350*1.77, src=htmlname),             
                          #html.Figcaption("SkyWeather2 Cam"),
                          html.Figcaption(htmlname)
                          ])
            print("+++++++value=", value)

        except:
            print(traceback.format_exc())
            print("camera file not found")
            htmlname = "/assets/SW2Textcolor.png"
            value = html.Div( [
                          html.Img( height=150, width=150*2.86, src=htmlname),             
                          html.Figcaption("SkyWeather2 Cam"),
                          ])

            pass
  
    else:
        raise PreventUpdate
    return [value]

@app.callback(
	      [
	      Output({'type' : 'WPdynamic', 'index' : MATCH}, 'children' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateWeatherUpdate(n_intervals,id, value):


    if ((n_intervals % (1*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
    #if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        print("--->>>updateWeatherUpdateString", datetime.datetime.now(), n_intervals)
        print("updateWeatherUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            UpdateCWJSONLock.acquire()
            weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            UpdateCWJSONLock.release()
            value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
            value = "Weather Updated at:" + value

            return [value]
        
        UpdateCWJSONLock.acquire()
        value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
        UpdateCWJSONLock.release()
    else:
        raise PreventUpdate
    return [value]


@app.callback(
	      [
	      Output({'type' : 'WPRdynamic', 'index' : MATCH}, 'figure' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPRdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPRdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateWeatherRosePage(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate
    print("WeatherRose n_intervals=", n_intervals)
    # update every 15 minutes
    #if (True): # 15 minutes -10 second timer
    if ((n_intervals % (15*6)) == 0): # 15 minutes -10 second timer
        print("--->>>updateCompassRose", datetime.datetime.now(), n_intervals)
        timeDelta = datetime.timedelta(days=7)
        data = weather_page.fetchWindData(timeDelta)
        fig = weather_page.figCompassRose(data)
 
    else:
        raise PreventUpdate
    return [fig]


@app.callback(
	      [
	      Output({'type' : 'WPGdynamic', 'index' : MATCH}, 'figure' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPGdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPGdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateWeatherGraphPage(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate

    if ((n_intervals % (1*6)) == 0): # 15 minutes -10 second timer
    #if ((n_intervals % (5*6)) == 0): # 15 minutes -10 second timer
       print("--->>>updateWeatherGraphs", datetime.datetime.now(), n_intervals, id)
       print("--->>>updateWeatherGraphs:", id['index'])
       if (id['index'] ==  'graph-oth'):
           fig = weather_page.buildOutdoorTemperature_Humidity_Graph_Figure()
       if (id['index'] ==  'graph-suv'):
           fig = weather_page.buildSunlightUVIndexGraphFigure()
       if (id['index'] ==  'graph-aqi'):
           fig = weather_page.buildAQIGraphFigure()
           #print("aqi-fig=",fig)

    else:
        raise PreventUpdate
    return [fig]


# Indoor Temperature Humidity


@app.callback(
	      [
	      Output({'type' : 'WPITHdynamic', 'index' : MATCH}, 'children' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'WPITHdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'WPITHdynamic', 'index' : MATCH}, 'value'  )]
              )

def updateIndoorTHUpdate(n_intervals,id, value):


    if ((n_intervals % (1*6)) == 0) or (n_intervals ==0): # 1 minutes -10 second timer
    #if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        print("--->>>updateIndoorTHUpdate", datetime.datetime.now(), n_intervals)
        print("updateIndoorTH  n_intervals =", n_intervals, id['index'])
        if (id['index'] ==  'temperature'):
           timeDelta = datetime.timedelta(days=7)
           data = indoorth.generateTHData(timeDelta)
           fig = indoorth.buildTemperatureGraph(data)
           return [fig]
        if (id['index'] ==  'humidity'):
           timeDelta = datetime.timedelta(days=7)
           data = indoorth.generateTHData(timeDelta)
           fig = indoorth.buildHumidityGraph(data)
           return [fig]
        
    else:
        raise PreventUpdate
    return [value]


##########################

if __name__ == '__main__':
    #app.run_server(debug=True, host='0.0.0.0')
    app.run_server(host='0.0.0.0')
