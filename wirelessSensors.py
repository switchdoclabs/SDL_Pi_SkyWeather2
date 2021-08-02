#
# wireless sensor routines

import util
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
import indoorTH
import pclogging

import time
import os
import signal
import traceback
sys.path.append('./SDP_Pi_HM3301/aqi')
import aqi

import MySQLdb as mdb
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

#cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R', '147']
cmd = ['/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R', '147', '-R', '148', '-R', '150', '-R', '151', '-R', '152']


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

ThreadStop = False;

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
    try:
        for line in iter(out.readline, b''):
            queue.put(( src, line))
        out.close()
    except:
       pass 

def randomadd(value, spread):

    return round(value+random.uniform(-spread, spread),2)


# MQTT Publish Line
def mqtt_publish_single(message, topic):
    topic = '{0}/{1}'.format("skyweather2", topic)
    #print ("topic=", topic)
    try:
            state.mqtt_client.publish(topic, message)
    except:
        traceback.print_exc()
        print('Mosquitto not available')



# process functions

def processFT020T(sLine, lastFT020TTimeStamp ):

    if (config.SWDEBUG):
        sys.stdout.write("processing FT020T Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    var = json.loads(sLine)
    if (lastFT020TTimeStamp == var["time"]):
        # duplicate
        if (config.SWDEBUG):
            sys.stdout.write("duplicate found\n")

        return ""

    lastFT020TTimeStamp = var["time"]

    if (config.MQTT_Enable == True):
        mqtt_publish_single(sLine, "FT020T")

    # now check for adding record


    # outside temperature and Humidity

    state.mainID = var["id"] 
    state.lastMainReading = nowStr()


    if (state.previousMainReading == "Never"):
        pclogging.systemlog(config.INFO,"Main Weather Sensors Found")
        print("Main Weather Sensors Found")
        pclogging.systemlog(config.INFO,"Blynk Updates Started")
        state.previousMainReading = state.lastMainReading



    wTemp = var["temperature"]

    ucHumi = var["humidity"]


    wTemp = (wTemp - 400)/10.0
    # deal with error condtions
    if (wTemp > 140.0):
        # error condition from sensor
        if (config.SWDEBUG):
            sys.stdout.write("error--->>> Temperature reading from FT020T\n")
            sys.stdout.write('This is the raw temperature: ' + str(wTemp) + '\n')
        # put in previous temperature 
        wtemp = state.OutdoorTemperature 
    #print("wTemp=%s %s", (str(wTemp),nowStr() ));
    if (ucHumi > 100.0):
        # bad humidity
        # put in previous humidity
        ucHumi  = state.OutdoorHumidity
     
    state.OutdoorTemperature = round(((wTemp - 32.0)/(9.0/5.0)),2)
    state.OutdoorHumidity =  ucHumi 

    
        
    state.WindSpeed =  round(var["avewindspeed"]/10.0, 1)
    state.WindGust  = round(var["gustwindspeed"]/10.0, 1)
    state.WindDirection  = var["winddirection"]
    


    state.TotalRain  = round(var["cumulativerain"]/10.0,1)

    wLight = var["light"]
    if (wLight >= 0x1fffa):
        wLight = wLight | 0x7fff0000

    wUVI =var["uv"]
    if (wUVI >= 0xfa):
        wUVI = wUVI | 0x7f00

    state.SunlightVisible =  wLight 
    state.SunlightUVIndex  = round(wUVI/10.0, 1 )

    if (var['batterylow'] == 0):
        state.BatteryOK = "OK"
    else:
        state.BatteryOK = "LOW"

    #print("looking for buildJSONSemaphore acquire")
    state.buildJSONSemaphore.acquire()
    #print("buildJSONSemaphore acquired")
    state.StateJSON = buildJSON.getStateJSON()
    #if (config.SWDEBUG):
    #    print("currentJSON = ", state.StateJSON)
    state.buildJSONSemaphore.release()
    #print("buildJSONSemaphore released")
    return lastFT020TTimeStamp


# processes Inside Temperature and Humidity
def processF016TH(sLine):
    if (config.SWDEBUG):
        sys.stdout.write('Processing F016TH data'+'\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
    
    var = json.loads(sLine)
    
    IT = round(((var["temperature_F"] - 32.0)/(9.0/5.0)),2)

    # check for bad read (not caught by checksum for some reason)
    # may be related to low battery
    if ((IT > 100.00) or (IT < -35)):
        # bad temperatures / Humidity
        #skip read
        return

    state.mainID = var["device"] + var["channel"]
    state.lastIndoorReading = nowStr()

    if (config.MQTT_Enable == True):
        mqtt_publish_single(sLine, "F016TH")



    if (state.previousIndoorReading == "Never"):
        pclogging.systemlog(config.INFO,"Indoor Weather Sensor Found")
        print("Indoor Weather Sensors Found")
        state.previousIndoorReading = state.lastIndoorReading

    state.IndoorTemperature = IT 
    state.IndoorHumidity = var["humidity"]
    state.lastIndoorReading = var["time"]
    state.insideID = var["channel"]



    indoorTH.addITReading(var["device"], var["channel"], state.IndoorTemperature, var["humidity"], var["battery"],  var["time"])

    #print("looking for buildJSONSemaphore acquire")
    state.buildJSONSemaphore.acquire()
    #print("buildJSONSemaphore acquired")
    state.StateJSON = buildJSON.getStateJSON()
    #if (config.SWDEBUG):
    #   print("currentJSON = ", state.StateJSON)
    #   pass
    state.buildJSONSemaphore.release()
    #print("buildJSONSemaphore released")





# processes Generic Packets 
def processWeatherSenseGeneric(sLine):
    if (config.MQTT_Enable == True):
        mqtt_publish_single(sLine, "Generic")
    if (config.SWDEBUG):
        sys.stdout.write('Processing Generic data'+'\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    return


def processWeatherSenseTB(sLine):
    # weathersense protocol 16
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']

    if (config.SWDEBUG):
        sys.stdout.write('Processing WeatherSense Lightning data'+'\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.MQTT_Enable == True):
        mqtt_publish_single(sLine, "WSLightning")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                "localhost",
                "root",
                config.MySQL_Password,
                "WeatherSenseWireless"
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])/1000.0
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])/1000.0
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])/1000.0
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2) 

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol,irqsource, previousinterruptresult, lightninglastdistance, sparebyte, lightningcount, interruptcount,  batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d, %d, %d, %d,%d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['irqsource'], state['previousinterruptresult'], state['lightninglastdistance'], state['sparebyte'],
            state['lightningcount'], state['interruptcount'],
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO TB433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return


def processWeatherSenseAQI(sLine):
    # weathersense protocol 15
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']

    if (config.SWDEBUG):
        sys.stdout.write('Processing WeatherSense Air Quality data'+'\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.MQTT_Enable == True):
        mqtt_publish_single(sLine, "WSAQI")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                "localhost",
                "root",
                config.MySQL_Password,
                "WeatherSenseWireless"
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])/1000.0
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])/1000.0
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])/1000.0
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)
 
            # calculate AQI 24 Hour
            timeDelta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            before = now - timeDelta
            before = before.strftime('%Y-%m-%d %H:%M:%S')
            query = "SELECT AQI, TimeStamp FROM AQI433MHZ WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

            cur.execute(query)
            myAQIRecords = cur.fetchall()
            myAQITotal = 0.0
            if (len(myAQIRecords) > 0):
                for i in range(0, len(myAQIRecords)):
                    myAQITotal = myAQITotal + myAQIRecords[i][0]

                AQI24Hour = (myAQITotal + float(state['AQI'])) / (len(myAQIRecords) + 1)
            else:
                AQI24Hour = 0.0


            # HOTFIX for AQI problem from the wireless AQI sensor
            # recalculate AQI from RAW values and write in database

            myaqi = aqi.to_aqi([
                (aqi.POLLUTANT_PM25, state['PM2.5A']),
                (aqi.POLLUTANT_PM10, state['PM10A'])
                ])
            if (myaqi > 500):
                myaqi = 500
            print("myaqi=", myaqi)
            state['AQI'] = myaqi

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, PM1_0S, PM2_5S, PM10S, PM1_0A, PM2_5A, PM10A, AQI, AQI24Hour, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d, %d, %d, %d, %d,%d, %d, %6.2f,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['PM1.0S'], state['PM2.5S'], state['PM10S'], state['PM1.0A'], state['PM2.5A'], state['PM10S'],
            state['AQI'], AQI24Hour,
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO AQI433MHZ (%s) VALUES(%s )" % (fields, values)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return

def WSread_AQI():
    #read AQI from WeatherSense

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            con = mdb.connect(
                "localhost",
                "root",
                config.MySQL_Password,
                "WeatherSenseWireless"
            )
            cur = con.cursor()

            query = "SELECT timestamp, AQI, AQI24Hour FROM AQI433MHZ ORDER BY timestamp DESC LIMIT 1;"
            cur.execute(query)
            
            myAQIRecords = cur.fetchall()
            if (len(myAQIRecords) > 0):
                state.WS_AQI = myAQIRecords[0][1]
                state.WS_Hour24_AQI = myAQIRecords[0][2]
            else:
                state.WS_AQI =  0.0
                state.WS_Hour24_AQI = 0.0 

        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            # sys.exit(1)


    return


def processSolarMAX(sLine):
    myState = json.loads(sLine)

    if (config.SWDEBUG):
        sys.stdout.write('Processing SolarMAX2 data'+'\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    # only accept SolarMAX2 Protocols (8,10,11)
    myProtocol = myState['weathersenseprotocol']
    if ((myProtocol == 8) or (myProtocol == 10) or (myProtocol == 11)):

        if (config.MQTT_Enable == True):
            mqtt_publish_single(sLine, "WSSolarMAX")

        if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
                myTEST = ""
                myTESTDescription = ""

                con = mdb.connect(
                    "localhost",
                    "root",
                    config.MySQL_Password,
                    "WeatherSenseWireless"
                )

                cur = con.cursor()
                batteryPower =  float(myState["batterycurrent"])* float(myState["batteryvoltage"])/1000.0
                loadPower  =  float(myState["loadcurrent"])* float(myState["loadvoltage"])/1000.0
                solarPower =  float(myState["solarpanelcurrent"])* float(myState["solarpanelvoltage"])/1000.0
                batteryCharge = util.returnPercentLeftInBattery(myState["batteryvoltage"], 4.2)

                fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, internaltemperature,internalhumidity, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
                values = "%d, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
                myState["deviceid"], myState["protocolversion"], myState["softwareversion"], myState["weathersenseprotocol"],
                myState["batteryvoltage"], myState["batterycurrent"], myState["loadvoltage"], myState["loadcurrent"],
                myState["solarpanelvoltage"], myState["solarpanelcurrent"], myState["auxa"], myState["internaltemperature"],
                myState["internalhumidity"], batteryCharge, myState["messageid"], batteryPower, loadPower, solarPower,
                myTEST, myTESTDescription)
                query = "INSERT INTO SolarMax433MHZ (%s) VALUES(%s )" % (fields, values)
                cur.execute(query)
                con.commit()
                
                # update state values 
                state.batteryVoltage = float(myState["batteryvoltage"])
                state.batteryCurrent = float(myState["batterycurrent"])
                state.solarVoltage = float(myState["solarpanelvoltage"])
                state.solarCurrent = float(myState["solarpanelcurrent"])
                state.loadVoltage = float(myState["loadvoltage"])
                state.loadCurrent = float(myState["loadcurrent"])
                state.batteryPower = batteryPower 
                state.solarPower = solarPower
                state.loadPower = loadPower
                state.batteryCharge = batteryCharge
                state.SolarMaxInsideTemperature = float(myState["internaltemperature"])
                state.SolarMaxInsideHumidity = float(myState["internalhumidity"]) 
                state.SolarMAXLastReceived = myState["time"] 



            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)

            finally:
                cur.close()
                con.close()

                del cur
                del con

    return


# processes AfterShock Packets 
def processWeatherSenseAfterShock(sLine):

    # weathersense protocol 18
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing AfterShock Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.MQTT_Enable == True):
        mqtt_publish_single(sLine, "WSAfterShock")


    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                    "localhost",
                    "root",
                    config.MySQL_Password,
                    "WeatherSenseWireless"
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, eqcount, finaleq_si, finaleq_pga, instanteq_si, instanteq_pga, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, solarpresent, aftershockpresent, keepalivemessage, lowbattery, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f, %d, %d, %d, %d,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['eqcount'], state['finaleq_si'], state['finaleq_pga'], state['instanteq_si'],
            state['instanteq_pga'], 
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],state["solarpresent"],state["aftershockpresent"],state["keepalivemessage"],state["lowbattery"],     batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO AS433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return




# main read 433HMz Sensor Loop
def readSensors():


    print("")
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
    # last timestamp for FT020T to remove duplicates
    lastFT020TTimeStamp = ""
    FT020Count = 0
    lastTimeSensorReceived = time.time()

    while True:
        #   Other processing can occur here as needed...
        #sys.stdout.write('Made it to processing step. \n')
        timeSinceLastSample = time.time() - lastTimeSensorReceived
       
        if (timeSinceLastSample > 720.0):   # restart if no reads in 12 minutes
        
            if (config.SWDEBUG):
                print(">>>>>>>>>>>>>>restarting SDR thread.....")
            lastTimeSensorReceived = time.time()
            if (config.SWDEBUG):
                print( "Killing SDR Thread")
            p.kill()
            t.join()
            pclogging.systemlog(config.INFO,"SDR Restarted")
            if (config.SWDEBUG):
                print("starting SDR Thread again")

                print("")
                print("######")
                print("Read Wireless Sensors")
                print("######")
            p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
            q = Queue()

            t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))
    
            t.daemon = True # thread dies with the program
            t.start()


        try:
            src, line = q.get(timeout = 1)
            #print(line.decode())
        except Empty:
            pulse += 1
        else: # got line
            pulse -= 1
            sLine = line.decode()
            lastTimeSensorReceived = time.time()
    
            #   See if the data is something we need to act on...

            if ( sLine.find('F007TH') != -1) or ( sLine.find('FT0300') != -1) or ( sLine.find('F016TH') != -1) or ( sLine.find('FT020T') != -1):
                
                if (( sLine.find('F007TH') != -1) or ( sLine.find('F016TH') != -1)): 
                    processF016TH(sLine)
                if (( sLine.find('FT0300') != -1) or ( sLine.find('FT020T') != -1)): 
                    lastFT020TTimeStamp = processFT020T(sLine, lastFT020TTimeStamp)
            if (sLine.find('SolarMAX') != -1):
                processSolarMAX(sLine)

            if (sLine.find('AQI') != -1):
                processWeatherSenseAQI(sLine)

            if (sLine.find('TB') != -1):
                processWeatherSenseTB(sLine)

            if (sLine.find('Generic') != -1):
                processWeatherSenseGeneric(sLine)

            if (sLine.find('AfterShock') != -1):
                processWeatherSenseAfterShock(sLine)


        sys.stdout.flush()

