#build state JSON

import config
import state
import json
from datetime import datetime


def getStateJSON():

        now = datetime.now()
        data = {}
        data['SkyWeather2Version'] = config.SWVERSION
        data['SampleDateTime'] = now.strftime("%m/%d/%y, %H:%M:%S %Z%z")
        data['UTCTime'] = datetime.utcnow().isoformat()
        data['lastMainReading'] = state.lastMainReading
        data['lastInsideReading'] = state.lastInsideReading
        data['mainID'] = state.mainID
        data['insideID'] = state.insideID
        data['currentOutsideTemperature'] = state.currentOutsideTemperature
        data['currentOutsideHumidity'] = state.currentOutsideHumidity
        data['currentInsideTemperature'] = state.currentInsideTemperature
        data['currentInsideHumidity'] = state.currentInsideHumidity
        data['currentRain60Minutes'] = state.currentRain60Minutes
        data['currentSunlightVisible'] = state.currentSunlightVisible
        data['currentSunlightIR'] = state.currentSunlightIR
        data['currentSunlightUV'] = state.currentSunlightUV
        data['currentSunlightUVIndex '] = state.currentSunlightUVIndex 
        data['ScurrentWindSpeed'] = state.ScurrentWindSpeed
        data['ScurrentWindGust '] = state.ScurrentWindGust 
        data['ScurrentWindDirection '] = state.ScurrentWindDirection 
        data['currentTotalRain '] = state.currentTotalRain 
        data['currentBarometricTemperature'] = state.currentBarometricTemperature
        data['currentBarometricPressure'] = state.currentBarometricPressure
        data['currentAltitude'] = state.currentAltitude
        data['currentSeaLevel'] = state.currentSeaLevel
        data['barometricTrend'] = state.barometricTrend
        data['pastBarometricReading'] = state.pastBarometricReading
        data['Indoor_AirQuality_Sensor_Value'] = state.Indoor_AirQuality_Sensor_Value
        data['Outdoor_AirQuality_Sensor_Value'] = state.Outdoor_AirQuality_Sensor_Value
        data['Hour24_Outdoor_AirQuality_Sensor_Value'] = state.Hour24_Outdoor_AirQuality_Sensor_Value
        data['currentAs3935Interrupt'] = state.currentAs3935Interrupt
        data['currentAs3935LastInterrupt'] = state.currentAs3935LastInterrupt
        data['currentAs3935LastDistance'] = state.currentAs3935LastDistance
        data['currentAs3935LastStatus'] = state.currentAs3935LastStatus
        data['currentAs3935LastLightningTimeStamp'] = state.currentAs3935LastLightningTimeStamp
        data['Last_Event'] = state.Last_Event
        data['EnglishMetric'] = state.EnglishMetric
        data['batteryVoltage'] = state.batteryVoltage
        data['batteryCurrent'] = state.batteryCurrent
        data['solarVoltage'] = state.solarVoltage
        data['solarCurrent'] = state.solarCurrent
        data['loadVoltage'] = state.loadVoltage
        data['loadCurrent'] = state.loadCurrent
        data['batteryPower'] = state.batteryPower
        data['solarPower'] = state.solarPower
        data['loadPower'] = state.loadPower
        data['batteryCharge'] = state.batteryCharge
        data['SolarMAXLastReceived'] = state.SolarMAXLastReceived
        data['SolarMaxInsideTemperature'] = state.SolarMaxInsideTemperature
        data['SolarMaxInsideHumidity'] = state.SolarMaxInsideHumidity
        data['fanState'] = state.fanState

        return json.dumps(data)
