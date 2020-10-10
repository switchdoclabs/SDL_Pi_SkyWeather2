# handles updating the IT Sensor Dictionary
import state
import datetime


def buildITReading (DeviceID, ChannelID, Temperature, Humidity, BatteryOK, time):
    newchannel = {}
    newchannel["deviceID"] = DeviceID
    newchannel["channelID"] = ChannelID 
    newchannel["temperature"] = Temperature
    newchannel["humidity"] = Humidity
    newchannel["batteryOK"] = BatteryOK
    newchannel["time"] = time
    state.IndoorTH.append(newchannel)
    #print("built IndoorIH")


def addITReading(DeviceID, ChannelID, Temperature, Humidity, BatteryOK, Time):

    if (len(state.IndoorTH) > 0):
        # check existing records, update if found 
        for singleChannel in state.IndoorTH:
            if (singleChannel["channelID"] == ChannelID):
                print("update IndoorIH")
                singleChannel["deviceID"] = DeviceID
                singleChannel["temperature"] = Temperature
                singleChannel["humidity"] = Humidity
                singleChannel["batteryOK"] = BatteryOK
                singleChannel["time"] = Time

                #print ("state.IndoorTH=",state.IndoorTH)
                return
    buildITReading(DeviceID, ChannelID, Temperature, Humidity, BatteryOK, Time)
    #print ("state.IndoorTH=",state.IndoorTH)



