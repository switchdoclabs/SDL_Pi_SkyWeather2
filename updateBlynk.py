from __future__ import print_function

# provides routine to update SGS Blynk Display
import time
import requests
import json
import util
import state
import traceback
# Check for user imports
import config


DEBUGBLYNK = False 
def stopFlash():
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V30?value=0')

def blynkInit():
    # initalize button states
    try:
        if (DEBUGBLYNK):
            print("Entering blynkInit:")

        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V5?value=0')
        if (state.runOLED == True):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V6?value=1')
        else:        
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V6?value=0')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V30?value=0')
        # initialize LEDs
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V42?value=255')
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V43?value=255')

        if (DEBUGBLYNK):
            print("config.English_Metric = ", config.English_Metric)
        if (config.English_Metric == 0):
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V8?value=0')
        else:        
            r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V8?value=1')

        if (DEBUGBLYNK):
            print("Exiting blynkInit:")

    except Exception as e:
        print("exception in blynkInit")
        print (e)
        return 0

def blynkResetButton(buttonNumber):
    try:
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/'+buttonNumber+'?value=0')
    except Exception as e:
        print("exception in blynkResetButton")
        print (e)
        return 0

def blynkEventUpdate(Event):
    try:
        put_header={"Content-Type": "application/json"}
        val = Event 
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
          print("blynkEventUpdate:",val)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V31', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkEventUpdate:POST:r.status_code:",r.status_code)
        return 1
    except Exception as e:
        print("exception in blynkEventUpdate")
        print (e)
        return 0

def blynkTerminalUpdate(entry):
    try:
        put_header={"Content-Type": "application/json"}

        entry = time.strftime("%Y-%m-%d %H:%M:%S")+": "+entry+"\n"
        put_body = json.dumps([entry])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V32', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POST:r.status_code:",r.status_code)
    except Exception as e:
        print("exception in blynkTerminalUpdate")
        print (e)
        return 0


def blynkSolarMAXLine(entry):
    try:
        put_header={"Content-Type": "application/json"}

        put_body = json.dumps([entry])
        if (DEBUGBLYNK):
            print("blynkSolarMAXUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V75', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkSolarMAXUpdate:POST:r.status_code:",r.status_code)
    except Exception as e:
        print("exception in blynkSolarMAXUpdate")
        print (e)
        return 0
    
def blynkSolarTerminalUpdate(entry):
    try:
        put_header={"Content-Type": "application/json"}
        entry = time.strftime("%Y-%m-%d %H:%M:%S")+": "+entry+"\n"

        put_body = json.dumps([entry])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V33', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POST:r.status_code:",r.status_code)
    except Exception as e:
        print("exception in blynkTerminalUpdate")
        print (e)
        return 0
    

def blynkUpdateImage():
    #Blynk.setProperty(V1, "urls", "https://image1.jpg", "https://image2.jpg");

    try:
        if (DEBUGBLYNK):
             print("blynkUpdateImage:started")
        """
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?value=2') # Picture URL
        if (DEBUGBLYNK):
             print "blynkUpdateImage:OTHER:r.status_code:",r.status_code
        #r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?urls=http://www.switchdoc.com/2.jpg') # Picture URL
        #r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?urls=http://www.switchdoc.com/skycamera.jpg,http://www.switchdoc.com/2.jpg') # Picture URL
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?value=1;url=http://www.switchdoc.com/skycamera.jpg')
        if (DEBUGBLYNK):
             print "blynkUpdateImage:OTHER:r.status_code:",r.status_code
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?value=2;url=http://www.switchdoc.com/2.jpg') # Picture URL
        if (DEBUGBLYNK):
             print "blynkUpdateImage:OTHER:r.status_code:",r.status_code

        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?value=2') # Picture URL
        if (DEBUGBLYNK):
             print "blynkUpdateImage:OTHER:r.status_code:",r.status_code
        """
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V70?urls=http://www.switchdoc.com/SkyWeatherNoAlpha.png') # Picture URL

    except Exception as e:
        print("exception in blynkUpdateImage")
        print (e)
        return 0


def blynkStateUpdate():

    try:
     # do not blynk if no main reading yet
     if (state.lastMainReading != "Never"):
        
        blynkUpdateImage()
        
        put_header={"Content-Type": "application/json"}

        # set last sample time 
        
        put_header={"Content-Type": "application/json"}
        val = time.strftime("%Y-%m-%d %H:%M:%S")  
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
          print("blynkEventUpdate:",val)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V44', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkEventUpdate:POST:r.status_code:",r.status_code)

        # do the graphs


        if (config.USEWSAQI):
            val = state.WS_AQI
        else:
            val = state.AQI 
        put_body = json.dumps([val])
        if (DEBUGBLYNK):
            print("blynkStateUpdate:Pre:put_body:",put_body)
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V7', data=put_body, headers=put_header)
        if (DEBUGBLYNK):
            print("blynkStateUpdate:POST:r.status_code:",r.status_code)
    

        val = util.returnTemperatureCF(state.OutdoorTemperature)
        tval = "{0:0.1f} ".format(val) + util.returnTemperatureCFUnit()
        put_body = json.dumps([tval])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V0', data=put_body, headers=put_header)

        val = util.returnTemperatureCF(state.OutdoorTemperature)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V10', data=put_body, headers=put_header)

        val = state.OutdoorHumidity 
        put_body = json.dumps(["{0:0.1f}%".format(val)])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V1', data=put_body, headers=put_header)

        val = state.OutdoorHumidity 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V11', data=put_body, headers=put_header)

        val = util.returnTemperatureCF(state.IndoorTemperature)
        tval = "{0:0.1f} ".format(val) + util.returnTemperatureCFUnit()
        put_body = json.dumps([tval])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V21', data=put_body, headers=put_header)

        val = util.returnTemperatureCF(state.IndoorTemperature)
        tval = "{0:0.1f}".format(val) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V120', data=put_body, headers=put_header)

        val = state.IndoorHumidity 
        put_body = json.dumps(["{0:0.1f}%".format(val)])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V13', data=put_body, headers=put_header)

        val = state.IndoorHumidity 
        put_body = json.dumps(["{0:0.1f}".format(val)])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V121', data=put_body, headers=put_header)

        if (state.fanState == False):
            val = 0
        else:
            val = 1
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V122', data=put_body, headers=put_header)


        #wind
        val = util.returnWindSpeed(state.WindSpeed)
        tval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
        put_body = json.dumps([tval])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V9', data=put_body, headers=put_header)

        #now humiidyt
        #val = util.returnWindSpeed(state.WindSpeed)
        val = state.OutdoorHumidity
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V19', data=put_body, headers=put_header)

        # outdoor Air Quality
        if (config.USEWSAQI):
            val = state.WS_AQI
        else:
            val = state.AQI 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V20', data=put_body, headers=put_header)
        
        #wind direction
        val = "{0:0.0f}/".format(state.WindDirection) + util.returnWindDirection(state.WindDirection)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V2', data=put_body, headers=put_header)

        #rain 
        val = "{0:0.2f}".format(state.TotalRain) 
        if (config.English_Metric == 1):
            tval = "{0:0.2f}mm".format(state.TotalRain) 
        else:
            tval = "{0:0.2f}in".format(state.TotalRain / 25.4) 
        put_body = json.dumps([tval])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V3', data=put_body, headers=put_header)

        #Sunlight 
        val = "{0:0.0f}".format(state.SunlightVisible) 
        #print ("Sunlight Val = ", state.SunlightVisible)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V4', data=put_body, headers=put_header)

        #Sunlight  for Graph
        val = "{0:0.0f}".format(state.SunlightVisible) 
        #print ("Sunlight Val = ", state.SunlightVisible)
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V130', data=put_body, headers=put_header)

        #barometric Pressure 
        if (config.English_Metric == 1):
            tval = "{0:0.2f}hPa".format(state.BarometricPressureSeaLevel*10.0)
        else:
            tval = "{0:0.2f}in".format((state.BarometricPressureSeaLevel * 0.2953)) 
        put_body = json.dumps([tval])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V40', data=put_body, headers=put_header)

        #barometric Pressure graph
        if (config.English_Metric == 1):
            tval = "{0:0.2f}".format(state.BarometricPressureSeaLevel) 
        else:
            tval = "{0:0.2f}".format((state.BarometricPressureSeaLevel * 0.2953)) 
        put_body = json.dumps([tval])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V41', data=put_body, headers=put_header)

        #solar data

        val = "{0:0.2f}".format(state.solarVoltage) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V50', data=put_body, headers=put_header)

        val = "{0:0.1f}".format(state.solarCurrent) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V51', data=put_body, headers=put_header)

        val = "{0:0.2f}".format(state.batteryVoltage) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V52', data=put_body, headers=put_header)

        val = "{0:0.1f}".format(state.batteryCurrent) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V53', data=put_body, headers=put_header)

        val = "{0:0.2f}".format(state.loadVoltage) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V54', data=put_body, headers=put_header)

        val = "{0:0.1f}".format(state.loadCurrent) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V55', data=put_body, headers=put_header)

        val = "{0:0.1f}W".format(state.batteryPower) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V60', data=put_body, headers=put_header)
        
        val = "{0:0.1f}W".format(state.solarPower) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V61', data=put_body, headers=put_header)
        
        val = "{0:0.1f}W".format(state.loadPower) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V62', data=put_body, headers=put_header)


        
        if (config.SolarMAX_Present == True):
            
            blynkSolarMAXLine(state.SolarMAXLastReceived)
            if (state.SolarMAXLastReceived != "Never"): 
                val = util.returnTemperatureCF(state.SolarMaxInsideTemperature)
                tval = "{0:0.1f} ".format(val) + util.returnTemperatureCFUnit()
                put_body = json.dumps([tval])
                r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V76', data=put_body, headers=put_header)

                val = "{0:0.1f}%".format(state.SolarMaxInsideHumidity) 
                put_body = json.dumps([val])
                r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V77', data=put_body, headers=put_header)

        
        
        val = "{0:0.1f}".format(state.batteryCharge) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V56', data=put_body, headers=put_header)
        
        val = "{0:0.1f}".format(state.batteryCharge) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V127', data=put_body, headers=put_header)
        
        delta = util.returnTemperatureCF(state.IndoorTemperature)- util.returnTemperatureCF(state.OutdoorTemperature)
        
        val = "{0:0.1f}".format(delta) 
        put_body = json.dumps([val])
        r = requests.put(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V128', data=put_body, headers=put_header)
        
        
        # LEDs 


        if (state.barometricTrend):   #True is up, False is down
                        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V42?color=%2300FF00') # Green
                        if (DEBUGBLYNK):
                            print("blynkAlarmUpdate:OTHER:r.status_code:",r.status_code)
        else:
                        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/update/V42?color=%23FF0000') # red



        return 1
    except Exception as e:
        print("exception in blynkStateUpdate")
        print(traceback.format_exc())
        print (e)
        return 0

def blynkStatusUpdate():

    if (DEBUGBLYNK):
        print("blynkStatusUpdate Entry")
    try:
        put_header={"Content-Type": "application/json"}

        # look for English or Metric 
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V8') # read button state
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:POSTEM:r.status_code:",r.status_code)
            print("blynkStatusUpdate:POSTEM:r.text:",r.text)
    
        if (r.text == '["1"]'):
            if (config.English_Metric == 0):
                config.English_Metric = 1
                if (DEBUGBLYNK):
                    print("blynkStatusUpdate:POSTBRC:config.English_Metric set to Metric")
                blynkTerminalUpdate("Set to Metric Units ")
                f = open("/home/pi/SDL_Pi_SkyWeather/config.English_Metric.txt", "w")
                f.write("1")
                f.close()
        else:

            if (config.English_Metric == 1):
                config.English_Metric = 0
                f = open("/home/pi/SDL_Pi_SkyWeather/config.English_Metric.txt", "w")
                f.write("0")
                f.close()
                if (DEBUGBLYNK):
                    print("blynkStatusUpdate:POSTBRC:config.English_Metric set to English")
                blynkTerminalUpdate("Set to English Units ")


        # look for rainbow button change
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V5') # read button state
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:POSTBR:r.status_code:",r.status_code)
            print("blynkStatusUpdate:POSTBR:r.text:",r.text)
    
        if (r.text == '["1"]'):
            state.runRainbow = True
            blynkTerminalUpdate("Turning Rainbow On ")
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.runRainbow set to True")
        else:
            if(state.runRainbow == True):
                blynkTerminalUpdate("Turning Rainbow Off ")
            state.runRainbow = False
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRC:state.runRainbow set to False")

                
        # turn OLED ON and OFF 
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V6') # read button state
        #if (DEBUGBLYNK):
    
        if (r.text == '["1"]'):
            if (state.runOLED == False):
                state.runOLED = True
                blynkTerminalUpdate("Turning OLED On ")
                if (DEBUGBLYNK):
                    print("blynkStatusUpdate:POSTBRO:state.runOLED set to True")

                if (config.OLED_Originally_Present == True):
                    config.OLED_Present = True 
                    util.turnOLEDOn()
        else:
            if (state.runOLED == True):
                blynkTerminalUpdate("Turning OLED Off ")
                state.runOLED = False
                
                if (DEBUGBLYNK):
                    print("blynkStatusUpdate:POSTBRO:state.runOLED set to False")
                if (config.OLED_Originally_Present == True):
                    config.OLED_Present = False 
                    util.turnOLEDOff()

        # look for Flash Strip Command
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/get/V30') # read button state
        if (DEBUGBLYNK):
            print("blynkStatusUpdate:POSTBF:r.status_code:",r.status_code)
            print("blynkStatusUpdate:POSTBF:r.text:",r.text)
   
        
        if (r.text == '["1"]'):
            state.flashStrip = True
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRF:state.flashStrip set to True")
        else:
            state.flashStrip = False
            if (DEBUGBLYNK):
                print("blynkStatusUpdate:POSTBRF:state.flashStrip set to False")




        


        return 1
    except Exception as e:
        print("exception in blynkStatusUpdate")
        print (e)
        return 0


        
def blynkSGSAppOnline():

    try:
        r = requests.get(config.BLYNK_URL+config.BLYNK_AUTH+'/isAppConnected')
        if (DEBUGBLYNK):
            print("blynkSGSAppOnline:POSTCHECK:r.text:",r.text)
        return r.text
    except Exception as e:
        print("exception in blynkApponline")
        print (e)
        return ""

   
