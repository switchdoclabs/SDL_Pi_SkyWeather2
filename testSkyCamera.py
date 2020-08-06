# imports
# Check for user imports
from __future__ import print_function
import config

import state
import SkyCamera


#Establish WeatherSTEMHash
if (config.USEWEATHERSTEM == True):
    state.WeatherSTEMHash = SkyCamera.SkyWeatherKeyGeneration(config.STATIONKEY)

    print("config.STATIONKEY=", config.STATIONKEY)
# test SkyWeather Camera and WeatherSTEM
print ("taking SkyPicture")
SkyCamera.takeSkyPicture()
print ("sending SkyCamera")
SkyCamera.sendSkyWeather()

