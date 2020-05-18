#
#
# configuration file - DO NOT MODIFY!   Defaults and configuration are read from a JSON file. SkyWeather2.JSON
#

#


SWVERSION = "001" # set in SkyWeather.py
import uuid 

# printing the value of unique MAC 
# address using uuid and getnode() function  
MACADDRESS = hex(uuid.getnode()) 

############
# WeatherSTEM configuration
############

STATIONMAC = MACADDRESS
STATIONHARDWARE=""


############
# Blynk configuration
############

BLYNK_URL = 'http://blynk-cloud.com/'


# device present global variables
# do not change - set by software in skyWeather2
Camera_Present = False
SunAirPlus_Present = False
AS3935_Present = False
BMP280_Present = False
OLED_Present = False
Sunlight_Present = False
DustSensor_Present = True

# Configuration Variables - Do not modify

SWDEBUG = None
enable_MySQL_Logging = None
MySQL_Password = None
enable_WLAN_Detection = None
PingableRouterAddress = None
mailUser = None
mailPassword = None
notifyAddress = None
fromAddress = None
enableText = None
textnotifyAddress = None
runLEDs = None
SolarMAX_Present = None
SolarMAX_Type = None
BMP280_Altitude_Meters = None
Sunlight_Gain = None
USEWEATHERSTEM = None
INTERVAL_CAM_PICS__SECONDS = None
STATIONKEY = None
WeatherUnderground_Present = None
WeatherUnderground_StationID = None
WeatherUnderground_StationKey = None
USEBLYNK = None
BLYNK_AUTH = None
AS3935_Lightning_Config = None
DustSensorSCL = None
DustSensorSDA = None
DustSensorPowerPin = None
GPIO_Pin_PowerDrive_Sig1 = None
GPIO_Pin_PowerDrive_Sig2 = None
WATCHDOGTRIGGER = None
Camera_Night_Enable = None
REST_Enable = None
MQTT_Enable = None
MQTT_Server_URL = None
MQTT_Port_Number = None
MQTT_Send_Seconds = None


import readJSON

# JSON read in files

# read JSON and put it it into the config variables

readJSON.readJSON()
