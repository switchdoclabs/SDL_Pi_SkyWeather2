#
# wireless sensor routines


import config

import json
import random

import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
#import json
import datetime
import buildJSON

import state

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R', '147']

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

#stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)


#   We're using a queue to capture output as it occurs
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put(( src, line))
    out.close()

def randomadd(value, spread):

    return round(value+random.uniform(-spread, spread),2)


# process functions

def processF300Data(sLine):

    if (config.SWDEBUG):
        sys.stdout.write("processing F300 Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    var = json.loads(sLine)

    # outside temperature and Humidity

    state.mainID = var["id"] 
    state.lastMainReading = nowStr()
    wTemp = var["temperature"]

    ucHumi = var["humidity"]


    wTemp = (wTemp - 400)/10.0
    # deal with error condtions
    if (wTemp > 140.0):
        # error condition from sensor
        if (config.SWDEBUG):
            sys.stdout.write("error--->>> Temperature reading from F300\n")
            sys.stdout.write('This is the raw temperature: ' + str(wTemp) + '\n')
        # put in previous temperature 
        wtemp = state.currentOutsideTemperature 
    print("wTemp=%s %s", (str(wTemp),nowStr() ));
    if (ucHumi > 100.0):
        # bad humidity
        # put in previous humidity
        ucHumi  = state.currentOutsideHumidity
     
    state.currentOutsideTemperature = round(((wTemp - 32.0)/(9.0/5.0)),2)
    state.currentOutsideHumidity =  ucHumi 

    
        
    state.ScurrentWindSpeed =  round(var["avewindspeed"]/10.0, 1)
    state.ScurrentWindGust  = round(var["gustwindspeed"]/10.0, 1)
    state.ScurrentWindDirection  = var["winddirection"]
    


    state.currentTotalRain  = round(var["cumulativerain"]/10.0,1)
    state.currentRain60Minutes = 0.0

    wLight = var["light"]
    if (wLight >= 0x1fffa):
        wLight = wLight | 0x7fff0000

    wUVI =var["uv"]
    if (wUVI >= 0xfa):
        wUVI = wUVI | 0x7f00

    state.currentSunlightVisible =  wLight 
    state.currentSunlightIR =  0
    state.currentSunlightUV = 0 
    state.currentSunlightUVIndex  = round(wUVI/10.0, 1 )



    print("looking for buildJSONSemaphore acquire")
    state.buildJSONSemaphore.acquire()
    print("buildJSONSemaphore acquired")
    state.currentStateJSON = buildJSON.getStateJSON()
    #if (config.SWDEBUG):
    #    print("currentJSON = ", state.currentStateJSON)
    state.buildJSONSemaphore.release()
    print("buildJSONSemaphore released")



# processes Inside Temperature and Humidity
def processF007THData(sLine):
    if (config.SWDEBUG):
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
    
    var = json.loads(sLine)

    state.mainID = var["device"] + var["channel"]
    state.lastInsideReading = nowStr()

    state.currentInsideTemperature = round(((var["temperature_F"] - 32.0)/(9.0/5.0)),2)
    state.currentInsideHumidity = var["humidity"]
    state.lastInsideReading = var["time"]
    state.insideID = var["channel"]

    print("looking for buildJSONSemaphore acquire")
    state.buildJSONSemaphore.acquire()
    print("buildJSONSemaphore acquired")
    state.currentStateJSON = buildJSON.getStateJSON()
    #if (config.SWDEBUG):
    #    print("currentJSON = ", state.currentStateJSON)
    state.buildJSONSemaphore.release()
    print("buildJSONSemaphore released")

# main read 433HMz Sensor Loop
def readSensors():


    print("")
    print("######")
    print("Read Wireless Sensors")
    print("######")
    #   Create our sub-process...
    #   Note that we need to either ignore output from STDERR or merge it with STDOUT due to a limitation/bug somewhere under the covers of "subprocess"
    #   > this took awhile to figure out a reliable approach for handling it...

    p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
    q = Queue()

    t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))
    
    t.daemon = True # thread dies with the program
    t.start()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    pulse = 0
    print("starting 433MHz scanning")
    print("######")

    while True:
        #   Other processing can occur here as needed...
        #sys.stdout.write('Made it to processing step. \n')



        try:
            src, line = q.get(timeout = 1)
            #print(line.decode())
        except Empty:
            pulse += 1
        else: # got line
            pulse -= 1
            sLine = line.decode()
            #   See if the data is something we need to act on...
            if ( sLine.find('F007TH') != -1) or ( sLine.find('FT0300') != -1):
                
                if ( sLine.find('F007TH') != -1): 
                    processF007THData(sLine)
                if ( sLine.find('FT0300') != -1): 
                    processF300Data(sLine)

        sys.stdout.flush()

