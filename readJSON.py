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
        config.USEWSLIGHTNING = False
        config.USEWSAQI = False
        config.USEWSSKYCAM = False
        config.DustSensorSCL = 20
        config.DustSensorSDA = 21
        config.DustSensorPowerPin = 5
        config.GPIO_Pin_PowerDrive_Sig1 = 4
        config.GPIO_Pin_PowerDrive_Sig2 = 4
        config.WATCHDOGTRIGGER = 6
        config.Camera_Night_Enable =  False
        config.Camera_Rotation =  0
        config.REST_Enable = False 
        config.MQTT_Enable = False 
        config.MQTT_Server_URL = "localhost" 
        config.MQTT_Port_Number = 1883 
        config.MQTT_Send_Seconds = 500 
        config.English_Metric = False 
       
       

def getJSONValue(entry):
        try:
            returnData = config.JSONData[entry]
            return returnData
        except:
            print("JSON value not found:", entry)
            return "" 



def readJSON(addPath):

        setDefaults()

        if os.path.isfile(addPath+'SkyWeather2.JSON'):
            print (addPath+"SkyWeather2.JSON File exists")
            with open(addPath+'SkyWeather2.JSON') as json_file:
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
                config.USEWSLIGHTNING = getJSONValue('USEWSLIGHTNING')
                config.USEWSAQI = getJSONValue('USEWSAQI')
                config.USWSSKYCAM = getJSONValue('USEWSSKYCAM')
                config.DustSensorSCL = int(getJSONValue('DustSensorSCL'))
                config.DustSensorSDA = int(getJSONValue('DustSensorSDA'))
                config.DustSensorPowerPin = int(getJSONValue('DustSensorPowerPin'))
                config.GPIO_Pin_PowerDrive_Sig1 = int(getJSONValue('GPIO_Pin_PowerDrive_Sig1'))
                config.GPIO_Pin_PowerDrive_Sig2 = int(getJSONValue('GPIO_Pin_PowerDrive_Sig2'))
                config.WATCHDOGTRIGGER = int(getJSONValue('WATCHDOGTRIGGER'))
                config.Camera_Night_Enable = getJSONValue('Camera_Night_Enable')
                config.Camera_Rotation = getJSONValue('Camera_Rotation')
                config.REST_Enable = getJSONValue('REST_Enable')
                config.MQTT_Enable = getJSONValue('MQTT_Enable')
                config.MQTT_Server_URL = getJSONValue('MQTT_Server_URL')
                config.MQTT_Port_Number = int(getJSONValue('MQTT_Port_Number'))
                config.MQTT_Send_Seconds = int(getJSONValue('MQTT_Send_Seconds'))
                config.English_Metric = getJSONValue('English_Metric')

        else:
            print ("SkyWeather2.JSON File does not exist")
            setDefaults()



