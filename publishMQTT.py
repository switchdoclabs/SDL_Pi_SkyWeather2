
import config
import state

import paho.mqtt.client


def publish():

    if (config.SWDEBUG):
        print("--->Sending MQTT Packet<---")
    state.mqtt_client.publish("SkyWeather2", state.currentStateJSON)


