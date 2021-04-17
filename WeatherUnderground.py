
# Send SkyWeather2 Information to the WeatherUnderground
#
# SwitchDoc Labs March, 2021
#
import sys
import requests
# import httplib
import traceback

import config
import state


def sendWeatherUndergroundData(Rain24Hour):

    if ((config.WeatherUnderground_Present == True) and (state.lastMainReading != "Never")):

    
        try:
            # https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=KCASANFR5&PASSWORD=XXXXXX&dateutc=2000-01-01+10%3A32%3A35&winddir=230&windspeedmph=12&windgustmph=12&tempf=70&rainin=0&baromin=29.1&dewptf=68.2&humidity=90&weather=&clouds=&softwaretype=vws%20versionxx&action=updateraw

            # build the URL
            myURL = "ID="+config.WeatherUnderground_StationID
            myURL += "&PASSWORD="+config.WeatherUnderground_StationKey
            myURL += "&dateutc=now"

            # now weather station variables
        
            myURL += "&winddir=%i" % state.WindDirection
        
            myURL += "&windspeedmph=%0.2f" % (state.WindSpeed/0.447704)
            myURL += "&windgustmph=%0.2f" % (state.WindGust/0.447704)
        
            myURL += "&humidity=%i" % state.OutdoorHumidity
            myURL += "&tempf=%0.2f" % ((state.OutdoorTemperature*9.0/5.0)+32.0)
        
            dewpoint =  state.OutdoorTemperature - ((100.0 - state.OutdoorHumidity) / 5.0);
            dewpointf = ((dewpoint*9.0/5.0)+32.0)
            myURL += "&dewptf=%0.2f" % dewpointf
        
            myURL += "&rainin=%0.2f" % ((state.Rain60Minutes)/25.4)
            myURL += "&dailyrainin=%0.2f" % ((Rain24Hour)/25.4)
            myURL += "&baromin=%0.2f" % (((state.BarometricPressureSeaLevel) * 0.2953))
        
            myURL += "&indoortempf=%0.2f" % ((state.IndoorTemperature*9.0/5.0)+32.0)
            myURL += "&indoorhumidity%0.2f=" % state.IndoorHumidity
            print("sv=", state.SunlightVisible) 
            print("svtype=", type(state.SunlightVisible) )
            myURL += "&solarradiation=%0.2f"% (float(state.SunlightVisible)*0.0079)
            myURL += "&UV=%0.2f"% state.SunlightUVIndex

            myURL += "&software=SkyWeather2"


            if (config.SWDEBUG):
	            print ("myURL=", myURL)
            #send it
            r = requests.get("https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php", params=myURL)

            if (config.SWDEBUG):
	            print(r.url)
	            print(r.text)
	            print( "GET sent")
        except:
            traceback.print_exc()
            print( "--WeatherUnderground Data Send Failed")


