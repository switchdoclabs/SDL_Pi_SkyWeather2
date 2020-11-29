# test for WeatherSense SwitchDoc Labs Weather Sensors
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
#import json
import datetime

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# 146 = FT-020T WeatherRack2, #147 = F016TH SDL Temperature/Humidity Sensor
print("Starting Wireless Read")
#cmd = [ '/usr/local/bin/rtl_433', '-vv',  '-q', '-F', 'json', '-R', '146', '-R', '147']
cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R', '147']

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        print(sLine)
        #   See if the data is something we need to act on...
        if (( sLine.find('F007TH') != -1) or ( sLine.find('F016TH') != -1)):
            sys.stdout.write('WeatherSense Indoor T/H F016TH Found' + '\n')
            sys.stdout.write('This is the raw data: ' + sLine + '\n')
        if (( sLine.find('FT0300') != -1) or ( sLine.find('FT020T') != -1)):
            sys.stdout.write('WeatherSense WeatherRack2 FT020T found' + '\n')
            sys.stdout.write('This is the raw data: ' + sLine + '\n')


    sys.stdout.flush()

