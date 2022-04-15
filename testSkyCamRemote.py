#
# tests SkyCam Remote and the updates parameters
#
import json
import paho.mqtt.client as mqtt
import os
import socket

import traceback
#commands

MQTTUPDATEPARAM = 10
MQTTCYCLECHANGE = 11
MQTTSTARTDELAY = 12 
MQTTTURNOFFBLINK = 13
MQTTBLINKXTIMES = 14
MQTTSETTODEFAULTS = 15
MQTTREBOOT = 16
MQTTRESOLUTION = 17
MQTTERASEMEMORY = 18

from subprocess import check_output

def on_log(client, userdata, level, buf):
    print("log: ",buf)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("SKYCAM/+/INFO")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)
    try:
        if (cameraID != ""):
            SplitTopic = msg.topic
            SplitTopic = SplitTopic.split("/")
            if (((SplitTopic[1] == cameraID) or (cameraID == "+")) and (SplitTopic[2] == "INFO")):
                myMessage = json.loads(msg.payload)
                if (myMessage["messagetype"] == "4"): 
                    # last INFO message - SkyCam only listens for a short while 
                    sendMessage(client, cameraID, sendWhatCommand)
    except:
        traceback.print_exc()

def sendMessage(client, cameraID, messageType):
    # send example command to SkyCameraRemote
    # send Blynk X Times
    # get msg topic
    MyTopic = "SKYCAM"+"/"+cameraID+"/"+"COMMANDS"
    # set up JSON 
    myIP = check_output(['hostname', '-I'])
    myIP = myIP.decode() 
    myIP = myIP.replace("\n","")
    myIP = myIP.replace(" ","")

    print("sending messagetype %s to:%s " %( messageType, MyTopic ))
# Commands:

    if (messageType == MQTTBLINKXTIMES):
        # send blink message
            myMessage = {
                "messagetype": MQTTBLINKXTIMES,
                "myip": myIP,
                "length": 300,
                "count": 3
                }

            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)

    if (messageType == MQTTCYCLECHANGE):
        # send time to sleep message
            myMessage = {
                "messagetype": MQTTCYCLECHANGE,
                "myip": myIP,
                "timetosleep": 60
                }

            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)

    if (messageType == MQTTSTARTDELAY):
            # send time to wait for contrast adjust 
            myMessage = {
                "messagetype": MQTTSTARTDELAY,
                "myip": myIP,
                "contrastdelay":1000 
                }
        
            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)

    if (messageType == MQTTREBOOT):
            #reboot SkyCam 
            myMessage = {
                "messagetype": MQTTREBOOT,
                "myip": myIP
                }
        
            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)

    if (messageType == MQTTRESOLUTION):
            # set resolution
            myMessage = {
                "messagetype": MQTTRESOLUTION,
                "myip": myIP,
                "framesize":10  # set UXGA 
                }
        
            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)

    if (messageType == MQTTERASEMEMORY):
            # set resolution
            myMessage = {
                "messagetype": MQTTERASEMEMORY,
                "myip": myIP
                }
        
            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)

    if (messageType == MQTTUPDATEPARAM):
            # update camera parameters 
            myMessage = {
                "messagetype": MQTTUPDATEPARAM,
                "myip": myIP,
                "sensorparams": "0;0;0;0;1;1;0;1;0;0;300;1;0;0;0;1;1;1;0;0;1;0;"
                #"sensorparams": "0;0;0;0;1;1;0;1;0;0;300;1;0;0;0;1;1;1;0;0;1;1;"
                }
        
            myMessage = json.dumps(myMessage)
            client.publish(MyTopic, myMessage)


    print("Messge Sent:",myMessage)




# main program

# what ID to test
#cameraID = "3BAD"
#cameraID = "F329"
#cameraID = "DE45"
cameraID = "26FD"
#cameraID = "+"   #sends to all cameras
# this command will be sent after an INFO messagetype 4  from cameraID
#sendWhatCommand = MQTTERASEMEMORY
sendWhatCommand = MQTTCYCLECHANGE
#sendWhatCommand = MQTTRESOLUTION 
#sendWhatCommand = MQTTBLINKXTIMES 
#sendWhatCommand = MQTTUPDATEPARAM 
#sendWhatCommand = MQTTSTARTDELAY 
#sendWhatCommand =  MQTTREBOOT 

#
client = mqtt.Client()
client.on_log=on_log
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", port=1883)


# Blocking call that processes network traffic, dispatches callbacks and

# handles reconnecting.
client.loop_forever()


