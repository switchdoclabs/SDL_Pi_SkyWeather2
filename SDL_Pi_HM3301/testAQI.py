import aqi
myaqi = aqi.to_aqi([
        (aqi.POLLUTANT_PM25, '4'),
        (aqi.POLLUTANT_PM10, '4')
    ])

print("myAQI=", myaqi)
