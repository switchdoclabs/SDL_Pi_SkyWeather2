

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
# 
################




################
# Page Functions
################

def NotImplPage():
    Row1 = html.Div(
        [ 
         
            dbc.Row(
                [
                    html.H1(children="Page Not Implemented")
                ]
            ),
        ]
    )
    
    layout = dbc.Container([
        Row1],
        className="ni",
    )
    return layout







