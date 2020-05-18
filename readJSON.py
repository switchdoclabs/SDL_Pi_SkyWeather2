import os
import config
import json

def setDefaults():
        config.SWDEBUG = False
        config.enable_MySQL_Logging = False
        config.MySQL_Password = "password"
        config.enable_WLAN_Detection = False
        config.PingableRouterAddress = "192.168.1.1"
        config.mailUser = "yourusername"
        config.mailPassword = "yourmailpassword"
        config.notifyAddress = "you@example.com"
        config.fromAddress = "yourfromaddress@example.com"
        config.enableText = False
        config.textnotifyAddress = "yournumber@yourprovider"
        config.runLEDs = False
        config.SolarMAX_Present = False
        config.SolarMAX_Type = "LEAD"
        config.BMP280_Altitude_Meters = 626.0
        config.Sunlight_Gain = 0
        config.USEWEATHERSTEM = False
        config.INTERVAL_CAM_PICS__SECONDS = 60
        config.STATIONKEY = ""
        config.WeatherUnderground_Present = False
        config.WeatherUnderground_StationID = "KWXXXXX"
        config.WeatherUnderground_StationKey = "YYYYYY"
        config.USEBLYNK = False
        config.BLYNK_AUTH = ""
        config.AS3935_Lightning_Config = "[2,1,3,0,3,3]"
        config.DustSensorSCL = 20
        config.DustSensorSDA = 21
        config.DustSensorPowerPin = 12
        config.GPIO_Pin_PowerDrive_Sig1 = 4
        config.GPIO_Pin_PowerDrive_Sig2 = 4
        config.WATCHDOGTRIGGER = 6
        config.Camera_Night_Enable =  False
        config.REST_Enable = False 
        config.MQTT_Enable = False 
        config.MQTT_Server_URL = "" 
        config.MQTT_Port_Number = 5900 
        config.MQTT_Send_Seconds = 500 
       
       

def getJSONValue(entry):
        try:
            returnData = config.JSONData[entry]
            return returnData
        except:
            print("JSON value not found:", entry)
            return "" 



def readJSON():

        setDefaults()

        if os.path.isfile('SkyWeather2.JSON'):
            print ("SkyWeather2.JSON File exists")
            with open('SkyWeather2.JSON') as json_file:
                config.JSONData = json.load(json_file)


                config.SWDEBUG = getJSONValue('SWDEBUG')
                config.enable_MySQL_Logging = getJSONValue('enable_MySQL_Logging')
                config.MySQL_Password = getJSONValue('MySQL_Password')
                config.enable_WLAN_Detection = getJSONValue('enable_WLAN_Detection')
                config.PingableRouterAddress = getJSONValue('PingableRouterAddress')
                config.mailUser = getJSONValue('mailUser')
                config.mailPassword = getJSONValue('mailPassword')
                config.notifyAddress = getJSONValue('notifyAddress')
                config.fromAddress = getJSONValue('fromAddress')
                config.enableText = getJSONValue('enableText')
                config.textnotifyAddress = getJSONValue('textnotifyAddress')
                config.runLEDs = getJSONValue('runLEDs')
                config.SolarMAX_Present = getJSONValue('SolarMAX_Present')
                config.SolarMAX_Type = getJSONValue('SolarMAX_Type')
                config.BMP280_Altitude_Meters = float(getJSONValue('BMP280_Altitude_Meters'))
                config.Sunlight_Gain = getJSONValue('Sunlight_Gain')
                config.USEWEATHERSTEM = getJSONValue('USEWEATHERSTEM')
                config.INTERVAL_CAM_PICS__SECONDS = int(getJSONValue('INTERVAL_CAM_PICS__SECONDS'))
                config.STATIONKEY = getJSONValue('STATIONKEY')
                config.WeatherUnderground_Present = getJSONValue('WeatherUnderground_Present')
                config.WeatherUnderground_StationID = getJSONValue('WeatherUnderground_StationID')
                config.WeatherUnderground_StationKey = getJSONValue('WeatherUnderground_StationKey')
                config.USEBLYNK = getJSONValue('USEBLYNK')
                config.BLYNK_AUTH = getJSONValue('BLYNK_AUTH')
                config.AS3935_Lightning_Config = getJSONValue('AS3935_Lightning_Config')
                config.DustSensorSCL = int(getJSONValue('DustSensorSCL'))
                config.DustSensorSDA = int(getJSONValue('DustSensorSDA'))
                config.DustSensorPowerPin = int(getJSONValue('DustSensorPowerPin'))
                config.GPIO_Pin_PowerDrive_Sig1 = int(getJSONValue('GPIO_Pin_PowerDrive_Sig1'))
                config.GPIO_Pin_PowerDrive_Sig2 = int(getJSONValue('GPIO_Pin_PowerDrive_Sig2'))
                config.WATCHDOGTRIGGER = int(getJSONValue('WATCHDOGTRIGGER'))
                config.Camera_Night_Enable = getJSONValue('Camera_Night_Enable')
                config.REST_Enable = getJSONValue('REST_Enable')
                config.MQTT_Enable = getJSONValue('MQTT_Enable')
                config.MQTT_Server_URL = getJSONValue('MQTT_Server_URL')
                config.MQTT_Port_Number = int(getJSONValue('MQTT_Port_Number'))
                config.MQTT_Send_Seconds = int(getJSONValue('MQTT_Send_Seconds'))

        else:
            print ("SkyWeather2.JSON File does not exist")
            setDefaults()



