
#utility programs
import state
import updateBlynk
import RPi.GPIO as GPIO

# Check for user imports
import config



def returnStatusLine(device, state):

        returnString = device
        if (state == True):
                returnString = returnString + ":   \t\tPresent"
        else:
                returnString = returnString + ":   \t\tNot Present"
        return returnString



def barometricTrend():
    if (state.BarometricPressure >= state.pastBarometricReading):
        state.barometricTrend = True
    else:
        state.barometricTrend = False

    state.pastBarometricReading = state.BarometricPressure


################
# Unit Conversion
################
# 

def returnTemperatureCF(temperature):
	if (config.English_Metric == True):
		# return Metric 
		return temperature
	else:
		return (9.0/5.0)*temperature + 32.0

def returnTemperatureCFUnit():
    #print("config.English_Metric=", config.English_Metric)
    if (config.English_Metric == True):
        # return Metric 
        return "C"
    else:
        return  "F"

def returnWindSpeedUnit():
	if (config.English_Metric == True):
		# return Metric 
		return "KPH"
	else:
		return  "MPH"

def returnWindSpeed(wind):
	if (config.English_Metric == True):
		# return Metric 
		return wind
	else:
		return wind/1.6


def returnWindDirection(windDirection):

    if (windDirection > 315.0+1.0):
        return "NNW"
    if (windDirection > 292.5+1.0):
        return "NW"
    if (windDirection > 270.0+1.0):
        return "WNW"
    if (windDirection > 247.5+1.0):
        return "W"
    if (windDirection > 225.0+1.0):
        return "WSW"
    if (windDirection > 202.5+1.0):
        return "SW"
    if (windDirection > 180.0+1.0):
        return "SSW"
    if (windDirection > 157.5+1.0):
        return "S"
    if (windDirection > 135.0+1.0):
        return "SSE"
    if (windDirection > 112.5+1.0):
        return "SE"
    if (windDirection > 90.0+1.0):
        return "ESE"
    if (windDirection > 67.5+1.0):
        return "E"
    if (windDirection > 45.0+1.0):
        return "ENE"
    if (windDirection > 22.5+1.0):
        return "NE"
    if (windDirection > 0.0+1.0):
        return "NNE"
    return "N"






def returnPercentLeftInBattery(currentVoltage, maxVolt):

    if(config.SolarMAX_Type == "LEAD"):

        returnPercent = ((currentVoltage - 11.00)/(2.6)) * 100.00
        if (returnPercent > 100.00):
            returnPercent = 100.0
        if (returnPercent < 0.0):
            returnPercent = 0.0

        return returnPercent
    else:

        scaledVolts = currentVoltage / maxVolt

        if (scaledVolts > 1.0):
                scaledVolts = 1.0


        if (scaledVolts > .9686):
                returnPercent = 10*(1-(1.0-scaledVolts)/(1.0-.9686))+90
                return returnPercent

        if (scaledVolts > 0.9374):
                returnPercent = 10*(1-(0.9686-scaledVolts)/(0.9686-0.9374))+80
                return returnPercent


        if (scaledVolts > 0.9063):
                returnPercent = 30*(1-(0.9374-scaledVolts)/(0.9374-0.9063))+50
                return returnPercent

        if (scaledVolts > 0.8749):
                returnPercent = 20*(1-(0.8749-scaledVolts)/(0.9063-0.8749))+11

                return returnPercent


        if (scaledVolts > 0.8437):
                returnPercent = 15*(1-(0.8437-scaledVolts)/(0.8749-0.8437))+1
                return returnPercent


        if (scaledVolts > 0.8126):
                returnPercent = 7*(1-(0.8126-scaledVolts)/(0.8437-0.8126))+2
                return returnPercent



        if (scaledVolts > 0.7812):
                returnPercent = 4*(1-(0.7812-scaledVolts)/(0.8126-0.7812))+1
                return returnPercent

        return 0



