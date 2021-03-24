from __future__ import print_function
#
#
# logging system from Project Curacao 
# filename: pclogger.py
# Version 1.0 10/04/13
#
# contains logging data 
#



import sys
import time
import datetime
# Check for user imports
import config
import util
import state
import updateBlynk
import MySQLdb as mdb

import traceback
import WeatherUnderground

def systemlog(level,  message):


 if (config.enable_MySQL_Logging == True):	
   LOWESTDEBUG = 0
	# open mysql database
	# write log
	# commit
	# close

   if (level >= LOWESTDEBUG):
        try:
                if (level == config.JSON):
                    if (config.USEBLYNK):
                        updateBlynk.blynkTerminalUpdate("JSON Loaded") 
                    pass
                else:
                    if (config.USEBLYNK):
                        updateBlynk.blynkTerminalUpdate(message) 
                    pass
                #print("trying database")
                con = util.getSkyWeatherConnection()
                cur = con.cursor()
                #print("before query")
                query = "INSERT INTO SystemLog(TimeStamp, Level, SystemText ) VALUES(LOCALTIMESTAMP(), %i, '%s')" % (level, message)
                #print("query=%s" % query)
                cur.execute(query)
                con.commit()


        except: 
                traceback.print_exc()
                con.rollback()
                #sys.exit(1)
        finally:
                cur.close()
                con.close()

                del cur
                del con


def errorlog(message, stacktrace):

        try:
                #print("trying database")
                con = util.getSkyWeatherConnection()
                cur = con.cursor()
                #print("before query")
                query = "INSERT INTO error_log(error) VALUES('%s')" % (message + '\n' + stacktrace)
                #print("query=%s" % query)
                cur.execute(query)
                con.commit()


        except: 
                traceback.print_exc()
                con.rollback()
                #sys.exit(1)
        finally:
                cur.close()
                con.close()

                del cur
                del con


def readLastHour24AQI():

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:

                # first calculate the 24 hour moving average for AQI
                
                print("trying database")
                con = util.getSkyWeatherConnection()
                cur = con.cursor()

                query = "SELECT id, AQI24Average FROM WeatherData ORDER BY id DESC Limit 1" 

                cur.execute(query)
                myAQIRecords = cur.fetchall()
                if (len(myAQIRecords > 0)):
                    state.Hour24_AQI = myAQIRecords[0][1]
                else:
                    state.Hour24_AQI = 0.0 

                #print("AQIRecords=",myAQIRecords)

        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con

import gpiozero 

def get60MinuteRain():
 if (config.enable_MySQL_Logging == True):	
	    # open mysql database
	    # write log
	    # commit
	    # close
        try:

           
                
                con = util.getSkyWeatherConnection()
                cur = con.cursor()
                timeDelta = datetime.timedelta(minutes=60)
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                # 60 minute
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE TimeStamp > '%s' ORDER by id ASC" % before
                #print("query=", query)
                cur.execute(query)
                rainspanrecords = cur.fetchall()
                rainspan = 0.0
                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                
                return rainspan

        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

 return 0.0 


def getCalendarDayRain():
 if (config.enable_MySQL_Logging == True):	
	    # open mysql database
	    # write log
	    # commit
	    # close
        try:

           
                
                con = util.getSkyWeatherConnection()
                cur = con.cursor()
                # calendar day rain
                query = "SELECT id, TotalRain, TimeStamp FROM WeatherData WHERE DATE(TimeStamp) = CURDATE() ORDER by id ASC"
                cur.execute(query)
                rainspanrecords = cur.fetchall()
                rainspan = 0.0
                if (len(rainspanrecords) > 0):
                    rainspan = rainspanrecords[len(rainspanrecords)-1][1] - rainspanrecords[0][1]
                
                return rainspan

        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

 return 0.0 

def writeWeatherRecord():
 Rain24Hour = getCalendarDayRain()
 print("Rain24Hour=", Rain24Hour)
 WeatherUnderground.sendWeatherUndergroundData(Rain24Hour)
 state.Rain60Minutes = get60MinuteRain()

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                cpu = gpiozero.CPUTemperature()
                state.CPUTemperature = cpu.temperature 
                print("CPUT=", state.CPUTemperature)
                # first calculate the 24 hour moving average for AQI
                
                print("trying database")
                con = util.getSkyWeatherConnection()
                cur = con.cursor()

                timeDelta = datetime.timedelta(days=1)
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT id, AQI, TimeStamp FROM WeatherData WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

                cur.execute(query)
                myAQIRecords = cur.fetchall()
                myAQITotal = 0.0
                #print("AQIRecords=",myAQIRecords)
                if (len(myAQIRecords) > 0):
                    for i in range(0, len(myAQIRecords)):

                        myAQITotal = myAQITotal + myAQIRecords[i][1] 
                    myAQI24 = (myAQITotal+float(state.AQI))/(len(myAQIRecords)+1)
                else:
                    myAQI24  = 0.0
                state.Hour24_AQI = myAQI24 

                fields = "OutdoorTemperature, OutdoorHumidity, IndoorTemperature, IndoorHumidity, TotalRain, SunlightVisible, SunlightUVIndex, WindSpeed, WindGust, WindDirection,BarometricPressure, BarometricPressureSeaLevel, BarometricTemperature, AQI, AQI24Average, BatteryOK, CPUTemperature"
                values = "%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%6.2f,%6.2f,%6.2f, \'%s\',%6.2f" % (state.OutdoorTemperature, state.OutdoorHumidity, state.IndoorTemperature, state.IndoorHumidity, state.TotalRain, state.SunlightVisible, state.SunlightUVIndex, state.WindSpeed, state.WindGust, state.WindDirection,state.BarometricPressure, state.BarometricPressureSeaLevel, state.BarometricTemperature, float(state.AQI), state.Hour24_AQI, state.BatteryOK, state.CPUTemperature)
                query = "INSERT INTO WeatherData (%s) VALUES(%s )" % (fields, values)
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con



def writeITWeatherRecord():

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:

                print("trying database")
                con = util.getSkyWeatherConnection()
                cur = con.cursor()


                fields = "DeviceID, ChannelID, Temperature, Humidity, BatteryOK, TimeRead"
                if (len(state.IndoorTH)> 0): 

                    for singleChannel in state.IndoorTH:
                        values = "%d, %d, %6.2f, %6.2f, \"%s\", \"%s\"" % (singleChannel["deviceID"], singleChannel["channelID"], singleChannel["temperature"], singleChannel["humidity"], singleChannel["batteryOK"], singleChannel["time"])
                        query = "INSERT INTO IndoorTHSensors (%s) VALUES(%s )" % (fields, values)
                       #print("query=", query)
                        cur.execute(query)
                        con.commit()
                else:
                    return
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con

