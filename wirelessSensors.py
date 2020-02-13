#
# wireless sensor routines


try:
	import conflocal as config
except ImportError:
	import config

import json
import random

import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
#import json
import datetime

import state

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '20']

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
        #sys.stdout.write('This is the raw data: ' + sLine + '\n')

    # now do random bouncing around on reasonable values


    state.currentOutsideTemperature = randomadd(10.0, 10.0)
    state.currentOutsideHumidity =  randomadd(40.0, 10.0)


    state.currentRain60Minutes = randomadd(10.0, 10.0)

    state.currentSunlightVisible =  randomadd(4000.0, 10.0)
    state.currentSunlightIR = randomadd(200.0, 10.0)
    state.currentSunlightUV = randomadd(300.0, 10.0)
    state.currentSunlightUVIndex  = randomadd(5.0, 10.0)

    state.ScurrentWindSpeed = randomadd(10.0, 10.0)
    state.ScurrentWindGust  = randomadd(30.0, 10.0)
    state.ScurrentWindDirection  = randomadd(330.0, 10.0)
    state.currentTotalRain  = randomadd(10.0, 10.0)




# processes Inside Temperature and Humidity
def processF007THData(sLine):
    if (config.SWDEBUG):
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
    
    var = json.loads(sLine)


    state.currentInsideTemperature = round(((var["temperature_F"] - 32.0)/(9.0/5.0)),2)
    state.currentInsideHumidity = var["humidity"]
    state.lastInsideReading = var["time"]
    state.insideID = var["channel"]
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
            if ( sLine.find('F007TH') != -1):
                processF007THData(sLine)
                processF300Data(sLine)

        sys.stdout.flush()

