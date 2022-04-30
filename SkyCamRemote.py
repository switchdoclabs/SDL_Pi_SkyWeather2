
#
# wireless sensor routines


import config

import json
import random

import sys
from subprocess import PIPE, Popen, STDOUT, check_output
from threading import Thread
import datetime
import MySQLdb as mdb
import traceback
import state
import os
import ProcessPicture
import util
GoodMessage = 0
Resends = 0


MQTTUPDATEPARAM = 10
MQTTCYCLECHANGE = 11
MQTTSTARTDELAY = 12 
MQTTTURNOFFBLINK = 13
MQTTBLINKXTIMES = 14
MQTTSETTODEFAULTS = 15

import paho.mqtt.client as mqtt
from paho.mqtt import publish




def startMQTT():

    broker_address= config.MQTT_Server_URL
    print("creating new MQTT instance")
    client = mqtt.Client("SkyCam") #create new instance
    client.on_message=MTon_message #attach function to callback
    client.on_connect=MTon_connect
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.on_log=MTon_log 
    client.loop_start()

def MTon_log(client, userdata, level, buf):
    #print("log: ",buf)
    pass


# The callback for when the client receives a CONNACK response from the server.
def MTon_connect(client, userdata, flags, rc):
    global GoodMessage, Resends
    GoodMessage = 0
    Resends = 0
    #print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SKYCAM/+/PICTURECHUNKS")
    client.subscribe("SKYCAM/+/INFO")

# The callback for when a PUBLISH message is received from the server.
def MTon_message(client, userdata, msg):
    global GoodMessage, Resends
    #print("message found:",msg.topic)
    # get msg topic
    SplitTopic = msg.topic
    SplitTopic = SplitTopic.split("/")
    
    if (SplitTopic[2] == "INFO"):
        if (config.SWDEBUG):
            print("INFO msg Received: %s" % msg.payload)

        processINFOMessage(msg)
        return 
    if (SplitTopic[2] == "PICTURECHUNKS"):
        myChunk = json.loads(msg.payload)

        #print("Picture ID %s Chunk %s of %s  Received. Resends: %s  Size=%d" % (myChunk["messageid"],int(myChunk["chunknumber"])+1, myChunk["totalchunknumbers"], myChunk["totalchunkresends"], len(myChunk["chunk"])))
       
        if (int(myChunk["chunknumber"])+1 == int(myChunk["totalchunknumbers"])):
            GoodMessage = GoodMessage + 1
            Resends = Resends + int(myChunk["totalchunkresends"])
            if (config.SWDEBUG):
                print("Picture ID %s Good Message %s Resends: %d" % (myChunk["messageid"], GoodMessage, Resends))
        # deal with Chunks
        
        ProcessPicture.saveChunk(myChunk)


def sendCommand(client, msg, messageType, payload):
    # not complete - do not use
    # Commands:

    # send Blynk X Times
    # get msg topic
    SplitTopic = msg.topic
    SplitTopic = SplitTopic.split("/")
    #print (SplitTopic)
    MyTopic = SplitTopic[0]+"/"+SplitTopic[1]+"/"+"COMMANDS"
    # set up JSON 
    myIP = check_output(['hostname', '-I'])
    myIP = myIP.decode() 
    myIP = myIP.replace("\n","")
    myIP = myIP.replace(" ","")



    # send blink message
    if (messageType == MQTTBLINKXTIMES):
        myMessage = {
            "messagetype": MQTTBLINKXTIMES,
            "myip": myIP,
            "length": 300,
            "count": 3
            }

        myMessage = json.dumps(myMessage)
        client.publish(MyTopic, myMessage)

    # send time to sleep message
    if (messageType == MQTTCYCLECHANGE):
        myMessage = {
            "messagetype": MQTTCYCLECHANGE,
            "myip": myIP,
            "timetosleep": 50
            }

        myMessage = json.dumps(myMessage)
        client.publish(MyTopic, myMessage)

# send time to set contrast delay on startup
    if (messageType == MQTTUPDATEPARAM): 
        myMessage = {
            "messagetype": MQTTUPDATEPARAM,
            "myip": myIP,
            "sensorparams": payload
            }

        myMessage = json.dumps(myMessage)
        client.publish(MyTopic, myMessage)



def processINFOMessage(msg):

    myJSON = json.loads(msg.payload)

    if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
                myTEST = ""
                myTESTDescription = ""
                print("in INFO with SQL")

                con = mdb.connect(
                    "localhost",
                    "root",
                    config.MySQL_Password,
                    "WeatherSenseWireless" 
                )

                cur = con.cursor()
                batteryPower =  float(myJSON["batterycurrent"])* float(myJSON["batteryvoltage"])
                loadPower  =  float(myJSON["loadcurrent"])* float(myJSON["loadvoltage"])
                solarPower =  float(myJSON["solarpanelcurrent"])* float(myJSON["solarpanelvoltage"])
                batteryCharge = util.returnPercentLeftInBattery(float(myJSON["batteryvoltage"]), 4.2)
                #print("batteryChange=", batteryCharge)
                fields = "cameraid, messageid, softwareversion, messagetype, rssi, internaltemperature, internalhumidity, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent,  batterypower, loadpower, solarpower, gndrreboots, batterycharge"
                values = "'%s', %s, %s, %s, %s, %s, %s,    %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %d " % (
                myJSON["id"], 
                myJSON["messageid"], 
                myJSON["softwareversion"], 
                myJSON["messagetype"],
                myJSON["currentrssi"],
                myJSON["internaltemperature"],
                myJSON["internalhumidity"],
                myJSON["batteryvoltage"], 
                myJSON["batterycurrent"], 
                myJSON["loadvoltage"], 
                myJSON["loadcurrent"],
                myJSON["solarpanelvoltage"], 
                myJSON["solarpanelcurrent"], 
                batteryPower, 
                loadPower, 
                solarPower,
                myJSON["gndrreboots"],
                batteryCharge)
               
                query = "INSERT INTO SkyCamSensors (%s) VALUES(%s )" % (fields, values)
                #print(query)
                cur.execute(query)
                con.commit()
            except: 
                traceback.print_exc()
                con.rollback()
                # sys.exit(1)

            finally:
                cur.close()
                con.close()

                del cur
                del con

