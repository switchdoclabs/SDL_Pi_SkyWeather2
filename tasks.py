from __future__ import print_function

from datetime import datetime

# apscheduler tasks

def tick():
    print('Tick! The time is: %s' % datetime.now())


def killLogger():
    scheduler.shutdown()
    print("Scheduler Shutdown....")
    exit()

