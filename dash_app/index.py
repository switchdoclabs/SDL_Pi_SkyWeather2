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
import aftershock_page
import aqi_page
import lightning_page
import solarmax_page
import skycam_page
import radiation_page

from non_impl import NotImplPage 

from navbar import Navbar, Logo

import logging



logging.getLogger('werkzeug').setLevel(logging.ERROR)

UpdateCWJSONLock = threading.Lock()
SGSDASHSOFTWAREVERSION = "006"

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

print (STATIC_PATH)


newValveState = ""
# state of previous page
previousPathname = ""

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE])

#print("new navbar=")
nav = Navbar()
logo = Logo(app)

app.config.suppress_callback_exceptions = True

app.layout =  html.Div(

        [

       html.Div(id='my-output-interval'),

       dcc.Interval(
            id='main-interval-component',
            interval=10*1000, # in milliseconds - leave as 10 seconds
            n_intervals=0
            ) ,

        dcc.Interval(
            id='minute-interval-component',
            interval=60 * 1000,  # in milliseconds
            n_intervals=0
        ),


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

    #print("--------------------->>>>>>>>>>>>>>>>new page")
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    #print("begin=",nowString)
    
    #print("pathname=", pathname)
    #print("previousPathname=", previousPathname)
    i = [i['prop_id'] for i in dash.callback_context.triggered]
    #print('i=', i)
    #print('TRIGGER(S):', [i['prop_id'] for i in dash.callback_context.triggered])
    if (i[0] == '.'):
        #print("---no page change--- ['.']")
        raise PreventUpdate	
    #if (pathname == previousPathname):
    #    print("---no page change---Equal Pathname")
    #    raise PreventUpdate	
    previousPathname = pathname
    
    #myLayout = NotImplPage()
    myLayout = status_page.StatusPage() 
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
    if pathname == '/skycam_page':
        myLayout = skycam_page.SkyCamPage()
        myLayout2 = ""
    if pathname == '/indoorth':
        myLayout = indoorth.IndoorTHPage()
        myLayout2 = ""
    if pathname == '/aqi_page':
        myLayout = aqi_page.AQIPage()
        myLayout2 = ""
    if pathname == '/lightning_page':
        myLayout = lightning_page.LightningPage()
        myLayout2 = ""
    if pathname == '/solarmax_page':
        myLayout = solarmax_page.SolarMAXPage()
        myLayout2 = ""
    if pathname == '/aftershock_page':
        myLayout = aftershock_page.AfterShockPage()
        myLayout2 = ""
    if pathname == '/radiation_page':
        myLayout = radiation_page.RadiationPage()
        myLayout2 = ""
 
    #print("myLayout= ",myLayout)
    #print("myLayout2= ",myLayout2)
    #print("page-content= ",app.layout)
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    #print("end=",nowString)
    return (logo, nav,myLayout, myLayout2 )

##################
# Log Page 
##################
@app.callback(Output({'type' : 'LOGPdynamic', 'index' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'LOGPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'LOGPdynamic', 'index' : MATCH}, 'value'  )]
              )

def logpageupdate(n_intervals, id, value):
    
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    #print ("---->inputs:",dash.callback_context.inputs) 
    #print(">log_page table Update started",id['index'])
    #print("LG-n_intervals=", n_intervals) 
    if (id['index'] == "systemlog"):
        data = log_page.fetchSystemLog()
        fig = log_page.buildTableFig(data,"System Log")
 

        #print("<log_page table Update complete",id['index'])
        return fig
   else:
    raise PreventUpdate

##################
# Status Page
##################
@app.callback(Output({'type' : 'VSPdynamic', 'index' : MATCH }, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'VSPdynamic', 'index' : MATCH }, 'id' )],
              [State({'type' : 'VSPdynamic', 'index' : MATCH}, 'color'  )]
              )

def update_indicators(n_intervals, id, color):
   if (True): # 1 minutes -10 second timer
    return status_page.returnPiThrottledColor(id) 

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
     if (id['GaugeType'] == 'pi-temp'):
        myName = "Pi CPU Temperature(C)" 
     #print("<status_page Gauge Update complete",id['GaugeType'])

     return newValue, myName 
   else:
    raise PreventUpdate


@app.callback(Output({'type' : 'SPdynamic', 'index' : MATCH }, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPdynamic', 'index' : MATCH }, 'id' )],
              [State({'type' : 'SPdynamic', 'index' : MATCH}, 'color'  )]
              )

def update_indicators(n_intervals, id, color):

   #if ((n_intervals % (1*5)) == 0): # 15 minutes -10 second timer
   if ((n_intervals % (16*6)) == 0): # 15 minutes -10 second timer
     
    color = status_page.updateIndicators(id)

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
    #print("+++++++++++++updateWImageP n_intervals", n_intervals)
    #print("+++++++++++++updateWImageP (n_intervals %6)", n_intervals% 6)
    if ((n_intervals % (1*6)) == 0) or (n_intervals ==0): # 1 minutes -10 second timer
        #print("--->>>updateSkyCamImage", datetime.datetime.now(), n_intervals)
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
            #print("+++++++value=", value)

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
        #print("--->>>updateWeatherUpdateString", datetime.datetime.now(), n_intervals)
        #print("updateWeatherUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            UpdateCWJSONLock.acquire()
            weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            UpdateCWJSONLock.release()
            value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
            value = "Weather Updated at:" + value

            return [value]
        elif id['index'] == 'WindDirection':
            wind_dir = weather_page.CWJSON[id['index']]
            wind_dir_str = weather_page.calc_wind_quadrant(wind_dir)
            value = str(wind_dir) + weather_page.CWJSON[id['index']+'Units'] + " " + wind_dir_str
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
    #print("WeatherRose n_intervals=", n_intervals)
    # update every 15 minutes
    #if (True): # 15 minutes -10 second timer
    if ((n_intervals % (15*6)) == 0): # 15 minutes -10 second timer
        #print("--->>>updateCompassRose", datetime.datetime.now(), n_intervals)
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
       #print("--->>>updateWeatherGraphs", datetime.datetime.now(), n_intervals, id)
       #print("--->>>updateWeatherGraphs:", id['index'])
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
        #print("--->>>updateIndoorTHUpdate", datetime.datetime.now(), n_intervals)
        #print("updateIndoorTH  n_intervals =", n_intervals, id['index'])
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


# lightning_page callbacks


@app.callback(
    [
        Output({'type': 'Lightninggraph', 'index': MATCH}, 'figure'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'Lightninggraph', 'index': MATCH}, 'id')],
    [State({'type': 'Lightninggraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    #print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphLightning figure")
        figure = lightning_page.build_graphLightning_figure()
    if (myIndex == '2'):
        print("GraphLightning Solar Currents")
        figure = lightning_page.build_graph1_figure()
    if (myIndex == '3'):
        print("GraphLightning Solar Voltages")
        figure = lightning_page.build_graph2_figure()

    return [figure]


@app.callback(
    [
        Output({'type': 'LPdynamic', 'index': MATCH}, 'children'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'LPdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'LPdynamic', 'index': MATCH}, 'value')]
)
def updateLightningUpdate(n_intervals, id, value):
    if (True):
        # if ((n_intervals % (1*2)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer

        # if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        print("--->>>updateLightningUpdate", datetime.datetime.now(), n_intervals)
        print("updateLightningUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            # weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            # value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
            now = datetime.datetime.now()
            nowString = now.strftime('%Y-%m-%d %H:%M:%S')
            value = "Lightning Updated at:" + nowString
            lightning_page.updateLightningLines()

            return [value]

        value = lightning_page.LLJSON[id['index']]
    else:
        raise PreventUpdate
    return [value]


# aqi_page callbacks

@app.callback(
    [
        Output({'type': 'AQIgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'AQIgraph', 'index': MATCH}, 'id')],
    [State({'type': 'AQIgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphAQI figure")
        figure = aqi_page.build_graphAQI_figure()
    if (myIndex == '2'):
        print("GraphAQI Solar Currents")
        figure = aqi_page.build_graph1_figure()
    if (myIndex == '3'):
        print("GraphAQI Solar Voltages")
        figure = aqi_page.build_graph2_figure()

    return [figure]

############
# callbacks
############
# radiation_page  callbacks
@app.callback(
    [
        Output({'type': 'RADgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'RADgraph', 'index': MATCH}, 'id')],
    [State({'type': 'RADgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphRAD figure")
        figure = radiation_page.build_graphRAD_figure()
    if (myIndex == '2'):
        print("GraphRAD Solar Currents")
        figure = radiation_page.build_graph1_figure()
    if (myIndex == '3'):
        print("GraphRAD Solar Voltages")
        figure = radiation_page.build_graph2_figure()

    return [figure]

############
# callbacks
############
# aftershock_page callbacks


@app.callback(
    [
        Output({'type': 'AfterShockgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'AfterShockgraph', 'index': MATCH}, 'id')],
    [State({'type': 'AfterShockgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    #print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        #print("GraphAfterShock figure")
        figure = aftershock_page.build_graphAfterShock_figure()
    if (myIndex == '2'):
        #print("GraphAfterShock Solar Currents")
        figure = aftershock_page.build_graph1_figure()
    if (myIndex == '3'):
        #print("GraphAfterShock Solar Voltages")
        figure = aftershock_page.build_graph2_figure()

    return [figure]


@app.callback(
    [
        Output({'type': 'ASdynamic', 'index': MATCH}, 'children'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'ASdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'ASdynamic', 'index': MATCH}, 'value')]
)
def updateAfterShockUpdate(n_intervals, id, value):
    if (True):
        # if ((n_intervals % (1*2)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer

        # if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        #print("--->>>updateAfterShockUpdate", datetime.datetime.now(), n_intervals)
        #print("updateAfterShockUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            # weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            # value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
            now = datetime.datetime.now()
            nowString = now.strftime('%Y-%m-%d %H:%M:%S')
            value = "AfterShock Updated at:" + nowString
            aftershock_page.updateAfterShockLines()

            return [value]

        value = aftershock_page.ASJSON[id['index']]
    else:
        raise PreventUpdate
    return [value]



# solarmax_page callbacks

@app.callback(
    [
        Output({'type': 'SolarMAXgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('minute15-interval-component', 'n_intervals'),
     Input({'type': 'SolarMAXgraph', 'index': MATCH}, 'id')],
    [State({'type': 'SolarMAXgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '2'):
        print("SolarMAX Solar Currents")
        figure = solarmax_page.build_graph1_figure()
    if (myIndex == '3'):
        print("SolarMAX Solar Voltages")
        figure = solarmax_page.build_graph2_figure()

    return [figure]

##########################


# skycam_page callbacks

@app.callback(
    [
        Output({'type': 'SkyCamGraphs', 'index': 0}, 'children'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'SkyCamGraphs', 'index': 0}, 'id')],
    [State({'type': 'SkyCamGraphs', 'index': 0}, 'value')]
)
def update_sky_metrics(n_intervals, id, value):
    print("skycam_n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    SkyCamList = skycam_page.getSkyCamList()
    output = skycam_page.build_solar_graphs(SkyCamList)
    #print("output=", output)
    return [output]




@app.callback(
    [
        Output({'type': 'SkyCamPics', 'index': 0}, 'children'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'SkyCamPics', 'index': 0}, 'id')],
    [State({'type': 'SkyCamPics', 'index': 0}, 'value')]
)
def update_skypic_metrics(n_intervals, id, value):
    print("skycampic_n_intervals=", n_intervals)
    myIndex = id['index']
    # build pictures
    SkyCamList = skycam_page.getSkyCamList()
    output = skycam_page.buildPics(SkyCamList)
    #print("picoutput=", output)
    return [output]







@app.server.route('/static/<resource>')
def serve_static(resource):
        return flask.send_from_directory(STATIC_PATH, resource)




if __name__ == '__main__':
    print("dash_app running on port 8050")
    #app.run_server(debug=True, host='0.0.0.0')
    app.run_server(host='0.0.0.0')
