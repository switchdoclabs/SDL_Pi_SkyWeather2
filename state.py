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

# JSON state record

currentStateJSON = ""
# WeatherSTEM info

WeatherSTEMHash = ""

# Weather Variable Sensor Reads

lastMainReading ="Never"
lastInsideReading = "Never"
mainID = ""
insideID = ""
# Weather Variables

currentOutsideTemperature = 0.0
currentOutsideHumidity = 1

currentInsideTemperature = 0.0
currentInsideHumidity = 1

currentRain60Minutes = 0.0

currentSunlightVisible = 0
currentSunlightIR = 0
currentSunlightUV = 0
currentSunlightUVIndex  = 0

ScurrentWindSpeed = 0
ScurrentWindGust  = 0
ScurrentWindDirection  = 0.2
currentTotalRain  = 0

currentBarometricTemperature = 0
currentBarometricPressure = 0
currentAltitude = 0 
currentSeaLevel = 0
barometricTrend = True
pastBarometricReading = 0

Indoor_AirQuality_Sensor_Value = 0
Outdoor_AirQuality_Sensor_Value = 0
Hour24_Outdoor_AirQuality_Sensor_Value = 0




# Lightning Values

currentAs3935Interrupt = 0

currentAs3935LastInterrupt = 0
currentAs3935LastDistance = 0
currentAs3935LastStatus = 0

currentAs3935LastLightningTimeStamp = 0

# Button Variables

runRainbow = False
flashStrip = False
runOLED = True

# status Values

Last_Event = "My Last Event"
EnglishMetric = 0


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
SolarMAXLastReceived = "None"

SolarMaxInsideTemperature = 0.0
SolarMaxInsideHumidity = 0.0
# Fan State

fanState = False


def printState():

    print ("-------------")
    print ("Current State")
    print ("-------------")
    print("latest MainSensor Reading=", lastMainReading)
    print("MainDeviceNumber=", mainID)
    print("currentOutsideTemperature = ",currentOutsideTemperature )
    print("currentOutsideHumidity = ", currentOutsideHumidity )

    print("latest Inside Sensor Reading=", lastInsideReading)
    print("InsideDeviceNumber=", insideID)
    print("currentInsideTemperature = ",currentInsideTemperature)
    print("currentInsideHumidity = ",  currentInsideHumidity )

    print("currentRain60Minutes = ",  currentRain60Minutes )

    print("currentSunlightVisible = ",  currentSunlightVisible )
    print("currentSunlightIR = ", currentSunlightIR )
    print("currentSunlightUV = ",  currentSunlightUV )
    print("currentSunlightUVIndex  = ", currentSunlightUVIndex  )

    print("ScurrentWindSpeed = ", ScurrentWindSpeed)
    print("ScurrentWindGust  = ",  ScurrentWindGust )
    print("ScurrentWindDirection  = ",  ScurrentWindDirection )
    print("currentTotalRain  = ", currentTotalRain  )

    print ("currentBarometricTemperature = ", currentBarometricTemperature )
    print ("currentBarometricPressure = ", currentBarometricPressure )
    print ("currentAltitude = ", currentAltitude )
    print ("currentSeaLevel = ", currentSeaLevel )
    print ("barometricTrend =",barometricTrend )
    print ("pastBarometricReading = ", pastBarometricReading )

    print ("Outdoor_AirQuality_Sensor_Value = ",  Outdoor_AirQuality_Sensor_Value )
    print ("Hour24_Outdoor_AirQuality_Sensor_Value = ",  Hour24_Outdoor_AirQuality_Sensor_Value )
    print ("Indoor_AirQuality_Sensor_Value = ",  Indoor_AirQuality_Sensor_Value )

    print ("-------------")


    print ("currentAs3935Interrupt = ", currentAs3935Interrupt )

    print ("currentAs3935LastInterrupt = ", currentAs3935LastInterrupt )
    print ("currentAs3935LastDistance = ",  currentAs3935LastDistance )
    print ("currentAs3935LastStatus = ", currentAs3935LastStatus )
    
    print ("currentAs3935LastLightningTimeStamp = ", currentAs3935LastLightningTimeStamp )


    
    print ("-------------")


    print ("runRainbow = ", runRainbow )
    print ("flashStrip = ", flashStrip )
    print ("runOLED =", runOLED )
    print ("-------------")



    print ("Last_Event = ", Last_Event )
    print ("EnglishMetric = ", EnglishMetric )
    
    
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
