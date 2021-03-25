
import config
import state
import pclogging
import traceback
import paho.mqtt.client


def publish():

    if (config.SWDEBUG):
        pclogging.systemlog(config.INFO,"--->Sending MQTT Packet<---")

    try:   
        state.mqtt_client.publish("skyweather2/state", state.StateJSON)
    except:
        try:
                pclogging.errorlog("mqtt failed", traceback.format_exc()) 
        except:     
                print(traceback.format_exc()) 
                print ("--------------------")
                print ("MQTT Failed")
                print ("--------------------")


