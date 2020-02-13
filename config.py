
#
#
# configuration file - contains customization for SkyWeather system
#

# it is a good idea to copy this file into a file called "conflocal.py" and edit that instead of this one.  This file is wiped out if you update SkyWeather.

SWDEBUG = False

SWVERSION = "001" # set in SkyWeather.py
import uuid 
  
# printing the value of unique MAC 
# address using uuid and getnode() function  
MACADDRESS = hex(uuid.getnode()) 

mailUser = "yourusename"
mailPassword = "yourmailpassword"

notifyAddress ="you@example.com"

fromAddress = "yourfromaddress@example.com"

enableText = False
textnotifyAddress = "yourphonenumber@yourprovider"

#MySQL Logging and Password Information

enable_MySQL_Logging = False
MySQL_Password = "password"

# modify this IP to enable WLAN operating detection  - search for WLAN_check in SkyWeather.py
enable_WLAN_Detection = False
PingableRouterAddress = "192.168.1.1"

# LED configuration (on use on a Raspberry Pi 3B+)

runLEDs = False

# WXLink and SolarMAX configuration
SolarMAX_Present = False

# SolarMAX_Type = "LEAD" for SolarMAX Lead Acid
# SolarMAX_Type = "LIPO" for SolarMAX LiPo
SolarMAX_Type = ""

# WeatherSTEM configuration

USEWEATHERSTEM = False
INTERVAL_CAM_PICS__SECONDS = 60
STATIONMAC = MACADDRESS
STATIONKEY="XXXXYYYY"
STATIONHARDWARE=""


# WeatherUnderground Station

WeatherUnderground_Present = False
WeatherUnderground_StationID = "KWXXXXX"
WeatherUnderground_StationKey = "YYYYYYY"

############
# Blynk configuration
############

USEBLYNK = False 
BLYNK_AUTH = 'xxxxx'
BLYNK_URL = 'http://blynk-cloud.com/'

############
# AS3935 Lightning Configuration
############
# format: [NoiseFLoor, Indoor, TuneCap, DisturberDetection, WatchDogThreshold, SpikeDetection]
AS3935_Lightning_Config = [2,1,3,0,3,3]



# for barometeric pressure - needed to calculate sealevel equivalent - set your weatherstation elevation here

BMP280_Altitude_Meters = 626.0

# device present global variables
# do not change - set by software
Camera_Present = False
SunAirPlus_Present = False
AS3935_Present = False
BMP280_Present = False
OLED_Present = False
Sunlight_Present = False
DustSensor_Present = True
# End of Do not change


# set Sunlight High Gain (indoors - 1) or Low Gain (outdoors - 0)
Sunlight_Gain = 0


DustSensorSCL = 20
DustSensorSDA = 21
DustSensorPowerPin = 12

# for fan
GPIO_Pin_PowerDrive_Sig1 = 4
GPIO_Pin_PowerDrive_Sig2 = 4     # GPIO 4

WATCHDOGTRIGGER = 6

