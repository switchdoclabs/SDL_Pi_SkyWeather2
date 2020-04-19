from __future__ import division
from __future__ import print_function

#
# wired sensor routines


from past.utils import old_div
import config


import sys

import datetime
import traceback
import state
import buildJSON

def readWiredSensors(bmp280, hdc1080):

    # read wired sensors


    if (config.BMP280_Present):	
        try:
            state.currentBarometricTemperature = round(bmp280.get_temperature(), 2)
            state.currentBarometricPressure = round(old_div(bmp280.get_pressure(),1000)*100, 5)
            state.currentAltitude = round(bmp280.get_altitude(), 4)
            state.currentSeaLevel = round(old_div(bmp280.get_sealevel_pressure(config.BMP280_Altitude_Meters),1000)*100, 5)
        except:
            if (config.SWDEBUG):
                print(traceback.format_exc()) 
                print(("readWiredSensors Unexpected error:", sys.exc_info()[0]))

    print("Looking for buildJSONSemaphore Acquire")
    state.buildJSONSemaphore.acquire()
    print("buildJSONSemaphore Acquired")
    state.currentStateJSON = buildJSON.getStateJSON()
    #if (config.SWDEBUG):
    #    print("currentJSON = ", state.currentStateJSON)
    state.buildJSONSemaphore.release()
    print("buildJSONSemaphore Released")



