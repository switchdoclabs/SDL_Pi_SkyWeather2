#!/usr/bin/env python3
#
# SkyWeather2 Solar Powered Weather Station
# Januayr 2020
#
# SwitchDoc Labs
# www.switchdoc.com
#
#

# imports
# Check for user imports
try:
	import conflocal as config
except ImportError:
	import config


config.SWVERSION = "001"

import time


import state
import tasks
import wirelessSensors

from apscheduler.schedulers.background import BackgroundScheduler

import apscheduler.events

# Scheduler Helpers



# print out faults inside events
def ap_my_listener(event):
        if event.exception:
              print (event.exception)
              print (event.traceback)




print ("")

print ("##########################################################")
print ("SkyWeather2 Weather Station Version "+config.SWVERSION+" - SwitchDoc Labs")
print ("")
print ("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
print ("##########################################################")
print ("")





# Set up scheduler

scheduler = BackgroundScheduler()

# for debugging
scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)

##############
# setup tasks
##############

# prints out the date and time to console
scheduler.add_job(tasks.tick, 'interval', seconds=60)

# read wireless sensor package
scheduler.add_job(wirelessSensors.readSensors) # run in background

if (config.SWDEBUG):
    # print state
    
    scheduler.add_job(state.printState, 'interval', seconds=60)

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
