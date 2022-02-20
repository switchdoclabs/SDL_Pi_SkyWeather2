import aqi
myaqi = aqi.to_aqi([
        (aqi.POLLUTANT_PM25, '102'),
        (aqi.POLLUTANT_PM10, '192')
    ])

print("myAQI=", myaqi)
