# 
# Contains State Variables
#

# FT0300 Invalid Statements
# Invalid data / null / max / min defines


INVALID_DATA_8  =               0x7a          # Invalid value (corresponding to 8bit value)
INVALID_DATA_16 =               0x7ffa        # Invalid value (corresponding to 16bit value)
INVALID_DATA_32 =               0x7ffffffa    # Invalid value (corresponding to 32bit value)

NULL_DATA_8     =               0x7b          # Indicates that the field does not exist
NULL_DATA_16    =               0x7ffb
NULL_DATA_32    =               0x7ffffffb

LOW_DATA_8      =               0x7c          # Means less than the minimum value that can be expressed
LOW_DATA_16     =               0x7ffc
LOW_DATA_32     =               0x7ffffffc

HIGH_DATA_8     =               0x7d          # Means greater than the maximum value that can be expressed
HIGH_DATA_16    =               0x7ffd
HIGH_DATA_32    =               0x7ffffffd

# 0x7e, 0x7f skip


# ===============================================================================
# Maximum and minimum
# ===============================================================================
TEMP_MIN_F      =               0            # -40.0F, offset 40.0F
TEMP_MAX_F      =               1800         # 140.0F, offset 40.0F

HUMI_MIN        =               10           # 10%
HUMI_MAX        =               99           # 99%

WIND_MAX        =               500          # 50.0m/s

RAIN_MAX        =               99999        # 9999.9mm

# WeatherSTEM info

WeatherSTEMHash = ""

# Weather Variable Sensor Reads



######################
# Weather State Variables
######################


# JSON state record

StateJSON = ""




# Weather Variable Sensor Reads

lastMainReading ="Never"
lastIndoorReading = "Never"
previousMainReading = "Never"
previousIndoorReading = "Never"
mainID = ""
insideID = ""
# Weather Variables

OutdoorTemperature = 0.0
OutdoorHumidity = 0.0

IndoorTemperature = 0.0
IndoorHumidity = 0.0

Rain60Minutes = 0.0

SunlightVisible = 0.0
SunlightUVIndex  = 0.0

WindSpeed = 0
WindGust  = 0
WindDirection  = 0.2
TotalRain  = 0

BarometricTemperature = 0
BarometricPressure = 0
Altitude = 0 
BarometricPressureSeaLevel = 0
BarometricTemperature = 0
barometricTrend = True
pastBarometricReading = 0

AQI = 0.0
Hour24_AQI = 0.0

# WeatherSense AQI Values
WS_AQI = 0.0
WS_Hour24_AQI = 0.0

BatteryOK = "OK"
CPUTemperature = 0.0

# Indoor Temperature Sensor Array

IndoorTH = []


# status Values

Last_Event = "My Last Event"




# Button Variables

runRainbow = False
flashStrip = False
runOLED = True

# status Values

Last_Event = "My Last Event"


# Solar Values


batteryVoltage = 0
batteryCurrent = 0
solarVoltage = 0
solarCurrent = 0
loadVoltage = 0
loadCurrent = 0
batteryPower = 0
solarPower = 0
loadPower = 0
batteryCharge = 0
SolarMAXLastReceived = "Never"

SolarMaxInsideTemperature = 0.0
SolarMaxInsideHumidity = 0.0
# Fan State

fanState = False


def printState():

    print ("-------------")
    print ("Current State")
    print ("-------------")



    print ("-------------")


    print("latest MainSensor Reading=", lastMainReading)
    print("MainDeviceNumber=", mainID)
    print("OutdoorTemperature = ",OutdoorTemperature )
    print("OutdoorHumidity = ", OutdoorHumidity )

    print("latest Indoor Sensor Reading=", lastIndoorReading)
    print("IndoorDeviceNumber=", insideID)
    print("IndoorTemperature = ",IndoorTemperature)
    print("IndoorHumidity = ",  IndoorHumidity )

    print("Rain60Minutes = ",  Rain60Minutes )

    print("SunlightVisible = ",  SunlightVisible )
    print("SunlightUVIndex  = ", SunlightUVIndex  )

    print("WindSpeed = ", WindSpeed)
    print("WindGust  = ",  WindGust )
    print("WindDirection  = ",  WindDirection )
    print("TotalRain  = ", TotalRain  )

    print ("BarometricTemperature = ", BarometricTemperature )
    print ("BarometricPressure = ", BarometricPressure )
    print ("Altitude = ", Altitude )
    print ("BarometricPressureSeaLevel = ", BarometricPressureSeaLevel )
    print ("BarometricTemperature = ", BarometricTemperature )
    print ("barometricTrend =",barometricTrend )
    print ("pastBarometricReading = ", pastBarometricReading )

    print ("AQI = ",  AQI )
    print ("Hour24_AQI = ",  Hour24_AQI )
    print ("WS_AQI = ",  WS_AQI )
    print ("WS_Hour24_AQI = ",  WS_Hour24_AQI )
    print ("Main Battery Status = ",  BatteryOK )
    print ("CPU Temperature = ",  CPUTemperature )

    
    print ("-------------")


    print ("runRainbow = ", runRainbow )
    print ("flashStrip = ", flashStrip )
    print ("runOLED =", runOLED )
    print ("-------------")



    print ("Last_Event = ", Last_Event )
    
    
    print ("-------------")

    print ("batteryVoltage", batteryVoltage )
    print ("batteryCurrent", batteryCurrent)
    print ("solarVoltage", solarVoltage )
    print ("solarCurrent", solarCurrent)
    print ("loadVoltage", loadVoltage)
    print ("loadCurrent", loadCurrent)
    print ("batteryPower", batteryPower)
    print ("solarPower", solarPower)
    print ("loadPower", loadPower)
    print ("batteryCharge", batteryCharge)

    print ("SolarMAX Inside Temperature", SolarMaxInsideTemperature)
    print ("SolarMAX Inside Humidity", SolarMaxInsideHumidity)
    print ("SolarMAX Last Received", SolarMAXLastReceived)
    print ("-------------")

    print ("-------------")

    print ("-------------")
    print ("fanState = ", fanState)
    print ("-------------")



import threading
buildJSONSemaphore = threading.Semaphore()

mqtt_client = None
