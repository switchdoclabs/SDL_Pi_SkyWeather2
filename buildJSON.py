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
        data['lastIndoorReading'] = state.lastIndoorReading
        data['mainID'] = state.mainID
        data['insideID'] = state.insideID

        data['OutdoorTemperature'] = state.OutdoorTemperature
        data['OutdoorHumidity'] = state.OutdoorHumidity
        data['IndoorTemperature'] = state.IndoorTemperature
        data['IndoorHumidity'] = state.IndoorHumidity
        data['Rain60Minutes'] = state.Rain60Minutes
        data['SunlightVisible'] = state.SunlightVisible
        data['SunlightUVIndex'] = state.SunlightUVIndex 
        data['WindSpeed'] = state.WindSpeed
        data['WindGust'] = state.WindGust 
        data['WindDirection'] = state.WindDirection 
        data['TotalRain'] = state.TotalRain 
        data['BarometricTemperature'] = state.BarometricTemperature
        data['BarometricPressure'] = state.BarometricPressure
        data['Altitude'] = state.Altitude
        data['BarometricPressureSeaLevel'] = state.BarometricPressureSeaLevel
        data['barometricTrend'] = state.barometricTrend
        data['pastBarometricReading'] = state.pastBarometricReading
        data['AQI'] = state.AQI
        data['Hour24_AQI'] = state.Hour24_AQI

        data['Last_Event'] = state.Last_Event
        data['English_Metric'] = config.English_Metric 
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
