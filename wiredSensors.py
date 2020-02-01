from __future__ import division
from __future__ import print_function

#
# wired sensor routines


from past.utils import old_div
try:
	import conflocal as config
except ImportError:
	import config


import sys

import datetime
import traceback
import state

def readWiredSensors(bmp280, hdc1080):

    # read wired sensors


    if (config.BMP280_Present):	
        try:
            state.currentBarometricTemperature = round(bmp280.read_temperature(), 2)
            state.currentBarometricPressure = round(old_div(bmp280.read_pressure(),1000), 4)
            state.currentAltitude = round(bmp280.read_altitude(), 4)
            state.currentSeaLevel = bmp280.read_sealevel_pressure(config.BMP280_Altitude_Meters)
            state.currentSeaLevel = round(old_div(bmp280.read_sealevel_pressure(config.BMP280_Altitude_Meters),1000), 4)
        except:
            if (config.SWDEBUG):
                print(traceback.format_exc()) 
                print(("Unexpected error:", sys.exc_info()[0]))



