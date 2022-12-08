
#
# tests SkyCam Remote and the updates parameters
#
import json
import paho.mqtt.client as mqtt
import os
import socket
import requests
import ipaddress
import subprocess
import traceback
import datetime

import config

# start scan for SkyCam Remotes - This will take a long time
# 2 minutes * 253 addresses

def sendCommandToWireless(myIP, myCommand):
        myURL = 'http://'+str(myIP)+'/'+myCommand
        returnJSON = {}
        for i in range(0,45):  # 3 minute per IP Scan
            try:
                #if (config.SWDEBUG):
                #    print("myURL=", myURL)
                req = requests.get(myURL,timeout=3)
                #print("req.text=", req.text)
                reqtext = req.text
                if (reqtext.find("401 Unau") != -1):
                    #print("401 found:")
                    break
                if (reqtext.find("404 Not") != -1):
                    #print("404 found:")
                    break
                #print("req.json()=", req.json())
                try:
                    returnJSON = req.json()
                    #print("returnJSON=", returnJSON)
                    break
                except:
                    #traceback.print_exc()
                    returnJSON = {}

            except Exception:
                #traceback.print_exc()
                #print("time out")
                #return {}
                returnJSON = {}
                pass
        return returnJSON



def findSkyCam():
    IPAddr = subprocess.check_output(['hostname', '-I'])
       
    IPAddr = IPAddr.decode()
    IPAddr = IPAddr.split(" ")
    print("Your Computer IP Address is:" + IPAddr[0])  
    myIP = IPAddr[0]
    myNetIP = IPAddr[0].split(".")
    myNetIP = myNetIP[0]+"."+myNetIP[1]+"."+myNetIP[2]+".0"
    CIDR = ipaddress.IPv4Network(myNetIP+"/24")
    print("Your Computer CIDR is:", CIDR)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", str(now))
    returnJSON = []

    for ip in ipaddress.IPv4Network(CIDR):
        if (ip != ipaddress.ip_address(myNetIP)):
            
            print ("checking IP:", str(ip))
            command = "checkForID?params="+myIP+",1883" 
            JSON = sendCommandToWireless(ip, command)
            #print("JSON=",JSON)
            #{"return_value": 0, "id": "26FD", "name": "SkyCam", "ipaddress": "192.168.1.2", "hardware": "esp32","return_string": "26FD,24", "connected": true}
    
            if len(JSON) != 0:
                #DumpedJSON = json.dumps(JSON[1])
                #DumpedJSON = json.loads(DumpedJSON)
                #DumpedJSON = json.loads(DumpedJSON)
                DumpedJSON = JSON 
                #print("DumpedJSON =", DumpedJSON)
                try:
                    if (len(DumpedJSON) > 4):
                        if (len(DumpedJSON["return_string"]) > 0):
                            return_string = DumpedJSON["return_string"]
                            splitstring = return_string.split(",")
                            if (len(splitstring) == 2):
                                print(">>>>>>>>>>>>>>>>")
                                print ("SkyCam Remote Found. IP Address=", DumpedJSON["ipaddress"]) 
                                print ("ID,version=", DumpedJSON["return_string"])
                                print(">>>>>>>>>>>>>>>>")
                                returnJSON.append(JSON)

                except:
                    traceback.print_exc()
                    pass
            
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Finish Time =", str(now))
    print ("returnJSON", returnJSON)

    return returnJSON 

print("############################")
print("Starting Find SkyCam Remote")
print("############################")
print("This will run for about 300 minutes")
print("Starting Scan")

findSkyCam()
