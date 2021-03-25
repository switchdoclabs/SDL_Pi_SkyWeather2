from __future__ import print_function

import requests
import time 
import picamera
import state

import hashlib



from PIL import ImageFont, ImageDraw, Image
import traceback
import util
import datetime as dt


import config
import pclogging

def SkyWeatherKeyGeneration(userKey):

    catkey = "AZWqNqDMhvK8Lhbb2jtk1bucj0s2lqZ6" +userKey

    md5result = hashlib.md5(catkey.encode())
    #print ("hashkey =", md5result.hexdigest())
    return md5result.hexdigest()

def takeSkyPicture():
 
    if (config.SWDEBUG):
        pclogging.systemlog(config.INFO, "--->skyCamera taking pic<---")
        print ("--------------------")
        print ("SkyCam Picture Taken")
        print ("--------------------")
    
    camera = picamera.PiCamera()

    camera.exposure_mode = "auto"
    try:
        camera.rotation = config.Camera_Rotation
        
        camera.resolution = (1920, 1080)
        # Camera warm-up time
        time.sleep(2)

        camera.capture('static/skycamera.jpg')

        # now add timestamp to jpeg
        pil_im = Image.open('static/skycamera.jpg')
      
        draw = ImageDraw.Draw(pil_im)
        
        # Choose a font
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)

        # set up units
        #wind
        val = util.returnWindSpeed(state.WindSpeed)
        WindStval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
        val = util.returnWindSpeed(state.WindGust)
        WindGtval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
        val = util.returnTemperatureCF(state.OutdoorTemperature)
        OTtval = "{0:0.1f} ".format(val) + util.returnTemperatureCFUnit()

        myText = "SkyWeather2 V%s %s Wind Speed: %s Wind Gust: %s Temp: %s " % (config.SWVERSION,dt.datetime.now().strftime('%d-%b-%Y %H:%M:%S'),WindStval, WindGtval, OTtval)
        print("mySkyCameraText=", myText)

        # Draw the text
        color = 'rgb(255,255,255)'
        #draw.text((0, 0), myText,fill = color, font=font)

        # get text size
        text_size = font.getsize(myText)

        # set button size + 10px margins
        button_size = (text_size[0]+20, text_size[1]+10)

        # create image with correct size and black background
        button_img = Image.new('RGBA', button_size, "black")
     
        # put text on button with 10px margins
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((10, 5), myText, fill = color, font=font)

        # put button on source image in position (0, 0)

        pil_im.paste(button_img, (0, 0))
        bg_w, bg_h = pil_im.size 
        # WeatherSTEM logo in lower left
        size = 64
        WSLimg = Image.open("static/WeatherSTEMLogoSkyBackground.png")
        WSLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(WSLimg, (0, bg_h-size))

        # SkyWeather log in lower right
        SWLimg = Image.open("static/SkyWeatherLogoSymbol.png")
        SWLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(SWLimg, (bg_w-size, bg_h-size))

        # Save the image
        pil_im.save('dash_app/assets/skycamera.jpg', format= 'JPEG')
        pil_im.save('static/skycamera.jpg', format= 'JPEG')
        pil_im.save('static/skycameraprocessed.jpg', format= 'JPEG')

        time.sleep(2)

    except:
        try:
                pclogging.errorlog("skycam pic failed", traceback.format_exc()) 
        except:     
                print(traceback.format_exc()) 
                print ("--------------------")
                print ("SkyCam Picture Failed")
                print ("--------------------")


    finally:
        try:
                camera.close()
        except:
                try:
                        pclogging.errorlog("skycam close failed", traceback.format_exc()) 
                except:     
                        print(traceback.format_exc()) 
                        print ("--------------------")
                        print ("SkyCam Close Failed ")
                        print ("--------------------")


    if (config.USEWEATHERSTEM == True):
        sendSkyWeather()


import base64


def sendSkyWeather():

    # defining the api-endpoint  
    API_ENDPOINT = "https://skyweather.weatherstem.com/"
  

    with open("static/skycamera.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())
       encoded_string = encoded_string.decode('utf-8')

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Package Sending")
        print ("--------------------")
        print ("API Key:",state.WeatherSTEMHash)
    if(state.barometricTrend == True):
        bptrendvalue = "Rising"
    else:
        bptrendvalue = "Falling"
   
    currentTime = time.time()

    print("------->Sea Level", state.BarometricPressureSeaLevel*10.0)
    data = {
                "SkyWeatherVersion": config.SWVERSION,
                "SkyWeatherHardware": config.STATIONHARDWARE,
                "api_key": state.WeatherSTEMHash,

	"device":{
                "key":  config.STATIONKEY,
                "MAC":config.STATIONMAC,
	},
	"utc":currentTime,
	"sensors":[


		{
			"name":"OutsideTemperature",
			"value": state.OutdoorTemperature,
                        "units" : "C"

		},
		{
			"name":"OutsideHumidity",
			"value": state.OutdoorHumidity,
                        "units" : "%"

		},
		{
			"name":"InsideTemperature",
			"value": state.IndoorTemperature,
                        "units" : "C"
		},
		{
			"name":"InsideHumidity",
			"value": state.IndoorHumidity,
                        "units" : "%"

		},
		{
			"name":"RainInLast60Minutes",
			"value": state.Rain60Minutes,
                        "units" : "mm/h"
		},
		{
			"name":"VisibleSunlight",
			"value": state.SunlightVisible,
                        "units" : "lux"
		},
        {
            "name":"IRSunlight",
            "value": "0.0",
                        "units" : "lux"
        },
        {
            "name":"UVSunlightt",
            "value": "0.0", 
                        "units" : "lux"
        },
		{
			"name":"WindSpeed",
			"value": state.WindSpeed,
                        "units" : "kph"
		},
		{
			"name":"WindGust",
			"value": state.WindGust,
                        "units" : "kph"
		},
		{
			"name":"WindDirection",
			"value": state.WindDirection,
                        "units" : "degrees"
		},
		{
			"name":"totalRain",
			"value": state.TotalRain,
                        "units" : "mm"

		},
		{
			"name":"BarometricPressure",
			"value": state.BarometricPressure*10.0,
                        "units" : "hPa"

		},
		{
			"name":"Altitude",
			"value": state.Altitude,
                        "units" : "m"
		},
		{
			"name":"SeaLevelPressure",
			"value": state.BarometricPressureSeaLevel*10.0,
                        "units" : "hPa"
		},
		{
			"name":"BarometricTrend",
			"value": bptrendvalue,
                        "units" : ""


		},
		{
			"name":"OutdoorAirQuality",
			"value": state.AQI,
                        "units" : "AQI"
		},

		#{
		#	"name":"UVSunlightIndex",
		#	"value": state.SunlightUVIndex,
        #                "units" : "index"
		#}
		
                ],
	"solarpower":[
		{
			"name":"BatteryVoltage",
			"value": state.batteryVoltage,
                        "units" : "V"


		},
		{
			"name":"BatteryCurrent",
			"value": state.batteryCurrent,
                        "units" : "ma"
		},
		{ 
                        "name":"SolarVoltage", 
                        "value": state.solarVoltage,
                        "units" : "V"
                },
		{
			"name":"SolarCurrent",
			"value": state.solarCurrent,
                        "units" : "ma"

		}, 
                {
			"name":"LoadVoltage",
			"value": state.loadVoltage,
                        "units" : "V"
		},
		{
			"name":"LoadCurrent",
			"value": state.loadCurrent,
                        "units" : "ma"
		},
		{
			"name":"BatteryPower",
			"value": state.batteryPower,
                        "units" : "W"
		},
		{
			"name":"SolarPower",
			"value": state.solarPower,
                        "units" : "W"
		},
		{
			"name":"LoadPower",
			"value": state.loadPower,
                        "units" : "W"
		},
		{
			"name":"BatteryCharge",
			"value": state.batteryCharge,
                        "units" : "%"

		},
		{
			"name":"WXBatteryVoltage",
			"value": 0,
                        "units" : "V"

		},
		{
			"name":"WXBatteryCurrent",
			"value": 0 ,
                        "units" : "ma"
		},
		{
			"name":"WXSolarVoltage",
			"value": 0 ,
                        "units" : "V"
		},
		{
			"name":"WXSolarCurrent",
			"value": 0 ,
                        "units" : "ma"
		},
		{
			"name":"WXLoadVoltage",
			"value": 0 ,
                        "units" : "V"
		},
		{
			"name":"WXLoadCurrent",
			"value": 0 ,
                        "units" : "ma"
		},
		{
			"name":"WXBatteryPOWER",
			"value": 0 ,
                        "units" : "W"
		},
		{
			"name":"WXSolarPower",
			"value": 0 ,
                        "units" : "W"
		},
		{
			"name":"WXLoadPower",
			"value": 0 ,
                        "units" : "W"
		},
		{
			"name":"WXBatteryCharge",
			"value": 0 ,
                        "units" : "%"


		}
		
	],
	"cameras":[
		{
			"name":"Sky Camera",
                        "image": encoded_string
		}
		
	]
    }
    import json
  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
    #print (data )
    # extracting response text  
    pastebin_url = r.text 
    if (config.SWDEBUG):
        print("The pastebin URL is (r.text):%s"%pastebin_url) 



        
