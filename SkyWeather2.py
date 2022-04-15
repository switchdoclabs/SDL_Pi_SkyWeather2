#!/usr/bin/env python3
#
# SkyWeather2 Solar Powered Weather Station
# November 2020
#
# SwitchDoc Labs
# www.switchdoc.com
#
#

# imports
# Check for user imports
from __future__ import print_function

import config

config.SWVERSION = "027.4"
# system imports

import time
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events

import subprocess
import pclogging
import traceback
import sys
import picamera

# user defined imports
import updateBlynk
import state
import tasks
import wirelessSensors
import wiredSensors
import sendemail
import watchDog
import util
from  bmp280 import BMP280
import SkyCamera
import os

import SkyCamRemote
import PictureManagement
import ProcessPicture

# Scheduler Helpers

# print out faults inside events
def ap_my_listener(event):
        if event.exception:
              print (event.exception)
              print (event.traceback)


# helper functions

	
def shutdownPi(why):

   pclogging.systemlog(config.INFO, "Pi Shutting Down: %s" % why)
   sendemail.sendEmail("test", "SkyWeather2 Shutting down:"+ why, "The SkyWeather2 Raspberry Pi shutting down.", config.notifyAddress,  config.fromAddress, "");
   sys.stdout.flush()
   time.sleep(10.0)

   os.system("sudo shutdown -h now")

def rebootPi(why):

   pclogging.systemlog(config.INFO, "Pi Rebooting: %s" % why)
   if (config.USEBLYNK):
     updateBlynk.blynkTerminalUpdate("Pi Rebooting: %s" % why)
   pclogging.systemlog(config.INFO, "Pi Rebooting: %s" % why)
   os.system("sudo shutdown -r now")


import MySQLdb as mdb

# Program Requirement Checking and new directories
os.makedirs("static/SkyCam", exist_ok=True)


if (config.enable_MySQL_Logging):
    # SkyWeather2 SQL Database

    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "SkyWeather2"
          )

    except:
        print("--------")
        print("MySQL Database SkyWeather2 Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p < SkyWeather2.sql")
        print("SkyWeather2 Stopped")
        print("--------")
        sys.exit("SkyWeather2 Requirements Error Exit")



    # WeatherSense SQL Database
    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "WeatherSenseWireless"
          )

    except:
        print("--------")
        print("MySQL Database WeatherSenseWireless Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p < WeatherSenseWireless.sql")
        print("SkyWeather2 Stopped")
        print("--------")
        sys.exit("SkyWeather2 Requirements Error Exit")

    # Check for updates having been applied
    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "WeatherSenseWireless"
          )
        cur = con.cursor()
        query = "SELECT * FROM SkyCamPictures"
        cur.execute(query)
    except:
        #print(traceback.format_exc())
        print("--------")
        print("MySQL Database WeatherSenseWireless Updates Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p WeatherSenseWireless < updateWeatherSenseWireless.sql")
        print("SkyWeather2 Stopped")
        print("--------")
        sys.exit("SkyWeather2 Requirements Error Exit")

    # update weather table 27.2 update
    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "SkyWeather2"
          )
        cur = con.cursor()
        query = "SELECT SerialNumber FROM WeatherData"
        cur.execute(query)
    except:
        print("--------")
        print("MySQL Database SkyWeather2 Updates Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p SkyWeather2 < 27.2.DataBaseUpdate.sql")
        print("SkyWeather2 Stopped")
        print("--------")
        sys.exit("SkyWeather2 Requirements Error Exit")

    # update weather table 27.3 update
    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "SkyWeather2"
          )
        cur = con.cursor()
        query = "SELECT RSSI FROM WeatherData"
        cur.execute(query)
    except:
        print("--------")
        print("MySQL Database SkyWeather2 Updates for 27.3 Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p SkyWeather2 < 27.3.DataBaseUpdate.sql")
        print("SkyWeather2 Stopped")
        print("--------")
        sys.exit("SkyWeather2 Requirements Error Exit")
        

# main program
print ("")

print ("##########################################################")
print ("SkyWeather2 Weather Station Version "+config.SWVERSION+" - SwitchDoc Labs")
print ("")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("##########################################################")
print ("")

#
if (config.SWDEBUG):
    print("Starting pigpio daemon")

# kill all pigpio instances
try:
    cmd = [ 'killall', 'pigpiod' ]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    print(output)
    time.sleep(5)
except:
    #print(traceback.format_exc())
    pass

cmd = [ '/usr/bin/pigpiod' ]
output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
print(output)
import DustSensor

# detect devices

################
# Dust Sensor
################

try:

        DustSensor.powerOnDustSensor()
        time.sleep(3)
        myData = DustSensor.get_data()
        #print ("data=",myData)
        
        config.DustSensor_Present = True

except:

        config.DustSensor_Present = False




################
# BMP280 Setup 
################

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


# Initialise the BMP280
bus = SMBus(1)

try:
        bmp280 = BMP280(i2c_dev=bus, i2c_addr=0x77)
        state.BarometricTemperature = round(bmp280.get_temperature(), 2)
 
        config.BMP280_Present = True
except:
        if (config.SWDEBUG):
            pass
            #print(traceback.format_exc())

        config.BMP280_Present = False

################
# SkyCamera Setup 
################


#Establish WeatherSTEMHash
if (config.USEWEATHERSTEM == True):
    state.WeatherSTEMHash = SkyCamera.SkyWeatherKeyGeneration(config.STATIONKEY)

#Detect Camera WeatherSTEMHash
try:

    with picamera.PiCamera() as cam:
        if (config.SWDEBUG):
            print("Pi Camera Revision",cam.revision)
        cam.close()
    config.Camera_Present = True
except:
    config.Camera_Present = False


# display device present variables


print("----------------------")
print(util.returnStatusLine("BMP280",config.BMP280_Present))
print(util.returnStatusLine("SkyCam",config.Camera_Present))
print(util.returnStatusLine("OLED",config.OLED_Present))
print(util.returnStatusLine("SunAirPlus/SunControl",config.SunAirPlus_Present))
print(util.returnStatusLine("SolarMAX",config.SolarMAX_Present))
print(util.returnStatusLine("DustSensor",config.DustSensor_Present))
print()
print(util.returnStatusEnable("UseBlynk",config.USEBLYNK))
print(util.returnStatusEnable("UseWSLIGHTNING",config.USEWSLIGHTNING))
print(util.returnStatusEnable("UseWSAQI",config.USEWSAQI))
print(util.returnStatusEnable("UseWSSKYCAM",config.USEWSSKYCAM))
print(util.returnStatusEnable("UseMySQL",config.enable_MySQL_Logging))
print(util.returnStatusEnable("UseMQTT",config.MQTT_Enable))
print(util.returnStatusLine("Check WLAN",config.enable_WLAN_Detection))
print(util.returnStatusLine("WeatherUnderground",config.WeatherUnderground_Present))
print(util.returnStatusLine("UseWeatherStem",config.USEWEATHERSTEM))

print("----------------------")

# startup


pclogging.systemlog(config.INFO,"SkyWeather2 Startup Version "+config.SWVERSION )

if (config.USEBLYNK):
     updateBlynk.blynkEventUpdate("SW Startup Version "+config.SWVERSION)
     updateBlynk.blynkTerminalUpdate("SW Startup Version "+config.SWVERSION) 

subjectText = "The "+ config.STATIONKEY + " SkyWeather2 Raspberry Pi has #rebooted."
ipAddress = subprocess.check_output(['hostname',  '-I'])

if (config.USEBLYNK):
     updateBlynk.blynkEventUpdate("IPAddress: "+ipAddress.decode())
     updateBlynk.blynkTerminalUpdate("IPAddress: "+ipAddress.decode()) 

bodyText = "SkyWeather2 Version "+config.SWVERSION+ " Startup \n"+ipAddress.decode()+"\n"
if (config.SunAirPlus_Present):
	sampleSunAirPlus()
	bodyText = bodyText + "\n" + "BV=%0.2fV/BC=%0.2fmA/SV=%0.2fV/SC=%0.2fmA" % (state.batteryVoltage, state.batteryCurrent, state.solarVoltage, state.solarCurrent)

try:
    sendemail.sendEmail("test", bodyText, subjectText ,config.notifyAddress,  config.fromAddress, "");
except:

    print(traceback.format_exc())
    print("Email Exception - not sent - probably not configured")

if (config.USEBLYNK):
     updateBlynk.blynkInit()


import paho.mqtt.client as mqtt


# set up MQTT
if (config.MQTT_Enable):
    state.mqtt_client = mqtt.Client(client_id="SkyWeather2") 
    state.mqtt_client.connect(config.MQTT_Server_URL, port=config.MQTT_Port_Number)

import publishMQTT

# Set up scheduler

scheduler = BackgroundScheduler()

# for debugging
scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)

##############
# setup tasks
##############
hdc1080 = None
wiredSensors.readWiredSensors(bmp280, hdc1080)

# prints out the date and time to console
scheduler.add_job(tasks.tick, 'interval', seconds=60)

# read wireless sensor package
scheduler.add_job(wirelessSensors.readSensors) # run in background

# read wired sensor package
scheduler.add_job(wiredSensors.readWiredSensors, 'interval', args=[bmp280, hdc1080], seconds = 30) 

if (config.SWDEBUG):
    # print state
    scheduler.add_job(state.printState, 'interval', seconds=60)

if (config.USEBLYNK):
    scheduler.add_job(updateBlynk.blynkStateUpdate, 'interval', seconds=30)

if (config.MQTT_Enable):
    scheduler.add_job(publishMQTT.publish, 'interval', seconds=config.MQTT_Send_Seconds)
        
scheduler.add_job(watchDog.patTheDog, 'interval', seconds=20)   # reset the WatchDog Timer


# every 5 days at 00:04, reboot
#scheduler.add_job(rebootPi, 'cron', day='5-30/5', hour=0, minute=4, args=["5 day Reboot"]) 
	
#check for Barometric Trend (every 15 minutes)
scheduler.add_job(util.barometricTrend, 'interval', seconds=15*60)

if (config.DustSensor_Present):
    #DustSensor.read_AQI() # get current value
    scheduler.add_job(DustSensor.read_AQI, 'interval', seconds=60*12)
   
if (config.USEWSAQI):
    wirelessSensors.WSread_AQI() # get current value
    scheduler.add_job(wirelessSensors.WSread_AQI, 'interval', seconds=60*20)
   

# weather sensors

#scheduler.add_job(pclogging.writeWeatherRecord, 'interval', seconds=2*60)
scheduler.add_job(pclogging.writeWeatherRecord, 'interval', seconds=15*60)

scheduler.add_job(pclogging.writeITWeatherRecord, 'interval', seconds=15*60)

        


# sky camera
if (config.Camera_Present):
        scheduler.add_job(SkyCamera.takeSkyPicture, 'interval', seconds=config.INTERVAL_CAM_PICS__SECONDS) 


# process SkyCam Remote bi-directional messages 
if (config.MQTT_Enable== True):
    scheduler.add_job(SkyCamRemote.startMQTT)  # run in background

# SkyCam Management Programs
scheduler.add_job(PictureManagement.cleanPictures, 'cron', day='*', hour=3, minute=4, args=["Daily Picture Clean"])

scheduler.add_job(PictureManagement.cleanTimeLapses, 'cron', day='*', hour=3, minute=10, args=["Daily Time Lapse Clean"])

scheduler.add_job(PictureManagement.buildTimeLapse, 'cron', day='*', hour=5, minute=30, args=["Time Lapse Generation"])


# start scheduler
scheduler.start()
print ("-----------------")
print ("Scheduled Jobs")
print ("-----------------")
scheduler.print_jobs()
print ("-----------------")



# Main Loop

while True:

    time.sleep(1.0)



